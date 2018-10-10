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
MAX_COMMAND_TIMEOUT_SEC = 3

MEASUREMENT_DELAY = 5.0

TMP_LOGGER_ADDR = 11

def RunMeasurements():
	# create and open the connection to the interface
	gpib = PrologixEthernetGPIB(GPIB_ETHERNET_HOST_NAME, MAX_COMMAND_TIMEOUT_SEC)
	gpib.open()
	try:
		# Clear the bus
		gpib.interface_clear()
	
		#
		# Configure the Keithley 740 Scanning Theromometer
		# currently only channels 7 & 8 are K type, Channels 2-6 are J, Channels 9 & 10 are T.
		#
		gpib.select(TMP_LOGGER_ADDR)
		gpib.write('K0X')		# Assert EOI, hold off bus until commands complete
		gpib.write('P1X')		# filter on
		gpib.write('O0X')		# celsius scale
		gpib.write('N10X')		# set all channels off
		gpib.write('T0X')		# trigger continous on talk (make a measurement when addressed to talk)
		gpib.write('G2X')		# format without prefix or suffix
		gpib.write('F0X')		# Function = current channel
		gpib.write('B0X')		# Read mode = current channel
		
		
		# configure channels. Note if a reading is attempted on an "OFF" channel, the bus will lockup
		gpib.write('C07N2X')	# Channel 7, Type K
		gpib.write('C08N2X')	# Channel 8, Type K
		

		
		# CSV header row.
		sys.stdout.write('DateTime, T7, T8\n')
		
		while True:
			measurements = []
			# capture the time now, so we can get a consistent delay at the end
			start = datetime.now()
			
			# datetime
			measurements.append(start)
			
			# K740
			gpib.select(TMP_LOGGER_ADDR)
			# select Channel 7
			gpib.write('C07X')
			measurements.append(float(gpib.read()))				# trigger and fetch current reading
			# select Channel 8
			gpib.write('C08X')
			measurements.append(float(gpib.read()))				# trigger and fetch current reading
			
									
			sys.stdout.write(','.join(str(x) for x in measurements))
			sys.stdout.write('\n')
			sys.stdout.flush()

			# compute the elapsed time and if it is under our measurement delay, we wait
			# the appropraite time to sync to the start of the cycle again
			elapsed = datetime.now() - start
			if elapsed.total_seconds() < MEASUREMENT_DELAY:
				time.sleep(MEASUREMENT_DELAY - elapsed.total_seconds())

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
while True:
	try:
		RunMeasurements()
	except GPIBTimeout as e:
		sys.stderr.write('GPIB Timeout Reading value, restarting\n')
		sys.stderr.flush()
		continue
