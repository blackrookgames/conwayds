shdir="$(dirname $(realpath $BASH_SOURCE))"
pydir="$(dirname $shdir)/src"
srcdir="$pydir/cpp/_cf/c_loads"
srcpath="$srcdir/__init__.py"

PREFIX=c_load_
PREFIX_LEN="${#PREFIX}"

# Get "sub-commands"
declare -a subcmds=()
for path in $srcdir/*; do
    # Check name
    name="$(basename $path)"
    name="${name%.*}"
    name_len="${#name}"
    if [ $name_len -lt $PREFIX_LEN ]; then continue; fi
    if [ ! "${name:0:$PREFIX_LEN}" = "$PREFIX" ]; then continue; fi
    # Add sub-command
    subcmds+=("${name:$PREFIX_LEN}")
done

# Delete file (we are going to recreate it)
if [ -f "$srcpath" ]; then rm "$srcpath"; fi

# Write to file
echo "from typing import Callable as _Callable" >>"$srcpath"
echo "from .c__HCmdLoad import _HCmdLoad" >>"$srcpath"
for name in "${subcmds[@]}"; do
    echo "from .$PREFIX$name import _create as _create_$name" >>"$srcpath"
done
# Create dictionary
echo "# Sub-commands" >>"$srcpath"
echo "__DICT:dict[str, _Callable[[], _HCmdLoad]] = {" >>"$srcpath"
echo "    '$name': _create_$name," >>"$srcpath"
echo "}" >>"$srcpath"
