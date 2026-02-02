__all__ = [\
    'ByteW']

from ..helper.mod_const import *
from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

class ByteW:
    """
    Utility for reading byte data
    """

    #region helper methods

    @classmethod
    def __write_l(cls, array:bytearray, start:int, count:int, value:int, minn:int, maxx:int):
        end = start + count
        if start < 0 or end > len(array):
            raise IndexError("start is out of range.")
        if value < minn: value = minn
        if value > maxx: value = maxx
        while start < end:
            array[start] = value & 0xFF
            start += 1
            value >>= 8

    @classmethod
    def __write_b(cls, array:bytearray, start:int, count:int, value:int, minn:int, maxx:int):
        end = start + count
        if start < 0 or end > len(array):
            raise IndexError("start is out of range.")
        if value < minn: value = minn
        if value > maxx: value = maxx
        while end > start:
            end -= 1
            array[end] = value & 0xFF
            value >>= 8
        
    #endregion

    #region methods

    #region uint8

    @classmethod
    def write_uint8(cls, array:bytearray, index:int, value:int):
        """
        Writes an 8-bit unsigned integer to a byte array

        :param array: Byte array
        :param index: Index to write value
        :param value: Value to write
        :raise IndexError: index is out of range
        """
        if index < 0 or index >= len(array):
            raise IndexError("index is out of range.")
        array[index] = max(U8_MIN, min(U8_MAX, value)) & 0xFF

    #endregion

    #region uint8

    @classmethod
    def write_int8(cls, array:bytearray, index:int, value:int):
        """
        Writes an 8-bit signed integer to a byte array

        :param array: Byte array
        :param index: Index to write value
        :param value: Value to write
        :raise IndexError: index is out of range
        """
        if index < 0 or index >= len(array):
            raise IndexError("index is out of range.")
        array[index] = max(I8_MIN, min(I8_MAX, value)) & 0xFF

    #endregion

    #region uint16

    @classmethod
    def write_uint16(cls, array:bytearray, start:int, value:int, big:bool):
        """
        Writes a 16-bit unsigned integer to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :param big: Whether or not to store in big-endian
        :raise IndexError: start is out of range
        """
        if big: cls.write_uint16_b(array, start, value)
        else: cls.write_uint16_l(array, start, value)
    
    @classmethod
    def write_uint16_l(cls, array:bytearray, start:int, value:int):
        """
        Writes a 16-bit unsigned integer in little-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_l(array, start, U16_SIZE, value, U16_MIN, U16_MAX)
    
    @classmethod
    def write_uint16_b(cls, array:bytearray, start:int, value:int):
        """
        Writes a 16-bit unsigned integer in big-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_b(array, start, U16_SIZE, value, U16_MIN, U16_MAX)

    #endregion

    #region int16

    @classmethod
    def write_int16(cls, array:bytearray, start:int, value:int, big:bool):
        """
        Writes a 16-bit signed integer to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :param big: Whether or not to store in big-endian
        :raise IndexError: start is out of range
        """
        if big: cls.write_int16_b(array, start, value)
        else: cls.write_int16_l(array, start, value)
    
    @classmethod
    def write_int16_l(cls, array:bytearray, start:int, value:int):
        """
        Writes a 16-bit signed integer in little-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_l(array, start, I16_SIZE, value, I16_MIN, I16_MAX)
    
    @classmethod
    def write_int16_b(cls, array:bytearray, start:int, value:int):
        """
        Writes a 16-bit signed integer in big-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_b(array, start, I16_SIZE, value, I16_MIN, I16_MAX)

    #endregion

    #region uint32

    @classmethod
    def write_uint32(cls, array:bytearray, start:int, value:int, big:bool):
        """
        Writes a 32-bit unsigned integer to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :param big: Whether or not to store in big-endian
        :raise IndexError: start is out of range
        """
        if big: cls.write_uint32_b(array, start, value)
        else: cls.write_uint32_l(array, start, value)
    
    @classmethod
    def write_uint32_l(cls, array:bytearray, start:int, value:int):
        """
        Writes a 32-bit unsigned integer in little-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_l(array, start, U32_SIZE, value, U32_MIN, U32_MAX)
    
    @classmethod
    def write_uint32_b(cls, array:bytearray, start:int, value:int):
        """
        Writes a 32-bit unsigned integer in big-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_b(array, start, U32_SIZE, value, U32_MIN, U32_MAX)

    #endregion

    #region int32

    @classmethod
    def write_int32(cls, array:bytearray, start:int, value:int, big:bool):
        """
        Writes a 32-bit signed integer to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :param big: Whether or not to store in big-endian
        :raise IndexError: start is out of range
        """
        if big: cls.write_int32_b(array, start, value)
        else: cls.write_int32_l(array, start, value)
    
    @classmethod
    def write_int32_l(cls, array:bytearray, start:int, value:int):
        """
        Writes a 32-bit signed integer in little-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_l(array, start, I32_SIZE, value, I32_MIN, I32_MAX)
    
    @classmethod
    def write_int32_b(cls, array:bytearray, start:int, value:int):
        """
        Writes a 32-bit signed integer in big-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_b(array, start, I32_SIZE, value, I32_MIN, I32_MAX)

    #endregion

    #region uint64

    @classmethod
    def write_uint64(cls, array:bytearray, start:int, value:int, big:bool):
        """
        Writes a 64-bit unsigned integer to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :param big: Whether or not to store in big-endian
        :raise IndexError: start is out of range
        """
        if big: cls.write_uint64_b(array, start, value)
        else: cls.write_uint64_l(array, start, value)
    
    @classmethod
    def write_uint64_l(cls, array:bytearray, start:int, value:int):
        """
        Writes a 64-bit unsigned integer in little-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_l(array, start, U64_SIZE, value, U64_MIN, U64_MAX)
    
    @classmethod
    def write_uint64_b(cls, array:bytearray, start:int, value:int):
        """
        Writes a 64-bit unsigned integer in big-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_b(array, start, U64_SIZE, value, U64_MIN, U64_MAX)

    #endregion

    #region int64

    @classmethod
    def write_int64(cls, array:bytearray, start:int, value:int, big:bool):
        """
        Writes a 64-bit signed integer to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :param big: Whether or not to store in big-endian
        :raise IndexError: start is out of range
        """
        if big: cls.write_int64_b(array, start, value)
        else: cls.write_int64_l(array, start, value)
    
    @classmethod
    def write_int64_l(cls, array:bytearray, start:int, value:int):
        """
        Writes a 64-bit signed integer in little-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_l(array, start, I64_SIZE, value, I64_MIN, I64_MAX)
    
    @classmethod
    def write_int64_b(cls, array:bytearray, start:int, value:int):
        """
        Writes a 64-bit signed integer in big-endian to a byte array

        :param array: Byte array
        :param start: Start index
        :param value: Value to write
        :raise IndexError: start is out of range
        """
        cls.__write_b(array, start, I64_SIZE, value, I64_MIN, I64_MAX)

    #endregion

    #endregion