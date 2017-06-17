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

GPIB_ETHERNET_HOST_NAME = 'GPIB'
MAX_COMMAND_TIMEOUT_SEC = 3

MEASUREMENT_DELAY = 5.0



def RunMeasurements():
	# create and open the connection to the interface
	gpib = PrologixEthernetGPIB(GPIB_ETHERNET_HOST_NAME, MAX_COMMAND_TIMEOUT_SEC)
	gpib.open()
	try:
		# Configure the Keithley 2015
		gpib.select(10)
		gpib.write(":FUNC 'VOLT:DC'")
		gpib.write(":VOLT:DC:RANGE 10")
		gpib.write(":VOLT:DC:NPLC 10")			# 'slow' rate
		gpib.write(":VOLT:DC:DIG MAX")
		gpib.write(":FORMAT:DATA ASCII")
		gpib.write(":VOLT:DC:AVER:TCON MOV")	# setup the averaging filter
		gpib.write(":VOLT:DC:AVER:COUNT 10")	# 10 averages
		gpib.write(":VOLT:DC:AVER:STATE ON")	# enable

		# Configure the Keithley 196
		gpib.select(11)
		gpib.write('F0X')	# DC Volts
		gpib.write('R3X')	# 30V range
		gpib.write('Z0X')	# Zero disabled
		gpib.write('S3X')	# 6.5d rate
		gpib.write('B0X')	# reading from ADC
		gpib.write('G1X')	# data format without prefixes
		gpib.write('P99X')	# Digital running average filter (max)
		gpib.write('N1X')	# Internal Filter for high sensitivity measurements enabled
		gpib.write('T0X')	# continous trigger on Talk
		gpib.write('A1X')	# enable Auto/Cal Multiplex
		

		# CSV header row.
		#sys.stdout.write('DateTime, TempC, K2015, K196\n')
		
		while True:
			measurements = []
			# capture the time now, so we can get a consistent delay at the end
			start = datetime.now()
			
			# datetime
			measurements.append(start)
			measurements.append('23.0')
			
			# K2015
			gpib.select(10)
			measurements.append(float(gpib.query(":READ?")))
			
			# K196
			gpib.select(11)
			measurements.append(float(gpib.read()))
			
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
