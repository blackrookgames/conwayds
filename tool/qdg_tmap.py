import numpy as np
import os
import sys

from async_tkinter_loop import async_mainloop
from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from typing import cast

import qdg.tmap.w__common as qdg_tmap_common
import qdg.tmap.w_main as qdg_tmap_main
import src.cli as cli
import src.cliutil as cliutil
import src.helper as helper

TILESIZE = 8

def init_cache():
    CACHENAME = ".cache"
    # Determine path
    if len(sys.argv) > 0:
        path = Path(sys.argv[0])
        ext = helper.StrUtil.find_last(path.name, '.')
        cachepath = path.parent.joinpath(CACHENAME).joinpath(path.name if (ext == -1) else path.name[:ext])
    else:
        cachepath = Path('.').joinpath(CACHENAME)
    # Make directory
    os.makedirs(str(cachepath), exist_ok = True)
    # Return path
    return cachepath
CACHEDIR = init_cache()

class qgd_tmap(cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "Open and edit a tilemap file"

    #region required

    __tilemap = cli.CLIRequiredDef(\
        name = "tilemap",\
        desc = "Path of tilemap file")

    #endregion

    #region optional

    __tileset = cli.CLIOptionWArgDef(\
        name = "tileset",\
        short = 't',\
        desc = "Path of tileset bitmap file (must be paletted)",\
        default = None)

    __reload = cli.CLIOptionFlagDef(\
        name = "reload",\
        short = 'r',\
        desc = "Force a reload, ignoring cached data")

    #endregion

    #region helper methods

    def __load_tilemap(self):
        self_tilemap = cast(str, self.tilemap) # type: ignore
        content = qdg_tmap_common.Content(Path(self_tilemap))
        if content.path.exists():
            print("Loading tilemap")
            content.load()
        else:
            print("Creating tilemap")
            content.save()
        return content

    def __load_tileset(self):
        self_tileset = cast(None | str, self.tileset) # type: ignore
        self_reload = cast(bool, self.reload) # type: ignore
        _IMAGE_W = 2048
        _IMAGE_H = 2048
        _CACHE_PATH = CACHEDIR.joinpath("image.png")
        _CACHE_KEY = 'reference'
        # Is tileset source cached?
        if (not self_reload) and _CACHE_PATH.exists():
            # Open cached image
            cache_img = cliutil.CLIPILUtil.image_from_file(str(_CACHE_PATH))
            # Do the sources match?
            matching = False
            if _CACHE_KEY in cache_img.info:
                if self_tileset is not None:
                    if Path(cache_img.info[_CACHE_KEY]).resolve() == Path(self_tileset).resolve():
                        matching = True
            elif self_tileset is None:
                matching = True
            if matching: return cache_img
        #region Make tileset
        # Progress updater
        def _prog(_prog:float):
            nonlocal prog_len
            # Erase previous
            sys.stdout.write("\b \b" * prog_len)
            # Write new
            _str = f"{round(_prog)}%"
            prog_len = len(_str)
            sys.stdout.write(_str)
            # Flush
            sys.stdout.flush()
        prog_len = 0
        # Load tileset
        print("Loading tileset")
        tileset = qdg_tmap_common.IFileTileset(self_tileset)
        # Create image
        print("Processing tileset ", end = '', flush = True)
        image = Image.new('RGB', (_IMAGE_W, _IMAGE_H))
        for _i in range(qdg_tmap_common.TILESET_TILE_COUNT):
            _finaltile = np.uint16(_i)
            # Properties
            _tile_index, _tile_sub, _tile_flip = qdg_tmap_common.finaltile_from(_finaltile)
            _tile_flip_x = (_tile_flip & 0b01) != 0 # TODO: Update
            _tile_flip_y = (_tile_flip & 0b10) != 0 # TODO: Update
            # Input X-coordinates
            if _tile_flip_x:
                _x_beg = qdg_tmap_common.TILESET_TILE_WIDTH - 1
                _x_inc = -1
            else:
                _x_beg = 0
                _x_inc = 1
            # Input Y-coordinates
            if _tile_flip_y:
                _y_beg = qdg_tmap_common.TILESET_TILE_HEIGHT - 1
                _y_inc = -1
            else:
                _y_beg = 0
                _y_inc = 1
            # Tile
            _off_x, _off_y = qdg_tmap_common.Tileset.offset(_finaltile)
            for _x in range(qdg_tmap_common.TILESET_TILE_WIDTH):
                for _y in range(qdg_tmap_common.TILESET_TILE_HEIGHT):
                    _in_x = _x_beg + _x * _x_inc
                    _in_y = _y_beg + _y * _y_inc
                    _color = tileset.palette[_tile_sub][tileset.tileset[_tile_index, _in_x, _in_y]]
                    image.putpixel((_off_x + _x, _off_y + _y), _color)
            # Next
            _prog(100 * ((_i + 1) / qdg_tmap_common.TILESET_TILE_COUNT))
        print()
        # Save image
        def _save():
            nonlocal image, self_tileset
            try:
                # Custom metadata
                _info = PngInfo()
                if self_tileset is not None:
                    _info.add_text(_CACHE_KEY, self_tileset)
                # Save
                image.save(_CACHE_PATH, pnginfo = _info)
                # Success!!!
                return
            except Exception as e:
                error = cliutil.CLICommandError(e)
            raise error
        _save()
        # Return
        return image
        #endregion

    #endregion

    #region methods

    def _main(self):
        try:
            tilesrc = self.__load_tileset()
            content = self.__load_tilemap()
            async_mainloop(qdg_tmap_main.Window(content, tilesrc))
        except cliutil.CLICommandError as e:
            print(f"ERROR: {e}", file = sys.stderr)
            return 1
        return 0

    #endregion

sys.exit(qgd_tmap().execute(sys.argv))