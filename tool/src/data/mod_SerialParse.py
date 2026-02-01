__all__ = [ 'SerialParse' ]

from enum\
    import Enum as _Enum

from ..helper.mod_ParseUtil import\
    ParseUtil as _ParseUtil
from ..helper.mod_ParseUtilStatus import\
    ParseUtilStatus as _ParseUtilStatus
from .mod_SerialError import\
    SerialError as _SerialError

class SerialParse:
    """
    Utility for parsing strings for deserialization
    """

    #region helper

    @classmethod
    def __parse_value1(cls,\
            function,\
            typedesc:str,\
            input:str):
        result = function(input)
        if result.status == _ParseUtilStatus.PASS:
            return result.value
        raise _SerialError(f"{input} is not a valid {typedesc}.")

    @classmethod
    def __parse_value2(cls,\
            function,\
            typedesc:str,\
            input:str,\
            min = None,\
            max = None):
        result = function(input, min, max)
        if result.status == _ParseUtilStatus.PASS:
            return result.value
        if result.status == _ParseUtilStatus.TOLO:
            raise _SerialError(f"{input} is less than the minimum value of {min}.")
        if result.status == _ParseUtilStatus.TOHI:
            raise _SerialError(f"{input} is less than the minimum value of {max}.")
        raise _SerialError(f"{input} is not a valid {typedesc}.")
        
    #endregion

    #region int

    @classmethod
    def to_int(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> int:
        """
        Attempts to parse input as an integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        return cls.__parse_value2(_ParseUtil.to_int, "integer", input, min, max)
    
    @classmethod
    def to_uint8(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> int:
        """
        Attempts to parse input as an 8-bit unsigned integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        return cls.__parse_value2(_ParseUtil.to_int, "8-bit unsigned integer", input, min, max)
        
    @classmethod
    def to_int8(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> int:
        """
        Attempts to parse input as an 8-bit signed integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        return cls.__parse_value2(_ParseUtil.to_int, "8-bit signed integer", input, min, max)
        
    @classmethod
    def to_uint16(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> int:
        """
        Attempts to parse input as a 16-bit unsigned integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        return cls.__parse_value2(_ParseUtil.to_int, "16-bit unsigned integer", input, min, max)
    
    @classmethod
    def to_int16(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> int:
        """
        Attempts to parse input as a 16-bit signed integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        return cls.__parse_value2(_ParseUtil.to_int, "16-bit signed integer", input, min, max)
    
    @classmethod
    def to_uint32(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> int:
        """
        Attempts to parse input as a 32-bit unsigned integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        return cls.__parse_value2(_ParseUtil.to_int, "32-bit unsigned integer", input, min, max)
    
    @classmethod
    def to_int32(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> int:
        """
        Attempts to parse input as a 32-bit signed integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        return cls.__parse_value2(_ParseUtil.to_int, "32-bit signed integer", input, min, max)
    
    @classmethod
    def to_uint64(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> int:
        """
        Attempts to parse input as a 64-bit unsigned integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        return cls.__parse_value2(_ParseUtil.to_int, "64-bit unsigned integer", input, min, max)
    
    @classmethod
    def to_int64(cls,\
            input:str,\
            min:None|int = None,\
            max:None|int = None)\
            -> int:
        """
        Attempts to parse input as a 64-bit signed integer
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        return cls.__parse_value2(_ParseUtil.to_int, "64-bit signed integer", input, min, max)

    #endregion

    #region float

    @classmethod
    def to_float(cls,\
            input:str,\
            min:None|float,\
            max:None|float)\
            -> float:
        """
        Attempts to parse input as a floating-point decimal
        
        :param input: Input
        :param min: Minimum value
        :param max: Maximum value
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        return cls.__parse_value2(_ParseUtil.to_int, "floating-point decimal", input, min, max)
    
    #endregion

    #region enum

    @classmethod
    def to_enum(cls,\
            input:str,\
            type:type[_Enum],\
            ignorecase:bool = False)\
            -> _Enum:
        """
        Attempts to parse input as an Enum
        
        :param input: Input
        :param type: Enum type
        :param ignorecase: Whether or not to ignore case differences
        :return: Parsed value
        :raise SerialError: input is invalid
        """
        result = _ParseUtil.to_enum(input, type, ignorecase = ignorecase)
        if result.status == _ParseUtilStatus.PASS:
            return result.value
        raise _SerialError(f"{input} is not a valid {type.__name__}.")

    #endregion