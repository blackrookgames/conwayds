__all__ = [\
    'CLIListUtil',]

from collections.abc import\
    Collection as _Collection

from ..helper.mod_const import\
    I8_NEG as _I8_NEG,\
    I16_NEG as _I16_NEG,\
    I32_NEG as _I32_NEG,\
    I64_NEG as _I64_NEG
from .mod_CLICommandError import\
    CLICommandError as _CLICommandError

class CLIListUtil:
    """
    CLI-utility for list-related operations
    """

    #region helper methods

    @classmethod
    def __int_from_file(cls, path:str, bytespervalue:int, neg:int = 0):
        """
        Assume
        - bytespervalue > 0
        """
        try:
            # Read from file
            with open(path, 'rb') as f:
                raw = f.read()
            # Create list
            data:list[int] = []
            _pos = 0
            for _i in range(len(raw) // bytespervalue):
                _value = 0
                # Extract bytes
                _shift = 0
                for _j in range(bytespervalue):
                    _value |= raw[_pos] << _shift
                    _shift += 8
                    _pos += 1
                # Correct sign
                if (_value & neg) != 0:
                    _value -= neg << 1
                # Add value
                data.append(_value)
            # Success!!!
            return data
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    @classmethod
    def __int_to_file(cls, data:_Collection[int], path:str, bytespervalue:int, neg:int = 0):
        """
        Assume
        - bytespervalue > 0
        """
        try:
            # Create byte array
            bytedata = bytearray(len(data) * bytespervalue)
            _pos = 0
            for _value in data:
                if _pos == len(bytedata): break
                _val = _value
                # Fix sign
                if _val < 0: _val += neg << 1
                # Convert to bytes
                for _j in range(bytespervalue):
                    bytedata[_pos] = _val & 0xFF
                    _val >>= 8
                    _pos += 1
            # Write to file
            with open(path, 'wb') as f:
                f.write(bytes(bytedata))
            # Success!!!
            return
        except Exception as e:
            error = _CLICommandError(e)
        raise error
    
    #endregion

    #region uint8

    @classmethod
    def uint8_from_file(cls, path:str):
        """
        Creates a list of 8-bit unsigned integers by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, 1) 

    @classmethod
    def uint8_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 8-bit unsigned integers to a file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, 1)

    #endregion

    #region int8

    @classmethod
    def int8_from_file(cls, path:str):
        """
        Creates a list of 8-bit signed integers by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, 1, neg = _I8_NEG) 

    @classmethod
    def int8_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 8-bit signed integers to a file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, 1, neg = _I8_NEG)

    #endregion

    #region uint16

    @classmethod
    def uint16_from_file(cls, path:str):
        """
        Creates a list of 16-bit unsigned integers by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, 2) 

    @classmethod
    def uint16_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 16-bit unsigned integers to a file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, 2)

    #endregion

    #region int16

    @classmethod
    def int16_from_file(cls, path:str):
        """
        Creates a list of 16-bit signed integers by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, 2, neg = _I16_NEG) 

    @classmethod
    def int16_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 16-bit signed integers to a file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, 2, neg = _I16_NEG)

    #endregion

    #region uint32

    @classmethod
    def uint32_from_file(cls, path:str):
        """
        Creates a list of 32-bit unsigned integers by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, 4) 

    @classmethod
    def uint32_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 32-bit unsigned integers to a file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, 4)

    #endregion

    #region int32

    @classmethod
    def int32_from_file(cls, path:str):
        """
        Creates a list of 32-bit signed integers by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, 4, neg = _I32_NEG) 

    @classmethod
    def int32_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 32-bit signed integers to a file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, 4, neg = _I32_NEG)

    #endregion

    #region uint64

    @classmethod
    def uint64_from_file(cls, path:str):
        """
        Creates a list of 64-bit unsigned integers by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, 8) 

    @classmethod
    def uint64_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 64-bit unsigned integers to a file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, 8)

    #endregion

    #region int64

    @classmethod
    def int64_from_file(cls, path:str):
        """
        Creates a list of 64-bit signed integers by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created list
        :raise CLICommandError:
            An error occurred
        """
        return cls.__int_from_file(path, 8, neg = _I64_NEG) 

    @classmethod
    def int64_to_file(cls, data:_Collection[int], path:str):
        """
        Saves a list of 64-bit signed integers to a file
        
        :param data:
            List of data to save
        :param path:
            Path of output file
        :raise CLICommandError:
            An error occurred
        """
        cls.__int_to_file(data, path, 8, neg = _I64_NEG)

    #endregion
