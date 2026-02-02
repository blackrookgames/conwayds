__all__ = [\
    'DataBuffer']

from typing import\
    Callable as _Callable

from ..helper.mod_const import *
from .mod_ByteR import\
    ByteR as _ByteR
from .mod_ByteW import\
    ByteW as _ByteW
from .mod_DataError import\
    DataError as _DataError
from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

class DataBuffer:
    """
    Represents a buffer containing byte data
    """

    #region init

    def __init__(self,\
            size:int = 0):
        if size < 0:
            raise ValueError("size must be greater than or equal to zero.")
        self.__data = bytearray(size)
        self.__cursor = 0

    #endregion

    #region operators

    def __len__(self):
        return len(self.__data)
    
    def __getitem__(self, index):
        try:
            return self.__data[self.__getindex(index)]
        except Exception as _e: e = _e
        raise e
    
    def __setitem__(self, index, value):
        try:
            _index = self.__getindex(index)
            self.__data[_index] = _ErrorUtil.valid_int(value, param = 'value')
            return
        except Exception as _e: e = _e
        raise e
    
    def __iter__(self):
        for _byte in self.__data:
            yield _byte

    #endregion

    #region properties

    @property
    def cursor(self):
        """
        Position of the cursor
        """
        return self.__cursor

    #endregion

    #region helper methods

    def __getindex(self, index):
        _index = _ErrorUtil.valid_int(index, param = 'index')
        if _index < 0 or _index >= len(self.__data):
            raise IndexError(f"index is out of range")
        return _index
    
    def __reserve(self, count:int):
        end = self.__cursor + count
        if end <= len(self.__data): return
        self.__data.extend(b'\x00' * (end - len(self.__data)))

    def __read_int(self, count:int, method:_Callable[[bytearray, int], int]):
        try:
            _value = method(self.__data, self.__cursor)
            self.__cursor += count
            return _value
        except IndexError as _e:
            e = _e
        raise e
    
    def __read_int2(self, count:int, method:_Callable[[bytearray, int, bool], int], big:bool):
        try:
            _value = method(self.__data, self.__cursor, big)
            self.__cursor += count
            return _value
        except IndexError as _e:
            e = _e
        raise e
    
    def __write_int(self, count:int, method:_Callable[[bytearray, int, int], None], value:int):
        self.__reserve(count)
        method(self.__data, self.__cursor, value)
        self.__cursor += count
    
    def __write_int2(self, count:int, method:_Callable[[bytearray, int, int, bool], None], value:int, big:bool):
        self.__reserve(count)
        method(self.__data, self.__cursor, value, big)
        self.__cursor += count

    #endregion

    #region methods
    
    def set_cursor(self,\
            position:int,\
            raisedata:bool = False):
        """
        Sets the position of the cursor
        
        :param position:
            New position of the cursor
        :param raisedata:
            If true, an invalid cursor position will be raised as a DataError instead of a ValueError. 
            This may be useful for detecting files with invalid offset data.
        :raise ValueError:
            raisedata == False and the cursor position is invalid
        :raise DataError:
            raisedata == True and the cursor position is invalid
        """
        if position < 0 or position > len(self.__data):
            if raisedata:
                if position < 0:
                    raise _DataError("Offset cannot be below zero.")
                raise _DataError("Offset cannot exceed the length of the data.")
            raise ValueError("Cursor position must be between zero and the current length of the buffer.")
        self.__cursor = position
    
    def read_byte(self):
        """
        Reads a single byte from the buffer and increments the cursor by 1
        
        :return:
            Read value
        :raise DataError:
            Cursor is at the end of the buffer
        """
        if self.__cursor == len(self.__data):
            raise _DataError("Unexpected end of data")
        value = self.__data[self.__cursor]
        self.__cursor += 1
        return value
    
    def write_byte(self,\
            value:int):
        """
        Writes a single byte to the buffer and increments the cursor by 1
        
        :param value:
            Value to write
        """
        if self.__cursor == len(self.__data):
            self.__data.append(value)
        else:
            self.__data[self.__cursor] = value
        self.__cursor += 1

    #region uint8

    def read_uint8(self):
        """
        Reads an 8-bit unsigned integer from the buffer and increments the cursor by 1
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(U8_SIZE, _ByteR.read_uint8)

    def write_uint8(self, value:int):
        """
        Writes an 8-bit unsigned integer to the buffer and increments the cursor by 1
        
        :value: Value to write
        """
        self.__write_int(U8_SIZE, _ByteW.write_uint8, value)

    #endregion

    #region int8

    def read_int8(self):
        """
        Reads an 8-bit signed integer from the buffer and increments the cursor by 1
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(I8_SIZE, _ByteR.read_int8)

    def write_int8(self, value:int):
        """
        Writes an 8-bit signed integer to the buffer and increments the cursor by 1
        
        :value: Value to write
        """
        self.__write_int(I8_SIZE, _ByteW.write_int8, value)

    #endregion

    #region uint16

    def read_uint16(self, big:bool):
        """
        Reads a 16-bit unsigned integer from the buffer and increments the cursor by 2
        
        :param big: Whether or not data is stored in big-endian
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int2(U16_SIZE, _ByteR.read_uint16, big)

    def read_uint16_l(self):
        """
        Reads a little-endian 16-bit unsigned integer from the buffer and increments the cursor by 2
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(U16_SIZE, _ByteR.read_uint16_l)

    def read_uint16_b(self):
        """
        Reads a big-endian 16-bit unsigned integer from the buffer and increments the cursor by 2
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(U16_SIZE, _ByteR.read_uint16_b)

    def write_uint16(self, value:int, big:bool):
        """
        Writes a 16-bit unsigned integer to the buffer and increments the cursor by 2
        
        :param big: Whether or not to store in big-endian
        :value: Value to write
        """
        self.__write_int2(U16_SIZE, _ByteW.write_uint16, value, big)

    def write_uint16_l(self, value:int):
        """
        Writes a little-endian 16-bit unsigned integer to the buffer and increments the cursor by 2
        
        :value: Value to write
        """
        self.__write_int(U16_SIZE, _ByteW.write_uint16_l, value)

    def write_uint16_b(self, value:int):
        """
        Writes a big-endian 16-bit unsigned integer to the buffer and increments the cursor by 2
        
        :value: Value to write
        """
        self.__write_int(U16_SIZE, _ByteW.write_uint16_b, value)

    #endregion

    #region int16

    def read_int16(self, big:bool):
        """
        Reads a 16-bit signed integer from the buffer and increments the cursor by 2
        
        :param big: Whether or not data is stored in big-endian
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int2(I16_SIZE, _ByteR.read_int16, big)

    def read_int16_l(self):
        """
        Reads a little-endian 16-bit signed integer from the buffer and increments the cursor by 2
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(I16_SIZE, _ByteR.read_int16_l)

    def read_int16_b(self):
        """
        Reads a big-endian 16-bit signed integer from the buffer and increments the cursor by 2
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(I16_SIZE, _ByteR.read_int16_b)

    def write_int16(self, value:int, big:bool):
        """
        Writes a 16-bit signed integer to the buffer and increments the cursor by 2
        
        :param big: Whether or not to store in big-endian
        :value: Value to write
        """
        self.__write_int2(I16_SIZE, _ByteW.write_int16, value, big)

    def write_int16_l(self, value:int):
        """
        Writes a little-endian 16-bit signed integer to the buffer and increments the cursor by 2
        
        :value: Value to write
        """
        self.__write_int(I16_SIZE, _ByteW.write_int16_l, value)

    def write_int16_b(self, value:int):
        """
        Writes a big-endian 16-bit signed integer to the buffer and increments the cursor by 2
        
        :value: Value to write
        """
        self.__write_int(I16_SIZE, _ByteW.write_int16_b, value)

    #endregion

    #region uint32

    def read_uint32(self, big:bool):
        """
        Reads a 32-bit unsigned integer from the buffer and increments the cursor by 4
        
        :param big: Whether or not data is stored in big-endian
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int2(U32_SIZE, _ByteR.read_uint32, big)

    def read_uint32_l(self):
        """
        Reads a little-endian 32-bit unsigned integer from the buffer and increments the cursor by 4
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(U32_SIZE, _ByteR.read_uint32_l)

    def read_uint32_b(self):
        """
        Reads a big-endian 32-bit unsigned integer from the buffer and increments the cursor by 4
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(U32_SIZE, _ByteR.read_uint32_b)

    def write_uint32(self, value:int, big:bool):
        """
        Writes a 32-bit unsigned integer to the buffer and increments the cursor by 4
        
        :param big: Whether or not to store in big-endian
        :value: Value to write
        """
        self.__write_int2(U32_SIZE, _ByteW.write_uint32, value, big)

    def write_uint32_l(self, value:int):
        """
        Writes a little-endian 32-bit unsigned integer to the buffer and increments the cursor by 4
        
        :value: Value to write
        """
        self.__write_int(U32_SIZE, _ByteW.write_uint32_l, value)

    def write_uint32_b(self, value:int):
        """
        Writes a big-endian 32-bit unsigned integer to the buffer and increments the cursor by 4
        
        :value: Value to write
        """
        self.__write_int(U32_SIZE, _ByteW.write_uint32_b, value)

    #endregion

    #region int32

    def read_int32(self, big:bool):
        """
        Reads a 32-bit signed integer from the buffer and increments the cursor by 4
        
        :param big: Whether or not data is stored in big-endian
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int2(I32_SIZE, _ByteR.read_int32, big)

    def read_int32_l(self):
        """
        Reads a little-endian 32-bit signed integer from the buffer and increments the cursor by 4
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(I32_SIZE, _ByteR.read_int32_l)

    def read_int32_b(self):
        """
        Reads a big-endian 32-bit signed integer from the buffer and increments the cursor by 4
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(I32_SIZE, _ByteR.read_int32_b)

    def write_int32(self, value:int, big:bool):
        """
        Writes a 32-bit signed integer to the buffer and increments the cursor by 4
        
        :param big: Whether or not to store in big-endian
        :value: Value to write
        """
        self.__write_int2(I32_SIZE, _ByteW.write_int32, value, big)

    def write_int32_l(self, value:int):
        """
        Writes a little-endian 32-bit signed integer to the buffer and increments the cursor by 4
        
        :value: Value to write
        """
        self.__write_int(I32_SIZE, _ByteW.write_int32_l, value)

    def write_int32_b(self, value:int):
        """
        Writes a big-endian 32-bit signed integer to the buffer and increments the cursor by 4
        
        :value: Value to write
        """
        self.__write_int(I32_SIZE, _ByteW.write_int32_b, value)

    #endregion

    #region uint64

    def read_uint64(self, big:bool):
        """
        Reads a 64-bit unsigned integer from the buffer and increments the cursor by 8
        
        :param big: Whether or not data is stored in big-endian
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int2(U64_SIZE, _ByteR.read_uint64, big)

    def read_uint64_l(self):
        """
        Reads a little-endian 64-bit unsigned integer from the buffer and increments the cursor by 8
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(U64_SIZE, _ByteR.read_uint64_l)

    def read_uint64_b(self):
        """
        Reads a big-endian 64-bit unsigned integer from the buffer and increments the cursor by 8
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(U64_SIZE, _ByteR.read_uint64_b)

    def write_uint64(self, value:int, big:bool):
        """
        Writes a 64-bit unsigned integer to the buffer and increments the cursor by 8
        
        :param big: Whether or not to store in big-endian
        :value: Value to write
        """
        self.__write_int2(U64_SIZE, _ByteW.write_uint64, value, big)

    def write_uint64_l(self, value:int):
        """
        Writes a little-endian 64-bit unsigned integer to the buffer and increments the cursor by 8
        
        :value: Value to write
        """
        self.__write_int(U64_SIZE, _ByteW.write_uint64_l, value)

    def write_uint64_b(self, value:int):
        """
        Writes a big-endian 64-bit unsigned integer to the buffer and increments the cursor by 8
        
        :value: Value to write
        """
        self.__write_int(U64_SIZE, _ByteW.write_uint64_b, value)

    #endregion

    #region int64

    def read_int64(self, big:bool):
        """
        Reads a 64-bit signed integer from the buffer and increments the cursor by 8
        
        :param big: Whether or not data is stored in big-endian
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int2(I64_SIZE, _ByteR.read_int64, big)

    def read_int64_l(self):
        """
        Reads a little-endian 64-bit signed integer from the buffer and increments the cursor by 8
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(I64_SIZE, _ByteR.read_int64_l)

    def read_int64_b(self):
        """
        Reads a big-endian 64-bit signed integer from the buffer and increments the cursor by 8
        
        :return: Read value
        :raise DataError: Unexpected end of data
        """
        return self.__read_int(I64_SIZE, _ByteR.read_int64_b)

    def write_int64(self, value:int, big:bool):
        """
        Writes a 64-bit signed integer to the buffer and increments the cursor by 8
        
        :param big: Whether or not to store in big-endian
        :value: Value to write
        """
        self.__write_int2(I64_SIZE, _ByteW.write_int64, value, big)

    def write_int64_l(self, value:int):
        """
        Writes a little-endian 64-bit signed integer to the buffer and increments the cursor by 8
        
        :value: Value to write
        """
        self.__write_int(I64_SIZE, _ByteW.write_int64_l, value)

    def write_int64_b(self, value:int):
        """
        Writes a big-endian 64-bit signed integer to the buffer and increments the cursor by 8
        
        :value: Value to write
        """
        self.__write_int(I64_SIZE, _ByteW.write_int64_b, value)

    #endregion

    #endregion