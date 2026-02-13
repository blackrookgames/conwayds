input_name=$1

shdir="$(dirname $(realpath $BASH_SOURCE))"
pydir="$(dirname $shdir)/src"
srcdir="$pydir/cpp/_cf/c_${input_name}s"
srcpath="$srcdir/__init__.py"

prefix="c_${input_name}_"
prefix_len="${#prefix}"

# Get "sub-commands"
declare -a subcmds=()
for path in $srcdir/*; do
    # Check name
    name="$(basename $path)"
    name="${name%.*}"
    name_len="${#name}"
    if [ $name_len -lt $prefix_len ]; then continue; fi
    if [[ $name_len -gt $prefix_len && "${name:$prefix_len:1}" = "_" ]]; then continue; fi
    if [ ! "${name:0:$prefix_len}" = "$prefix" ]; then continue; fi
    # Add sub-command
    subcmds+=("${name:$prefix_len}")
done

# Delete file (we are going to recreate it)
if [ -f "$srcpath" ]; then rm "$srcpath"; fi

# Write to file
echo "from typing import Callable as _Callable" >>"$srcpath"
echo "from ..c__HCmdConvert import _HCmdConvert" >>"$srcpath"
for name in "${subcmds[@]}"; do
    echo "from .$prefix$name import _create as _create_$name, _type as _type_$name" >>"$srcpath"
done
# Create dictionary
echo "# Sub-commands" >>"$srcpath"
echo "__DICT:dict[type, _Callable[[object, str], _HCmdConvert]] = {" >>"$srcpath"
for name in "${subcmds[@]}"; do
    echo "    _type_$name.__value__: _create_$name," >>"$srcpath"
done
echo "}" >>"$srcpath"
