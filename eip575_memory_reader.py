"""
EIP 575 over GPIB

The EIP 575 uses older style 2516 and 2532 EPROMs. My EPROM reader was unable to
read the 2532s because the pins are not compatible with the more modern 2732 EPROM.

However there is a Test Command accessible by GPIB that allows you to read / write
arbitrary memory locations.

I poked around the memory map looking for the chunks that seemed to match the EPROM 
575 revision D images that I had downloaded.

Once I identified where they were most probably located, I implemented this to 
read and extract the EPROM data into IntelHex files. These were then diffed against
the existing ones and are identical.

This means that my device should be able to be updated to implement the power meter
Option 2, although the calibration constants are not likely to be correct. I believe
that these reside on the EPROM that is fitted to the A107 Gate 

WARNING: this is a slow process. It took about 45 minutes to dump all the data.

Ash. 2018-04-11

"""

# we need to select the specific GPIB interface driver needed
from gpib.prologix.ethernet import PrologixEthernetGPIB
from gpib.base import GPIBTimeout

from intelhex import IntelHex

from datetime import datetime
import time
import sys

GPIB_ETHERNET_HOST_NAME = '192.168.0.10'
MAX_COMMAND_TIMEOUT_SEC = 3

EIP_ADDR = 2
READ_DELAY = 0.15
	

def ReadAddress(gpib, address): 
	# send address
	gpib.write('TA10')
	gpib.write('%04X' % address)
	time.sleep(READ_DELAY)
	# read result and extract the byte in hex
	data = gpib.readeol()
	print(data[-7:], flush=True)	
	gpib.write('TP')
	return int(data[-2:], 16)
	
def ReadEprom(gpib, startAddress, length, name):
	# new hex file storage
	ih = IntelHex()
	# iterate over memory and pull each byte
	for i in range(0, length):
		ih[i] = ReadAddress(gpib, startAddress+i)
		
	ih.tofile(name, format='hex')

	
def DumpEproms():
	# create and open the connection to the interface
	gpib = PrologixEthernetGPIB(GPIB_ETHERNET_HOST_NAME, MAX_COMMAND_TIMEOUT_SEC)
	gpib.open()
	try:
		# Configure the EIP 575
		print('Resetting EIP 575')
		gpib.select(EIP_ADDR)
		gpib.interface_clear()
		gpib.selected_device_clear()

		# wait for it to complete
		time.sleep(.5)
		
	
		#
		# Memory Map (tentative)
		#
		# A105 CPU Board
		# 0xC000 - 6500003-01D	4Kx8 EPROM BDC3CCF601B427037EC0B5D60E261ACE
		# 0xD000 - 6500003-02D	4Kx8 EPROM CADC54CBC95B41CCFB50CD505BF603A7
		# 0xE000 - 6500003-03D	4Kx8 EPROM D74CBDEA3839BDE0D72003BDE0D4F6EA
		# 0xF000 - 6500003-04D	4Kx8 EPROM 5F39F6030C2706D655C50126F3F69808
		#
		# 0x2800 - 6500003-05D	2Kx8 EPROM BD2B5296362713850426299636270B85
		# 
		# A107 Gate Generator
		# 0x???? - 6400002-04D	2Kx8 EPROM 131313120F0F0F0F0F0F0F0F0F0E0F10
		# 
		
		#ReadEprom(gpib, 0x2800, 0x0800, '6400003-05D-Read.hex')

		#ReadEprom(gpib, 0xC000, 0x1000, '6500003-01D-Read.hex')
		#ReadEprom(gpib, 0xD000, 0x1000, '6500003-02D-Read.hex')
		#ReadEprom(gpib, 0xE000, 0x1000, '6500003-03D-Read.hex')
		#ReadEprom(gpib, 0xF000, 0x1000, '6500003-04D-Read.hex')
		ReadEprom(gpib, 0x0000, 0x0800, '0000-07FF-Read.hex')
		
		
	
	finally:
		# Something went wrong, close.
		gpib.close()

#
# Main Entry Point
#


DumpEproms()
