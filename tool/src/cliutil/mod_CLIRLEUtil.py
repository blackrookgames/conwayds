__all__ = [\
    'CLIRLEUtil',]

from collections.abc import\
    Collection as _Collection
from typing import\
    Callable as _Callable

from ..helper.mod_const import\
    I8_MAX as _I8_MAX,\
    I8_MIN as _I8_MIN,\
    I16_MAX as _I16_MAX,\
    I16_MIN as _I16_MIN,\
    I32_MAX as _I32_MAX,\
    I32_MIN as _I32_MIN,\
    I64_MAX as _I64_MAX,\
    I64_MIN as _I64_MIN,\
    U8_MAX as _U8_MAX,\
    U8_MIN as _U8_MIN,\
    U16_MAX as _U16_MAX,\
    U16_MIN as _U16_MIN,\
    U32_MAX as _U32_MAX,\
    U32_MIN as _U32_MIN,\
    U64_MAX as _U64_MAX,\
    U64_MIN as _U64_MIN
from .mod_CLICommandError import\
    CLICommandError as _CLICommandError
from .mod_CLIListUtil import\
    CLIListUtil as _CLIListUtil

class CLIRLEUtil:
    """
    CLI-utility for RLE-related operations
    """

    #region helper methods

    @classmethod
    def __int_from_file(cls,\
            path:str,\
            func:_Callable[[str], list[int]]):
        try: 
            # Read from file
            data = func(path)
            # Decode RLE
            if len(data) > 0:
                # Get RLE prefix
                prefix = data.pop(0)
                # Decode
                _pos = 0
                while _pos < len(data):
                    if data[_pos] == prefix:
                        # Pop prefix
                        data.pop(_pos)
                        # Make sure there's raw data left for decoding
                        if (_pos + 2) > len(data): break
                        # Get value
                        _value = data.pop(_pos)
                        # Get occurances
                        _occur = data.pop(_pos)
                        # Insert values
                        for _i in range(_occur): data.insert(_pos, _value)
                    else: _pos += 1
            # Success!!!
            return data
        except _CLICommandError as e:
            error = e
        raise error

    @classmethod
    def __int_to_file(cls,\
            data:_Collection[int],\
            path:str,\
            func:_Callable[[_Collection[int], str], None],\
            minvalue:int,\
            maxvalue:int,\
            combos:int):
        try: 
            #region Determine RLE Prefix
            # Create intermediate
            _occurs:dict[int, int] = {}
            for _value in data:
                if _value in _occurs: _occurs[_value] += 1
                else: _occurs[_value] = 1
            # Determine an RLE prefix
            if len(_occurs) == combos:
                prefix = 0
                _min = -1
                for _k, _v in _occurs.items():
                    if _min == -1 or _min > _v:
                        prefix = _k
                        _min = _v
            else:
                prefix = minvalue
                while prefix in _occurs: prefix += 1
            #endregion
            # Create Intermediate Data 
            interdata:list[int] = []
            # Add prefix
            interdata.insert(0, prefix)
            # Add data
            _occur = 0
            _value = 0
            def _addvalue():
                nonlocal prefix, interdata, _occur, _value
                if _occur > 1 or _value == prefix:
                    interdata.append(prefix)
                    interdata.append(_value)
                    interdata.append(_occur)
                else: interdata.append(_value)
            for _v in data:
                if _occur > 0 and (_value != _v or _occur == maxvalue):
                    _addvalue()
                    _occur = 0
                _value = _v
                _occur += 1
            if _occur > 0: _addvalue()
            # Write to file
            func(interdata, path)
            # Success!!!
            return
        except _CLICommandError as e:
            error = e
        raise error
    
    #endregion

    #region uint8

    @classmethod
    def uint8_from_file(cls, path:str):
        """
        Creates a list of 8-bit unsigned integers by loading from an RLE-compressed file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, _CLIListUtil.uint8_from_file) 

    @classmethod
    def uint8_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 8-bit unsigned integers to an RLE-compressed file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, _CLIListUtil.uint8_to_file, _U8_MIN, _U8_MAX, _U8_MAX - _U8_MIN)

    #endregion

    #region int8

    @classmethod
    def int8_from_file(cls, path:str):
        """
        Creates a list of 8-bit signed integers by loading from an RLE-compressed file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, _CLIListUtil.int8_from_file) 

    @classmethod
    def int8_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 8-bit signed integers to an RLE-compressed file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, _CLIListUtil.int8_to_file, _I8_MIN, _I8_MAX, _I8_MAX - _I8_MIN)

    #endregion

    #region uint16

    @classmethod
    def uint16_from_file(cls, path:str):
        """
        Creates a list of 16-bit unsigned integers by loading from an RLE-compressed file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, _CLIListUtil.uint16_from_file) 

    @classmethod
    def uint16_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 16-bit unsigned integers to an RLE-compressed file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, _CLIListUtil.uint16_to_file, _U16_MIN, _U16_MAX, _U16_MAX - _U16_MIN)

    #endregion

    #region int16

    @classmethod
    def int16_from_file(cls, path:str):
        """
        Creates a list of 16-bit signed integers by loading from an RLE-compressed file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, _CLIListUtil.int16_from_file) 

    @classmethod
    def int16_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 16-bit signed integers to an RLE-compressed file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, _CLIListUtil.int16_to_file, _I16_MIN, _I16_MAX, _I16_MAX - _I16_MIN)

    #endregion

    #region uint32

    @classmethod
    def uint32_from_file(cls, path:str):
        """
        Creates a list of 32-bit unsigned integers by loading from an RLE-compressed file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, _CLIListUtil.uint32_from_file) 

    @classmethod
    def uint32_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 32-bit unsigned integers to an RLE-compressed file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, _CLIListUtil.uint32_to_file, _U32_MIN, _U32_MAX, _U32_MAX - _U32_MIN)

    #endregion

    #region int32

    @classmethod
    def int32_from_file(cls, path:str):
        """
        Creates a list of 32-bit signed integers by loading from an RLE-compressed file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, _CLIListUtil.int32_from_file) 

    @classmethod
    def int32_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 32-bit signed integers to an RLE-compressed file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, _CLIListUtil.int32_to_file, _I32_MIN, _I32_MAX, _I32_MAX - _I32_MIN)

    #endregion

    #region uint64

    @classmethod
    def uint64_from_file(cls, path:str):
        """
        Creates a list of 64-bit unsigned integers by loading from an RLE-compressed file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, _CLIListUtil.uint64_from_file) 

    @classmethod
    def uint64_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 64-bit unsigned integers to an RLE-compressed file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, _CLIListUtil.uint64_to_file, _U64_MIN, _U64_MAX, _U64_MAX - _U64_MIN)

    #endregion

    #region int64

    @classmethod
    def int64_from_file(cls, path:str):
        """
        Creates a list of 64-bit signed integers by loading from an RLE-compressed file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, _CLIListUtil.int64_from_file) 

    @classmethod
    def int64_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 64-bit signed integers to an RLE-compressed file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, _CLIListUtil.int64_to_file, _I64_MIN, _I64_MAX, _I64_MAX - _I64_MIN)

    #endregion