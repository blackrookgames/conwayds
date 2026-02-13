shpath="$(realpath $BASH_SOURCE)"
bash "$shpath.call.sh"
bash "$shpath.hcmdconvert.sh" databuffer
bash "$shpath.hcmdconvert.sh" dspalette
bash "$shpath.hcmdconvert.sh" dstileset
bash "$shpath.hcmdconvert.sh" imgimage
bash "$shpath.loads.sh"
bash "$shpath.saves.sh"