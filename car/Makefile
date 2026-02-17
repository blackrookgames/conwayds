ifeq ($(strip $(DEVKITARM)),)
$(error "Please set DEVKITARM in your environment. export DEVKITARM=<path to>devkitARM")
endif

MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MKFILE_DIR := $(dir $(MKFILE_PATH))

GPPDIR := $(DEVKITARM)/bin

GPP := $(GPPDIR)/arm-none-eabi-g++
GNM := $(GPPDIR)/arm-none-eabi-gcc-nm
NDSTOOL := $(DEVKITARM)/../tools/bin/ndstool
CALICO := $(DEVKITARM)/../calico
LIBNDS := $(DEVKITARM)/../libnds

BINDIR := $(MKFILE_DIR)bin
OBJDIR := $(MKFILE_DIR)obj
HDRDIR := $(MKFILE_DIR)hdr
SRCDIR := $(MKFILE_DIR)src

EXENAME := car
EXEPATH := $(BINDIR)/$(EXENAME).nds
ELFPATH := $(BINDIR)/$(EXENAME).elf
MAPPATH := $(BINDIR)/$(EXENAME).map
LSTPATH := $(BINDIR)/$(EXENAME).lst

SRCPATHS := main.cpp Palette.cpp\
	Car00.cpp Car01.cpp Car02.cpp Car03.cpp Car04.cpp Car05.cpp Car06.cpp Car07.cpp Car08.cpp Car09.cpp\
	Car10.cpp Car11.cpp Car12.cpp Car13.cpp Car14.cpp Car15.cpp Car16.cpp Car17.cpp Car18.cpp Car19.cpp\
	Car20.cpp Car21.cpp Car22.cpp Car23.cpp Car24.cpp Car25.cpp Car26.cpp Car27.cpp Car28.cpp Car29.cpp\
	Car30.cpp Car31.cpp Car32.cpp Car33.cpp Car34.cpp Car35.cpp Car36.cpp Car37.cpp

OBJPATHS := $(foreach path,$(notdir $(SRCPATHS)),$(OBJDIR)/$(path:.cpp=.o))

all : $(EXEPATH)

$(EXEPATH) : $(OBJPATHS)
	@mkdir -p "$$(dirname $@)"
	$(GPP) \
		-L$(CALICO)/lib -L$(LIBNDS)/lib \
		-specs=$(CALICO)/share/ds9.specs \
		-g -march=armv5te -mtune=arm946e-s -mthumb \
		-Wl,-Map,$(MAPPATH) \
		$(OBJPATHS) \
		-lnds9 -lcalico_ds9 \
		-o $(ELFPATH)
	$(GNM) \
		-CSn $(ELFPATH) > $(LSTPATH)
	@$(NDSTOOL) \
		-c $(EXEPATH)  \
		-9 $(ELFPATH) \
		-7 $(CALICO)/bin/ds7_maine.elf \
		-b $(CALICO)/share/nds-icon.bmp \
		"app;built with devkitARM;http://devkitpro.org" \
		> /dev/null

$(OBJDIR)/%.o : $(SRCDIR)/%.cpp
	@mkdir -p "$$(dirname $@)"
	$(GPP) \
		-MMD -MP -MF $(@:.o=.d) \
		-D__NDS__ \
		-I$(CALICO)/include \
		-g -Wall -O2 -ffunction-sections -fdata-sections \
		-march=armv5te -mtune=arm946e-s -mthumb \
		-I$(HDRDIR) \
		-I$(BINDIR) \
		-I$(LIBNDS)/include \
		-I$(BINDIR) \
		-DARM9 \
		-fno-rtti -fno-exceptions \
		-c $< -o $@

clean:
	@if [ -d $(BINDIR) ]; then rm -r $(BINDIR); fi
	@if [ -d $(OBJDIR) ]; then rm -r $(OBJDIR); fi