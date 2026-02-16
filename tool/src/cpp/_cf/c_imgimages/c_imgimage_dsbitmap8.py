all = []

from typing import\
    cast as _cast

from ....cli.mod_CLIOptionFlagDef import\
    CLIOptionFlagDef as _CLIOptionFlagDef
from ....cli.mod_CLIRequiredDef import\
    CLIRequiredDef as _CLIRequiredDef
from ....ds.mod_DSBitmap8 import\
    DSBitmap8 as _DSBitmap8
from ....ds.mod_DSPalette import\
    DSPalette as _DSPalette
from ....ds.mod_DSUtil import\
    DSUtil as _DSUtil
from ....img.mod_ImgImage import\
    ImgImage as _ImgImage
from ....img.mod_ImgPalette import\
    ImgPalette as _ImgPalette

from ...mod__Creator import _Creator
from ..c__HCmdConvert import _HCmdConvert

class _HHCmdConvert(_HCmdConvert):
    __palette = _CLIRequiredDef("palette")
    __noalpha = _CLIOptionFlagDef("noalpha")
    def _main(self, creator: _Creator):
        self_palette = _cast(str, self.palette) # type: ignore
        self_noalpha = _cast(bool, self.noalpha) # type: ignore
        ipal = _cast(_DSPalette, creator.get_var(self_palette, _DSPalette))
        ibmp = _cast(_DSBitmap8, self._data)
        image = _ImgImage(palsize = 256, alpha = not self_noalpha)
        _DSUtil.palette_set_pal(_cast(_ImgPalette, image.palette), ipal)
        _DSUtil.bitmap8_set_img(image, ibmp)
        creator.set_var(self._ovar, image)

type _type = _DSBitmap8
def _create(data, ovar): return _HHCmdConvert(data, ovar)