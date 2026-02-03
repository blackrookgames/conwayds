__all__ = [\
    'CLIDataUtil',]

from io import\
    StringIO as _StringIO
from pathlib import\
    Path as _Path

from ..data.mod_DataBuffer import\
    DataBuffer as _DataBuffer
from .mod_CLICommandError import\
    CLICommandError as _CLICommandError
from .mod_CLIStrUtil import\
    CLIStrUtil as _CLIStrUtil

class CLIDataUtil:
    """
    CLI-utility for data operations
    """

    #region buffer

    @classmethod
    def buffer_from_file(cls, path:str):
        """
        Creates a DataBuffer by loading from a file
        
        :param path:
            Path of input file
        :return:
            Created DataBuffer
        :raise CLICommandError:
            An error occurred
        """
        try:
            # Open file
            with open(path, 'rb') as input:
                raw = input.read()
            # Create buffer
            buffer = _DataBuffer(len(raw))
            for i in range(len(raw)):
                buffer[i] = raw[i]
            # Success!!!
            return buffer
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    @classmethod
    def buffer_to_file(cls, buffer:_DataBuffer, path:str):
        """
        Saves a DataBuffer to a file
        
        :param path:
            Path of output file
        :param buffer:
            DataBuffer to save
        :raise CLICommandError:
            An error occurred
        """
        try: 
            with open(path, 'wb') as output:
                output.write(bytes(buffer))
            return
        except Exception as e:
            error = _CLICommandError(e)
        raise error

    @classmethod
    def buffer_to_cpp(cls, buffer:_DataBuffer, path_hdr:str, path_cpp:str, classname:str,\
            defname:None|str = None):
        """
        Exports a DataBuffer to a C++ source
        
        :param buffer:
            DataBuffer to save
        :param path_hdr:
            Path of C++ header file
        :param path_cpp:
            Path of C++ file
        :param classname:
            Name of C++ class
        :param defname:
            DEF name
        :raise CLICommandError:
            An error occurred
        """
        # Write header
        with _StringIO() as _hdr:
            # DEF header
            if defname is not None:
                _hdr.write(f"#ifndef {defname}\n")
                _hdr.write(f"#define {defname}\n")
                _hdr.write('\n')
            # Write include
            _hdr.write("#include <nds.h>\n")
            _hdr.write('\n')
            # Write class header
            _hdr.write(f"class {classname}\n")
            _hdr.write("{\n")
            _hdr.write("    public:\n")
            # size
            _hdr.write("    static const size_t size;\n")
            # data
            _hdr.write(f"    static const u8 data[];\n")
            # Write class footer
            _hdr.write("};\n")
            # DEF footer
            if defname is not None:
                _hdr.write('\n')
                _hdr.write("#endif\n")
            # Write to file
            _CLIStrUtil.str_to_file(_hdr.getvalue(), path_hdr)
        # Write C++
        with _StringIO() as _cpp:
            # Write include
            _cpp.write(f"#include \"{_Path(path_hdr).name}\"\n")
            _cpp.write('\n')
            # size
            _cpp.write(f"const size_t {classname}::size = {len(buffer)};\n")
            _cpp.write("\n")
            # data
            _cpp.write(f"const u8 {classname}::data[] = \n")
            _cpp.write("{")
            for _i in range(len(buffer)):
                if (_i % 16) == 0: _cpp.write("\n    ")
                _cpp.write(f"0x{buffer[_i]:02X}, ")
            _cpp.write("\n")
            _cpp.write("};\n")
            # Write to file
            _CLIStrUtil.str_to_file(_cpp.getvalue(), path_cpp)
        

    #endregion