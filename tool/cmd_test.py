import sys

from enum import\
    auto as _auto,\
    Enum as _Enum

import src.cli as _cli

class DayOfWeek(_Enum):
    SUNDAY = _auto()
    MONDAY = _auto()
    TUESDAY = _auto()
    WEDNESDAY = _auto()
    THURSDAY = _auto()
    FRIDAY = _auto()
    SATURDAY = _auto()

class cmd_test(_cli.CLICommand):

    @property
    def _desc(self) -> None|str:
        return "This is a command description."

    #region required

    __string = _cli.CLIRequiredDef(\
        name = "string",\
        desc = "String")
    __number = _cli.CLIRequiredDef(\
        name = "number",\
        desc = "Number",\
        parse = _cli.CLIParseUtil.to_int)

    #endregion

    #region optional

    __day = _cli.CLIOptionWArgDef(\
        name = "day",\
        short = 'd',\
        desc = "Day of the week",\
        parse = _cli.CLIParseUtil.to_enum,\
        arg = (DayOfWeek, True, ),\
        default = None)
    __u8 = _cli.CLIOptionWArgDef(\
        name = "u8",\
        short = 'B',\
        desc = "8-bit unsigned integer",\
        parse = _cli.CLIParseUtil.to_uint8,\
        default = 0)
    __i8 = _cli.CLIOptionWArgDef(\
        name = "i8",\
        short = 'b',\
        desc = "8-bit signed integer",\
        parse = _cli.CLIParseUtil.to_int8,\
        default = 0)
    __u16 = _cli.CLIOptionWArgDef(\
        name = "u16",\
        short = 'S',\
        desc = "16-bit unsigned integer",\
        parse = _cli.CLIParseUtil.to_uint16,\
        default = 0)
    __i16 = _cli.CLIOptionWArgDef(\
        name = "i16",\
        short = 's',\
        desc = "16-bit signed integer",\
        parse = _cli.CLIParseUtil.to_int16,\
        default = 0)
    __u32 = _cli.CLIOptionWArgDef(\
        name = "u32",\
        short = 'I',\
        desc = "32-bit unsigned integer",\
        parse = _cli.CLIParseUtil.to_uint32,\
        default = 0)
    __i32 = _cli.CLIOptionWArgDef(\
        name = "i32",\
        short = 'i',\
        desc = "32-bit signed integer",\
        parse = _cli.CLIParseUtil.to_int32,\
        default = 0)
    __u64 = _cli.CLIOptionWArgDef(\
        name = "u64",\
        short = 'L',\
        desc = "64-bit unsigned integer",\
        parse = _cli.CLIParseUtil.to_uint64,\
        default = 0)
    __i64 = _cli.CLIOptionWArgDef(\
        name = "i64",\
        short = 'l',\
        desc = "64-bit signed integer",\
        parse = _cli.CLIParseUtil.to_int64,\
        default = 0)
    __f = _cli.CLIOptionWArgDef(\
        name = "float",\
        short = 'f',\
        desc = "Floating-point decimal",\
        parse = _cli.CLIParseUtil.to_float,\
        default = 0)

    #endregion

    #region methods

    def _main(self):
        print(f"day   {self.day}")
        print(f"string   {self.string}")
        print(f"number   {self.number}")
        print(f"u8       {self.u8}")
        print(f"i8       {self.i8}")
        print(f"u16      {self.u16}")
        print(f"i16      {self.i16}")
        print(f"u32      {self.u32}")
        print(f"i32      {self.i32}")
        print(f"u64      {self.u64}")
        print(f"i64      {self.i64}")
        print(f"float    {self.float}")

        return 0

    #endregion

if __name__ == '__main__':
    sys.exit(cmd_test().execute(sys.argv))