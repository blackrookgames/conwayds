all = []

from sys import\
    stderr as _stderr

from ....cli.mod_CLIParseUtil import\
    CLIParseUtil as _CLIParseUtil

def _tobpp(input:str):
    passs, value = _CLIParseUtil.to_int(input)
    if not passs: return False, 0
    if value != 8 and value != 16:
        print(f"{value} is not valid for the bits-per-pixel.", file = _stderr)
        return False, 0
    return True, value