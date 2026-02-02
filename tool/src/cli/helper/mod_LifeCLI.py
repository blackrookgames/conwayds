__all__ = [\
    'LifeCLI',\
    'LifeCLIFormat',]

from enum import\
    auto as _auto,\
    Enum as _Enum
from io import\
    StringIO as _StringIO
from sys import\
    stderr as _stderr
from typing import\
    cast as _cast

from ...data.mod_SerialError import\
    SerialError as _SerialError
from ...life.mod_LifePattern import\
    LifePattern as _LifePattern
from ...life.mod_LifePatternRule import\
    LifePatternRule as _LifePatternRule
from ...life.mod_LifeSerial import\
    LifeSerial as _LifeSerial
from ..mod_CLIParseUtil import\
    CLIParseUtil as _CLIParseUtil
from .mod_ImgCLI import\
    ImgCLI as _ImgCLI
from .mod_StrCLI import\
    StrCLI as _StrCLI

class LifeCLIFormat(_Enum):
    """
    Represents a format for storing pattern data
    """

    RLE = _auto()
    """
    Pattern data is stored as run-length encoded data
    """

    TXT = _auto()
    """
    Pattern data is stored in plain text\n
    NOTE: Rule configurations cannot be stored in this format
    """

    IMG = _auto()
    """
    Pattern data is stored as an image\n
    NOTE: Rule configurations cannot be stored in this format
    """

class LifeCLI:
    """
    Utility for Life-related operations
    """

    #region pattern

    @classmethod
    def pattern_load(cls, path:str, format:None|LifeCLIFormat|str = None):
        """
        Attrmpts to load a LifePattern from a file
        
        :param path:
            Path of input file
        :param format:
            Data format (use None to auto-detect)
        :return:
            Loaded LifePattern (or None if an error occurred)
        """
        # Get format
        if format is not None:
            if isinstance(format, str):
                _result, format = _CLIParseUtil.to_enum(format, (LifeCLIFormat, True, )) # type: ignore
                if not _result: return None
                format = _cast(LifeCLIFormat, format)
        else:
            if _ImgCLI.checkext(path):
                format = LifeCLIFormat.IMG
            elif path.endswith(".rle"):
                format = LifeCLIFormat.RLE
            else:
                format = LifeCLIFormat.TXT
        # Load
        match format:
            case LifeCLIFormat.RLE:
                return cls.pattern_load_rle(path)
            case LifeCLIFormat.TXT:
                return cls.pattern_load_txt(path)
            case LifeCLIFormat.IMG:
                return cls.pattern_load_img(path)
            case _: return None # Should never happen

    @classmethod
    def pattern_save(cls, pattern:_LifePattern, path:str, format:None|LifeCLIFormat|str = None):
        """
        Attrmpts to save a LifePattern to a file
        
        :param pattern:
            Pattern to save
        :param path:
            Path of output file
        :param format:
            Data format (use None to auto-detect)
        :return:
            Whether or not successful
        """
        # Get format
        if format is not None:
            if isinstance(format, str):
                _result, format = _CLIParseUtil.to_enum(format, (LifeCLIFormat, True, )) # type: ignore
                if not _result: return False
                format = _cast(LifeCLIFormat, format)
        else:
            if _ImgCLI.checkext(path):
                format = LifeCLIFormat.IMG
            elif path.endswith(".rle"):
                format = LifeCLIFormat.RLE
            else:
                format = LifeCLIFormat.TXT
        # Load
        match format:
            case LifeCLIFormat.RLE:
                return cls.pattern_save_rle(pattern, path)
            case LifeCLIFormat.TXT:
                return cls.pattern_save_txt(pattern, path)
            case LifeCLIFormat.IMG:
                return cls.pattern_save_img(pattern, path)
            case _: return False # Should never happen

    #endregion

    #region pattern rle

    @classmethod
    def pattern_load_rle(cls, path:str):
        """
        Attrmpts to create a pattern using data from an RLE file
        
        :param path:
            Path of input file
        :return:
            Created life pattern
        """
        # Load string
        string = _StrCLI.load(path)
        if string is None: return None
        # Read string
        try:
            return _LifeSerial.pattern_from_rle(string)
        except _SerialError as _e:
            print(_e, file = _stderr)
            return None

    @classmethod
    def pattern_save_rle(cls, pattern:_LifePattern, path:str):
        """
        Attempts to save pattern data to an RLE file
        
        :param pattern:
            Life pattern
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        string = _LifeSerial.pattern_to_rle(pattern)
        return _StrCLI.save(string, path)

    #endregion
    
    #region pattern txt

    @classmethod
    def pattern_load_txt(cls, path:str):
        """
        Attempts to create a pattern using data from a text file
        
        :param path:
            Path of input file
        :return:
            Created life pattern (or None if an error occurred)
        """
        # Load string
        string = _StrCLI.load(path)
        if string is None: return None
        # Read string
        try:
            return _LifeSerial.pattern_from_txt(string)
        except _SerialError as _e:
            print(_e, file = _stderr)
            return None

    @classmethod
    def pattern_save_txt(cls, pattern:_LifePattern, path:str):
        """
        Attrmpts to save pattern data to a text file\n
        Note that any rule configurations will be lost
        
        :param pattern:
            Life pattern
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        string = _LifeSerial.pattern_to_txt(pattern)
        return _StrCLI.save(string, path)

    #endregion

    #region pattern img

    @classmethod
    def pattern_load_img(cls, path:str):
        """
        Attempts to create a pattern using data from an image
        
        :param path:
            Path of input file
        :return:
            Created life pattern (or None if an error occurred)
        """
        # Load image
        img = _ImgCLI.load(path)
        if img is None: return None
        # Read image
        return _LifeSerial.pattern_from_img(img)

    @classmethod
    def pattern_save_img(cls, pattern:_LifePattern, path:str):
        """
        Attrmpts to save pattern data to an image\n
        Note that any rule configurations will be lost
        
        :param pattern:
            Life pattern
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        img = _LifeSerial.pattern_to_img(pattern)
        return _ImgCLI.save(img, path)

    #endregion