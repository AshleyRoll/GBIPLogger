"""
Test Plotting routines from CSV
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
 

sourceFile = sys.argv[1]

avgWindow = 30		# 10 sec * 30 = 5 min average

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
		

def plot_series_and_average(axis, xSeries, mainSeries, avgSeries, color, name):
	axis.plot(xSeries, mainSeries, color, label=name, zorder=1, alpha=0.3, linewidth=0.1)
	l = "%s SMA(%d)"%(name,avgWindow)
	axis.plot(xSeries, avgSeries, color, label=l, zorder=2, alpha=1, linewidth=0.2)



# import the CSV data
sourceData = pd.read_csv(sourceFile, parse_dates=[0], skipinitialspace=True)

date_X = sourceData['DateTime']
windowT_Y = sourceData['TWindow']
roomT_Y = sourceData['TRoom']
k2015a_edcV_Y = sourceData['K2015A_EDC']
k2015a_edcV_Y_avg = k2015a_edcV_Y.rolling(window=avgWindow).mean()
k196a_edcV_Y = sourceData['K196A_EDC']
k196a_edcV_Y_avg = k196a_edcV_Y.rolling(window=avgWindow).mean()

k2015a_jvrV_Y = sourceData['K2015A_JVR']
k2015a_jvrV_Y_avg = k2015a_jvrV_Y.rolling(window=avgWindow).mean()
k196a_jvrV_Y = sourceData['K196A_JVR']
k196a_jvrV_Y_avg = k196a_jvrV_Y.rolling(window=avgWindow).mean()

plt.rcParams['font.size'] = 4
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600
plt.rcParams['figure.titlesize'] = 'small'


figure = plt.figure(1)

# EDC subplots
laxis = plt.subplot(311)
laxis.get_xaxis().set_visible(False)

# plot left axis
laxis.set_ylabel("Volts")
laxis.tick_params(axis='y', colors='b')
plot_series_and_average(laxis, date_X, k2015a_edcV_Y, k2015a_edcV_Y_avg, "b-", "K2015_EDC")

# plot right axis
raxis = plt.twinx()
raxis.set_ylabel("Volts")
raxis.tick_params(axis='y', colors='r')
plot_series_and_average(raxis, date_X, k196a_edcV_Y, k196a_edcV_Y_avg, "r-", "K196_EDC")


laxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.7f')%x))
raxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.5f')%x))

laxis.legend(loc=2)
raxis.legend(loc=1)

plt.tight_layout()

# JFR subplots
laxis = plt.subplot(312)
laxis.get_xaxis().set_visible(False)

# plot left axis
laxis.set_ylabel("Volts")
laxis.tick_params(axis='y', colors='b')
plot_series_and_average(laxis, date_X, k2015a_jvrV_Y, k2015a_jvrV_Y_avg, "b-", "K2015_JVR")

# plot right axis
raxis = plt.twinx()
raxis.set_ylabel("Volts")
raxis.tick_params(axis='y', colors='r')
plot_series_and_average(raxis, date_X, k196a_jvrV_Y, k196a_jvrV_Y_avg, "r-", "K196_JVR")

laxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.7f')%x))
raxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.5f')%x))

laxis.legend(loc=2)
raxis.legend(loc=1)

plt.tight_layout()


# temperature subplots
laxis = plt.subplot(313)


# plot left axis
roomTplot = laxis.plot(date_X, roomT_Y, "b-", label="Room Temp", linewidth=0.1)
windowTplot = laxis.plot(date_X, windowT_Y, "r-", label="Window Temp", linewidth=0.1)
		
laxis.set_ylabel("°C")

plt.legend()

plt.tight_layout()	

#plt.show()
figure.savefig(sourceFile + '.pdf', orientation='landscape', papertype='a4', bbox_inches='tight' )