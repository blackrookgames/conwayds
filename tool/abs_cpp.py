import sys

from enum import\
    Enum as _Enum
from io import\
    StringIO as _StringIO

import src.cli as cli
import src.data as data

class abs_cpp(cli.CLICommand):

    #region helper methods

    @classmethod
    def __error_cppinput(cls):
        return "ERROR: Cannot accept C++ source code as input."
    
    @classmethod
    def __itype_parse(cls,\
            input:str,\
            arg:tuple[type[_Enum], bool, _Enum]):
        # Parse as enum
        _s, _r = cli.CLIParseUtil.to_enum(input, (arg[0], arg[1]))
        if not _s: return False, None
        # Make sure C++ is not specified
        if _r == arg[2]:
            print(cls.__error_cppinput(), file = sys.stderr)
            return False, None
        # Success!!!
        return True, _r

    @classmethod
    def __getexclude(cls,\
            formats:type[_Enum],\
            exclude):
        for format in formats:
            if format.name != exclude:
                continue
            return format
        return None

    @classmethod
    def __makedesc(cls,\
            prefix:str,\
            formats:type[_Enum],\
            suffix:str,\
            exclude:None|_Enum,\
            ignorecase:bool):
        with _StringIO() as strio:
            # prefix
            strio.write(prefix)
            # formats
            first = True
            for format in formats:
                if format != exclude:
                    # Comma
                    if first: first = False
                    else: strio.write(", ")
                    # Value
                    if ignorecase: strio.write(format.name.lower())
                    else: strio.write(format.name)
            # suffix
            strio.write(suffix)
            # Return
            return strio.getvalue()
    
    @classmethod
    def _input(cls,\
            name:str = "input",\
            desc:None|str = "Path to the input file"):
        return cli.CLIRequiredDef(\
            name = name,\
            desc = desc)
    
    @classmethod
    def _output(cls,\
            name:str = "output",\
            desc:None|str = "Path to the output file"):
        return cli.CLIRequiredDef(\
            name = name,\
            desc = desc)

    @classmethod
    def _header(cls,\
            name:str = "header",\
            short:None|str = 'h',\
            desc:None|str = "Path to output header file; this is unused if output type is not cpp"):
        return cli.CLIOptionWArgDef(\
            name = name,\
            short = short,\
            desc = desc,\
            default = None)

    @classmethod
    def _itype(cls,\
            formats:type[_Enum],\
            name:str = "itype",\
            short:None|str = 'i',\
            desc:None|str = None,\
            ignorecase:bool = True,\
            cpp = 'CPP'):
        exclude = cls.__getexclude(formats, cpp)
        if desc is None:
            desc = cls.__makedesc("Input type. Allowed values: ", formats, "", exclude, ignorecase)
        return cli.CLIOptionWArgDef(\
            name = name,\
            short = short,\
            desc = desc,\
            parse = cls.__itype_parse,\
            arg = (formats, ignorecase, exclude),\
            default = None)
    
    @classmethod
    def _otype(cls,\
            formats:type[_Enum],\
            name:str = "otype",\
            short:None|str = 'o',\
            desc:None|str = None,\
            ignorecase:bool = True):
        if desc is None:
            desc = cls.__makedesc("Output type. Allowed values: ", formats, "", None, ignorecase)
        return cli.CLIOptionWArgDef(\
            name = name,\
            short = short,\
            desc = desc,\
            parse = cli.CLIParseUtil.to_enum,\
            arg = (formats, ignorecase),\
            default = None)

    @classmethod
    def _cppinput(cls,\
            path:str):
        if path.endswith(".cpp"):
            print(cls.__error_cppinput(), file = sys.stderr)
            return True
        return False

    #endregion