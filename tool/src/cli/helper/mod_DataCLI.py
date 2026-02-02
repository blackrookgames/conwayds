__all__ = [\
    'DataCLI',]

from sys import\
    stderr as _stderr

from ...data.mod_DataBuffer import\
    DataBuffer as _DataBuffer

class DataCLI:
    """
    CLI-utility for data operations
    """

    #region buffer

    @classmethod
    def buffer_load(cls, path:str):
        """
        Attempts to create a DataBuffer by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created DataBuffer (or None if load failed)
        """
        # Read bytes from file 
        try:
            with open(path, 'rb') as input:
                bytes = input.read()
        except Exception as e:
            print(f"ERROR: {e}", file = _stderr)
            return None
        # Create buffer
        buffer = _DataBuffer(len(bytes))
        for i in range(len(bytes)):
            buffer[i] = bytes[i]
        return buffer

    @classmethod
    def buffer_save(cls, buffer:_DataBuffer, path:str):
        """
        Attempts to save a DataBuffer to a file
        
        :param buffer:
            DataBuffer to save
        :param path:
            Path of output file
        :return:
            Whether or not successful
        """
        try: 
            with open(path, 'wb') as output:
                output.write(bytes(buffer))
            return True
        except Exception as e:
            print(f"ERROR: {e}", file = _stderr)
            return False

    @classmethod
    def buffer_cpp(cls, buffer:_DataBuffer, path_cpp:str, path_hdr:None|str = None):
        """
        Attempts to export a DataBuffer to a C++ source
        
        :param buffer:
            DataBuffer to save
        :param path_cpp:
            Path of C++ file
        :param path_hdr:
            Path of C++ header file
        :return:
            Whether or not successful
        """
        # TODO: Add code
        print("TODO: Add code")
        return False

    #endregion