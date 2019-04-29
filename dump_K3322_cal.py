"""
Download the calibration constants from a Keithley 3322/3333 LCR meter
"""

# we need to select the specific GPIB interface driver needed
from gpib.prologix.ethernet import PrologixEthernetGPIB
from gpib.base import GPIBTimeout

from datetime import datetime
import time
import sys

GPIB_ETHERNET_HOST_NAME = '192.168.0.10'
MAX_COMMAND_TIMEOUT_SEC = 1

INSTRUMENT_A_ADDR = 2
READ_DELAY = 0.15


def PadHex(i, w):
	s = hex(i)
	return s[2:].zfill(w)

def DumpCalConstants():
	# create and open the connection to the interface
	gpib = PrologixEthernetGPIB(GPIB_ETHERNET_HOST_NAME, MAX_COMMAND_TIMEOUT_SEC)
	gpib.open()
	try:
		# Clear the bus
		gpib.interface_clear()

		gpib.select(INSTRUMENT_A_ADDR)
		
		print(f'ID: {gpib.query("?ID")}')

		for addr in range(0x1000, 0x1010, 2):
			paddr = PadHex(addr, 7)
			v = gpib.query(f'`~1,{paddr}')
			
			if addr % 8 == 0:
				v = v + ' ' + gpib.query(f'`~2,{paddr}') + ' ' + gpib.query(f'`~3,{paddr}')
			
			print(f'{paddr}: {v}')
		


	finally:
		# Something went wrong, close.
		gpib.close()

#
# Main Entry Point
#
# Continously run the measurements, catching the GPIBTimeout exception
# if we get one and restarting measurements. If a different exception occurs
# the loop is terminated
#
DumpCalConstants()
