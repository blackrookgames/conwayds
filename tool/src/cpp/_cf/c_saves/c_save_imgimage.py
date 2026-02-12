all = []

from typing import\
    cast as _cast

from ....cliutil.mod_CLICommandError import\
    CLICommandError as _CLICommandError
from ....cliutil.mod_CLIImgUtil import\
    CLIImgUtil as _CLIImgUtil
from ....img.mod_ImgImage import\
    ImgImage as _ImgImage

from ...mod__CmdFuncError import _CmdFuncError
from ...mod__Creator import _Creator
from .c__HCmdSave import _HCmdSave

class _HHCmdSave(_HCmdSave):
    def _main(self, creator: _Creator):
        try:
            self_path = _cast(str, self.path) # type: ignore
            path = creator.resolvepath(self_path)
            data = _cast(_ImgImage, self._data)
            _CLIImgUtil.image_to_file(data, path)
            return
        except _CLICommandError as _e:
            e = _CmdFuncError(_e)
        raise e

type _type = _ImgImage
def _create(data): return _HHCmdSave(data)