all = []

from sys import\
    stderr as _stderr

from ....cli.mod_CLIParseUtil import\
    CLIParseUtil as _CLIParseUtil

def __tobpp(input:str):
    passs, value = _CLIParseUtil.to_int(input)
    if not passs: return False, 0
    if value != 4 and value != 8:
        print(f"{value} is not valid for the bits-per-pixel.", file = _stderr)
        return False, 0
    return True, value