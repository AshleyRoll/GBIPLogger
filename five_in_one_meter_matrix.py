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

MEASUREMENT_DELAY = 1.0
MATRIX_SWITCH_STABILISE_DELAY = 0.2

TMP_LOGGER_ADDR = 11
MATRIX_SWITCH_ADDR = 10
K2015_A_ADDR = 1


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
		
		#
		# Configure the Keithley 705 switch.
		# This code assumes 2 * 7052 4*5 Matrix cards
		# Column 01 - 05 is card slot 1
		# Column 06 - 10 is card slot 2
		# Rows are 1 - 4
		# The "channel" numbers are then ccr (eg Col 3, row 2 = 03:2) close is C03:2, open is N03:2
		#
		# We will use columns as inputs, and rows as outputs. Note that we can tie the cards together to get more
		# columns or rows.. 
		# 
		# we can then configure each input to go to 1 or more outputs or we can cycle them between each output
		# and keep the outputs isolated. It is pretty flexible as we can open and close any cross-connect at any time.
		# 
		# WARNING: a delay is needed 
		gpib.select(MATRIX_SWITCH_ADDR)
		gpib.write('K0X')		# Assert EOI
		gpib.write('T6X')		# trigger on external (not using triggers)
		gpib.write('A0X')		# Matrix mode
		gpib.write('RX')		# Reset all channels
		
		gpib.write('B011X')		# temp.. display col 1 row 1
		
		# Configure the Keithley 2015
		gpib.select(K2015_A_ADDR)
		gpib.write(":FUNC 'VOLT:DC'")
		gpib.write(":VOLT:DC:RANGE 10")
		gpib.write(":VOLT:DC:NPLC 10")			# 10 = 'slow' rate, 1 = 'medium'
		gpib.write(":VOLT:DC:DIG MAX")
		gpib.write(":FORMAT:DATA ASCII")
		#gpib.write(":VOLT:DC:AVER:TCON MOV")	# setup the averaging filter
		#gpib.write(":VOLT:DC:AVER:COUNT 10")	# 10 averages
		gpib.write(":VOLT:DC:AVER:STATE OFF")	# disable filter
		gpib.write(":INIT:CONT OFF")			# one shot trigger

		
		
		# CSV header row.
		sys.stdout.write('DateTime, T7, T8, C1, C2, C3, C4, C5\n')
		
		while True:
			measurements = []
			# capture the time now, so we can get a consistent delay at the end
			start = datetime.now()
			
			# datetime
			measurements.append(start.strftime("%Y-%m-%d %H:%M:%S"))
			
			# K740
			gpib.select(TMP_LOGGER_ADDR)
			# select Channel 7
			gpib.write('C07X')
			measurements.append(float(gpib.read()))				# trigger and fetch current reading
			# select Channel 8
			gpib.write('C08X')
			measurements.append(float(gpib.read()))				# trigger and fetch current reading
			
		
			# Row 1: K2015	
			# Col 1 - 5: inputs
			
			for c in range(1, 6):
				# enable the channel
				gpib.select(MATRIX_SWITCH_ADDR)
				gpib.write('C{col:02d}:{row:d}X'.format(col=c, row=1))
				time.sleep(MATRIX_SWITCH_STABILISE_DELAY)				#stabilise
				
				# K2015
				gpib.select(K2015_A_ADDR)
				measurements.append(round(float(gpib.query(":READ?")), 7))
				
				# disable channel
				gpib.select(MATRIX_SWITCH_ADDR)
				gpib.write('N{col:02d}:{row:d}X'.format(col=c, row=1))
			
						
			sys.stdout.write(','.join(str(x) for x in measurements))
			sys.stdout.write('\n')
			sys.stdout.flush()

			# compute the elapsed time and if it is under our measurement delay, we wait
			# the appropraite time to sync to the start of the cycle again
		#	elapsed = datetime.now() - start
		#	if elapsed.total_seconds() < MEASUREMENT_DELAY:
		#		time.sleep(MEASUREMENT_DELAY - elapsed.total_seconds())

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
	#try:
		RunMeasurements()
	#except GPIBTimeout as e:
	#	sys.stderr.write('GPIB Timeout Reading value, restarting\n')
	#	sys.stderr.flush()
	#	continue
