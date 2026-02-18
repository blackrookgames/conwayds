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

EXENAME := conway
EXEPATH := $(BINDIR)/$(EXENAME).nds
ELFPATH := $(BINDIR)/$(EXENAME).elf
MAPPATH := $(BINDIR)/$(EXENAME).map
LSTPATH := $(BINDIR)/$(EXENAME).lst

SRCPATHS := main.cpp Assets.cpp StartPattern.cpp

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