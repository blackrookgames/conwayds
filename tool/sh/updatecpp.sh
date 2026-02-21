shpath="$(realpath $BASH_SOURCE)"
bash "$shpath.call.sh"
bash "$shpath.hcmdconvert.sh" databuffer
bash "$shpath.hcmdconvert.sh" dsbitmap
bash "$shpath.hcmdconvert.sh" dspalette
bash "$shpath.hcmdconvert.sh" dstileset
bash "$shpath.hcmdconvert.sh" imgimage
bash "$shpath.hcmdconvert.sh" lifepattern
bash "$shpath.hcmdconvert.sh" string
bash "$shpath.loads.sh"
bash "$shpath.saves.sh"