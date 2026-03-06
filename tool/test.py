import sys

from pathlib import Path

import src.cliutil as cliutil

path0 = Path(sys.argv[0]).parent.joinpath("test0.bin")
path1 = Path(sys.argv[0]).parent.joinpath("test1.bin")

l = cliutil.CLIListUtil.int64_from_file(str(path0))
cliutil.CLIListUtil.int64_to_file(l, str(path1))