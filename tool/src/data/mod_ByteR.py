__all__ = [\
    'ByteR']

from ..helper.mod_ErrorUtil import\
    ErrorUtil as _ErrorUtil

class ByteR:
    """
    Utility for reading byte data
    """

    #region helper methods
    
    @classmethod
    def __read_l(cls, array:bytearray, start:int, count:int):
        end = start + count
        if start < 0 or end > len(array):
            raise IndexError("start is out of range.")
        # Read
        value = 0
        while end > start:
            end -= 1
            value <<= 8
            value |= array[end]
        # Return
        return value
    
    @classmethod
    def __read_b(cls, array:bytearray, start:int, count:int):
        end = start + count
        if start < 0 or end > len(array):
            raise IndexError("start is out of range.")
        # Read
        value = 0
        while start < end:
            value <<= 8
            value |= array[start]
            start += 1
        # Return
        return value
    
    @classmethod
    def __read_neg(cls, value:int, mask:int):
        if (value & mask) == 0:
            return value
        return (value & (~mask)) - mask
        
    #endregion

    #region methods
    
    @classmethod
    def read_uint8(cls, array:bytearray, index:int):
        """
        Reads an 8-bit unsigned integer from a byte array

        :param array: Byte array
        :param index: Index of value to read
        :return: Read value
        :raise IndexError: index is out of range
        """
        if index < 0 or index >= len(array):
            raise IndexError("index is out of range.")
        return array[index]
    
    @classmethod
    def read_int8(cls, array:bytearray, index:int):
        """
        Reads an 8-bit signed integer from a byte array

        :param array: Byte array
        :param index: Index of value to read
        :return: Read value
        :raise IndexError: index is out of range
        """
        if index < 0 or index >= len(array):
            raise IndexError("index is out of range.")
        return cls.__read_neg(array[index], 0x80)
    
    @classmethod
    def read_uint16(cls, array:bytearray, start:int, big:bool):
        """
        Reads a little-endian 16-bit unsigned integer from a byte array

        :param array: Byte array
        :param start: Starting index
        :param big: Whether or not data is stored in big-endian
        :return: Read value
        :raise IndexError: start is out of range
        """
        if big: return cls.read_uint16_b(array, start)
        return cls.read_uint16_l(array, start)
    
    @classmethod
    def read_uint16_l(cls, array:bytearray, start:int):
        """
        Reads a little-endian 16-bit unsigned integer from a byte array

        :param array: Byte array
        :param start: Starting index
        :return: Read value
        :raise IndexError: start is out of range
        """
        return cls.__read_l(array, start, 2)
    
    @classmethod
    def read_uint16_b(cls, array:bytearray, start:int):
        """
        Reads a big-endian 16-bit unsigned integer from a byte array

        :param array: Byte array
        :param start: Starting index
        :return: Read value
        :raise IndexError: start is out of range
        """
        return cls.__read_b(array, start, 2)

    #endregion