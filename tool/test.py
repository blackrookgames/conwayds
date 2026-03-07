import sys

from pathlib import Path

import src.cliutil as cliutil

path0 = Path(sys.argv[0]).parent.joinpath("test0.bin")
path1 = Path(sys.argv[0]).parent.joinpath("test1.bin")

l = cliutil.CLIRLEUtil.uint8_from_file(str(path0))

for _item in l:
    print(f"0x{_item:02X} ", end = '')
print()

cliutil.CLIRLEUtil.uint8_to_file(l, str(path1))