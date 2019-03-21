"""
Generic Logging for GPIB instrument data

This is a pretty simple interface, you may need to add your own implementation for specific measurements
"""

# we need to select the specific GPIB interface driver needed
from gpib.prologix.ethernet import PrologixEthernetGPIB
from gpib.base import GPIBTimeout

from datetime import datetime
import time
import sys

GPIB_ETHERNET_HOST_NAME = '192.168.0.10'
MAX_COMMAND_TIMEOUT_SEC = 2

K2015_A_ADDR = 1

def RunMeasurements():
	# create and open the connection to the interface
	gpib = PrologixEthernetGPIB(GPIB_ETHERNET_HOST_NAME, MAX_COMMAND_TIMEOUT_SEC)
	gpib.open()
	try:
		# Clear the bus
		gpib.interface_clear()

		gpib.select(K2015_A_ADDR)
		gpib.write(":FUNC 'VOLT:DC'")
	
		print(f'ID: {gpib.query("*IDN?")}')
		print(f'Calibrated: {gpib.query(":CAL:PROT:DATE?")}')
		print(f'Next Due: {gpib.query(":CAL:PROT:NDUE?")}')
		print('Data:')
		
		# cal data is long and there are weird effects with normal query
		# to get the full data set we have to read twice
		gpib.write(":CAL:PROT:DATA?")
		
		print(gpib.read() + gpib.read())

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
RunMeasurements()
