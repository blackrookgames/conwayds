all = []

from typing import\
    cast as _cast

from ....ds.mod_DSPalette import\
    DSPalette as _DSPalette
from ....ds.mod_DSTileset8 import\
    DSTileset8 as _DSTileset8
from ....ds.mod_DSUtil import\
    DSUtil as _DSUtil
from ....img.mod_ImgImage import\
    ImgImage as _ImgImage
from ....img.mod_ImgPalette import\
    ImgPalette as _ImgPalette

from ...mod__Creator import _Creator
from .c_imgimage__dstileset import _HHCmdConvert

class _HHHCmdConvert(_HHCmdConvert):
    def _main(self, creator: _Creator):
        self_palette = _cast(str, self.palette) # type: ignore
        self_tpr = _cast(int, self.tpr) # type: ignore
        self_noalpha = _cast(bool, self.noalpha) # type: ignore
        ipal = _cast(_DSPalette, creator.get_var(self_palette, _DSPalette))
        itiles = _cast(_DSTileset8, self._data)
        image = _ImgImage(palsize = 256, alpha = not self_noalpha)
        _DSUtil.palette_set_pal(_cast(_ImgPalette, image.palette), ipal)
        _DSUtil.tileset8_set_img(image, itiles, tpr = self_tpr)
        creator.set_var(self._ovar, image)

type _type = _DSTileset8
def _create(data, ovar): return _HHHCmdConvert(data, ovar)