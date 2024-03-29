# Sprinter Arduino Project Makefile
# 
# Makefile Based on:
# Arduino 0011 Makefile
# Arduino adaptation by mellis, eighthave, oli.keller
#
# This has been tested with Arduino 0022.
# 
# This makefile allows you to build sketches from the command line
# without the Arduino environment (or Java).
#
# Detailed instructions for using the makefile:
#
#  1. Modify the line containg "INSTALL_DIR" to point to the directory that
#     contains the Arduino installation (for example, under Mac OS X, this
#     might be /Applications/arduino-0012).
#
#  2. Modify the line containing "PORT" to refer to the filename
#     representing the USB or serial connection to your Arduino board
#     (e.g. PORT = /dev/tty.USB0).  If the exact name of this file
#     changes, you can use * as a wildcard (e.g. PORT = /dev/tty.usb*).
#
#  3. Set the line containing "MCU" to match your board's processor. 
#     Older one's are atmega8 based, newer ones like Arduino Mini, Bluetooth
#     or Diecimila have the atmega168.  If you're using a LilyPad Arduino,
#     change F_CPU to 8000000. If you are using Gen7 electronics, you
#     probably need to use 20000000. Either way, you must regenerate
#     the speed lookup table with create_speed_lookuptable.py.
#
#  4. Type "make" and press enter to compile/verify your program.
#
#  5. Type "make upload", reset your Arduino board, and press enter to
#     upload your program to the Arduino board.
#
# $Id$

#For "old" Arduino Mega
#MCU = atmega1280
#For Arduino Mega2560
#MCU = atmega2560
#For Sanguinololu
#MCU = atmega644p 
MCU = atmega1284p
#For Printrboard
#MCU = at90usb1286 


#Arduino install directory
INSTALL_DIR = /home/user-1/Documents/arduino-1.8.7

# Be sure to regenerate speed_lookuptable.h with create_speed_lookuptable.py
# if you are setting this to something other than 16MHz
F_CPU = 16000000

UPLOAD_RATE = 115200
AVRDUDE_PROGRAMMER = arduino
PORT = /dev/ttyUSB0

TARGET = $(notdir $(CURDIR))


############################################################################
# Below here nothing should be changed...

ARDUINO = $(INSTALL_DIR)/hardware/arduino/avr/cores/arduino
AVR_TOOLS_PATH = 
SRC =  $(ARDUINO)/pins_arduino.c $(ARDUINO)/wiring.c \
	$(ARDUINO)/wiring_analog.c $(ARDUINO)/wiring_digital.c \
	$(ARDUINO)/wiring_pulse.c \
	$(ARDUINO)/wiring_shift.c $(ARDUINO)/WInterrupts.c
CXXSRC = $(ARDUINO)/WMath.cpp $(ARDUINO)/WString.cpp\
	$(ARDUINO)/Print.cpp applet/Marlin.cpp MarlinSerial.cpp Sd2Card.cpp SdBaseFile.cpp SdFatUtil.cpp SdFile.cpp SdVolume.cpp motion_control.cpp planner.cpp stepper.cpp temperature.cpp cardreader.cpp MatrixMath.cpp FPUTransform.cpp z_probe.cpp
	
FORMAT = ihex


# Name of this Makefile (used for "make depend").
MAKEFILE = Makefile

# Debugging format.
# Native formats for AVR-GCC's -g are stabs [default], or dwarf-2.
# AVR (extended) COFF requires stabs, plus an avr-objcopy run.
DEBUG = stabs

OPT = s

# Place -D or -U options here
CDEFS = -DF_CPU=$(F_CPU)
CXXDEFS = -DF_CPU=$(F_CPU)

# Place -I options here
CINCS = -I$(ARDUINO)
CXXINCS = -I$(ARDUINO)

# Compiler flag to set the C Standard level.
# c89   - "ANSI" C
# gnu89 - c89 plus GCC extensions
# c99   - ISO C99 standard (not yet fully implemented)
# gnu99 - c99 plus GCC extensions
#CSTANDARD = -std=gnu99
CDEBUG = -g$(DEBUG)
CWARN = -Wall -Wstrict-prototypes
CTUNING = -funsigned-char -funsigned-bitfields -fpack-struct -fshort-enums -w -ffunction-sections -fdata-sections -DARDUINO=22
#CEXTRA = -Wa,-adhlns=$(<:.c=.lst)

CFLAGS = $(CDEBUG) $(CDEFS) $(CINCS) -O$(OPT) $(CWARN) $(CEXTRA) $(CTUNING)
CXXFLAGS =         $(CDEFS) $(CINCS) -O$(OPT) -Wall    $(CEXTRA) $(CTUNING)
#ASFLAGS = -Wa,-adhlns=$(<:.S=.lst),-gstabs 
LDFLAGS = -lm


# Programming support using avrdude. Settings and variables.
AVRDUDE_PORT = $(PORT)
AVRDUDE_WRITE_FLASH = -U flash:w:applet/$(TARGET).hex:i
AVRDUDE_FLAGS = -D -C $(INSTALL_DIR)/hardware/tools/avrdude.conf \
	-p $(MCU) -P $(AVRDUDE_PORT) -c $(AVRDUDE_PROGRAMMER) \
	-b $(UPLOAD_RATE)

# Program settings
CC = $(AVR_TOOLS_PATH)avr-gcc
CXX = $(AVR_TOOLS_PATH)avr-g++
OBJCOPY = $(AVR_TOOLS_PATH)avr-objcopy
OBJDUMP = $(AVR_TOOLS_PATH)avr-objdump
AR  = $(AVR_TOOLS_PATH)avr-ar
SIZE = $(AVR_TOOLS_PATH)avr-size
NM = $(AVR_TOOLS_PATH)avr-nm
AVRDUDE = avrdude
REMOVE = rm -f
MV = mv -f

# Define all object files.
OBJ = $(SRC:.c=.o) $(CXXSRC:.cpp=.o) $(ASRC:.S=.o) 

# Define all listing files.
LST = $(ASRC:.S=.lst) $(CXXSRC:.cpp=.lst) $(SRC:.c=.lst)

# Combine all necessary flags and optional flags.
# Add target processor to flags.
ALL_CFLAGS = -mmcu=$(MCU) -I. $(CFLAGS)
ALL_CXXFLAGS = -mmcu=$(MCU) -I. $(CXXFLAGS)
ALL_ASFLAGS = -mmcu=$(MCU) -I. -x assembler-with-cpp $(ASFLAGS)


# Default target.
all: build sizeafter

build: elf hex 

applet/$(TARGET).cpp:# $(TARGET).pde $(MAKEFILE)

applet/%.cpp: %.pde
# Here is the "preprocessing".
# It creates a .cpp file based with the same name as the .pde file.
# On top of the new .cpp file comes the WProgram.h header.
# At the end there is a generic main() function attached.
# Then the .cpp file will be compiled. Errors during compile will
# refer to this new, automatically generated, file. 
# Not the original .pde file you actually edit...
	@echo "  WR    $@"
	@test -d $(dir $@) || mkdir $(dir $@)
	@echo '#include "WProgram.h"' > $@
	@cat $< >> $@
	@cat $(ARDUINO)/main.cpp >> $@

elf: applet/$(TARGET).elf
hex: applet/$(TARGET).hex
eep: applet/$(TARGET).eep
lss: applet/$(TARGET).lss 
sym: applet/$(TARGET).sym

# Program the device.  
upload: applet/$(TARGET).hex
	stty hup < $(PORT); true
	$(AVRDUDE) $(AVRDUDE_FLAGS) $(AVRDUDE_WRITE_FLASH)
	stty -hup < $(PORT); true


	# Display size of file.
HEXSIZE = $(SIZE) --target=$(FORMAT) applet/$(TARGET).hex
ELFSIZE = $(SIZE)  applet/$(TARGET).elf
sizebefore:
	@if [ -f applet/$(TARGET).elf ]; then echo; echo $(MSG_SIZE_BEFORE); $(HEXSIZE); echo; fi

sizeafter:
	@if [ -f applet/$(TARGET).elf ]; then echo; echo $(MSG_SIZE_AFTER); $(ELFSIZE); echo; fi


# Convert ELF to COFF for use in debugging / simulating in AVR Studio or VMLAB.
COFFCONVERT=$(OBJCOPY) --debugging \
	--change-section-address .data-0x800000 \
	--change-section-address .bss-0x800000 \
	--change-section-address .noinit-0x800000 \
	--change-section-address .eeprom-0x810000 


coff: applet/$(TARGET).elf
	$(COFFCONVERT) -O coff-avr applet/$(TARGET).elf $(TARGET).cof


extcoff: $(TARGET).elf
	$(COFFCONVERT) -O coff-ext-avr applet/$(TARGET).elf $(TARGET).cof


.SUFFIXES: .elf .hex .eep .lss .sym
.PRECIOUS: .o

.elf.hex:
	@echo "  COPY  $@"
	@$(OBJCOPY) -O $(FORMAT) -R .eeprom $< $@

.elf.eep:
	-$(OBJCOPY) -j .eeprom --set-section-flags=.eeprom="alloc,load" \
		--change-section-lma .eeprom=0 -O $(FORMAT) $< $@

# Create extended listing file from ELF output file.
.elf.lss:
	$(OBJDUMP) -h -S $< > $@

# Create a symbol table from ELF output file.
.elf.sym:
	$(NM) -n $< > $@

	# Link: create ELF output file from library.
applet/$(TARGET).elf: applet/$(TARGET).cpp applet/core.a Configuration.h
	@echo "  CXX   $@"
	@$(CC) $(ALL_CXXFLAGS) -Wl,--gc-sections -o $@ applet/$(TARGET).cpp -L. applet/core.a $(LDFLAGS)

applet/core.a: $(OBJ) Configuration.h
	@for i in $(OBJ); do echo "  AR    $$i"; $(AR) rcs applet/core.a $$i; done

%.o: %.c Configuration.h $(MAKEFILE)
	@echo "  CC    $@"
	@$(CC) -c $(ALL_CFLAGS) $< -o $@

%.o: %.cpp Configuration.h $(MAKEFILE)
	@echo "  CXX   $@"
	@$(CXX) -c $(ALL_CXXFLAGS) $< -o $@

# Target: clean project.
clean:
	@echo "  RM    applet/*"
	@$(REMOVE) applet/$(TARGET).hex applet/$(TARGET).eep applet/$(TARGET).cof applet/$(TARGET).elf \
		applet/$(TARGET).map applet/$(TARGET).sym applet/$(TARGET).lss applet/$(TARGET).cpp applet/core.a \
		$(OBJ) $(LST) $(SRC:.c=.s) $(SRC:.c=.d) $(CXXSRC:.cpp=.s) $(CXXSRC:.cpp=.d)
	@echo "  RMDIR applet/"
	@rmdir applet

depend:
	if grep '^# DO NOT DELETE' $(MAKEFILE) >/dev/null; \
	then \
		sed -e '/^# DO NOT DELETE/,$$d' $(MAKEFILE) > \
			$(MAKEFILE).$$$$ && \
		$(MV) $(MAKEFILE).$$$$ $(MAKEFILE); \
	fi
	echo '# DO NOT DELETE THIS LINE -- make depend depends on it.' \
		>> $(MAKEFILE); \
	$(CC) -M -mmcu=$(MCU) $(CDEFS) $(CINCS) $(SRC) $(ASRC) >> $(MAKEFILE)

.PHONY:	all build elf hex eep lss sym program coff extcoff clean depend applet_files sizebefore sizeafter
