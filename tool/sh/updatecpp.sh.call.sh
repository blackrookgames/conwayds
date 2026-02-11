shdir="$(dirname $(realpath $BASH_SOURCE))"
pydir="$(dirname $shdir)/src"
cppdir="$pydir/cpp"

srcpath="$cppdir/mod_run.py"

MODULE=_cf
TYPE_NONE=0
TYPE_CMD=1
TYPE_FUNC=2

extract() {
    local _name=$1
    local _type=$2
    local _outname=$3
    # Default
    eval "$_type=$TYPE_NONE"
    eval "$_outname="
    # Get length
    local _len="${#_name}"
    # Check underscores (must be c_ or f_; not c__ or f__)
    if [ $_len -lt 2 ]; then
        return
    fi
    if [ ! "${_name:1:1}" = "_"  ]; then
        return
    fi
    if [[ $_len -ge 3 && "${_name:2:1}" == "_" ]]; then
        return
    fi
    eval "$_outname=${_name:2}"
    # Check first character
    case "${_name:0:1}" in
        # Command
        c)
            eval "$_type=$TYPE_CMD"
            ;;
        # Function
        f)
            eval "$_type=$TYPE_FUNC"
            ;;
    esac
}

# Get commands and functions
declare -a cmds=()
declare -a funcs=()
for path in $cppdir/$MODULE/*; do
    # Make sure path is a file
    if [ ! -f "$path" ]; then continue; fi
    # Extract name
    name="$(basename $path)"
    extract "${name%.*}" type name
    case "$type" in
        # Command
        "$TYPE_CMD")
            cmds+=("$name")
            ;;
        # Function
        "$TYPE_FUNC")
            funcs+=("$name")
            ;;
    esac
done

# Delete file (we are going to recreate it)
if [ -f "$srcpath" ]; then rm "$srcpath"; fi

# Write to file
echo "all = ['run']" >>"$srcpath"
# Write imports
echo "from .mod__Creator import _Creator" >>"$srcpath"
echo "from .mod__call import _CmdDef, _FuncDef" >>"$srcpath"
for name in "${cmds[@]}"; do
    echo "from .$MODULE.c_$name import __def as _c_$name" >>"$srcpath"
done
for name in "${funcs[@]}"; do
    echo "from .$MODULE.f_$name import __def as _f_$name" >>"$srcpath"
done
# Create command dictionary
echo "# Commands" >>"$srcpath"
echo "_CMDS:dict[str, _CmdDef] = {" >>"$srcpath"
for name in "${cmds[@]}"; do
    echo "    '@$name': _c_$name," >>"$srcpath"
done
echo "}" >>"$srcpath"
# Create function dictionary
echo "# Functions" >>"$srcpath"
echo "_FUNCS:dict[str, _FuncDef] = {" >>"$srcpath"
for name in "${funcs[@]}"; do
    echo "    '$name': _f_$name," >>"$srcpath"
done
echo "}" >>"$srcpath"
# Create run
echo "# Run" >>"$srcpath"
echo "def run(fpath:str, dpath:str):" >>"$srcpath"
echo "    \"\"\"" >>"$srcpath"
echo "    Creates C++ sources." >>"$srcpath"
echo "    " >>"$srcpath"
echo "    :param fpath:" >>"$srcpath"
echo "        Path of configuration file" >>"$srcpath"
echo "    :param dpath:" >>"$srcpath"
echo "        Path of working directory" >>"$srcpath"
echo "    :raise CLICommandError:" >>"$srcpath"
echo "        An error occurred" >>"$srcpath"
echo "    \"\"\"" >>"$srcpath"
echo "    _Creator.run(fpath, dpath, _CMDS, _FUNCS)" >>"$srcpath"