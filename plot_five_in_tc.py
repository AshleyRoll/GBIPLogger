"""
Test Plotting routines from CSV
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


sourceFile = sys.argv[1]

avgWindow = 300


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
		

def plot_series_and_average(axis, xSeries, mainSeries, avgSeries, color, name):
	axis.plot(xSeries, mainSeries, color, label=name, zorder=1, alpha=0.3, linewidth=0.1)
	l = "%s SMA(%d)"%(name,avgWindow)
	axis.plot(xSeries, avgSeries, color, label=l, zorder=2, alpha=1, linewidth=0.2)
	axis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.7f')%x))

def plot_series(axis, xSeries, mainSeries, color, name):
	axis.plot(xSeries, mainSeries, color, label=name, zorder=1, alpha=0.3, linewidth=0.1)
	axis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.7f')%x))

	
def plot_temp_coefficient(axis, tempSeries, voltSeries, timeSeries, label):
	axis.set_xlabel("°C")
	axis.set_ylabel("Volts")
	axis.set_title(label)
	
	#axis.scatter(tempSeries, voltSeries, marker='.', linewidths=0.5, s=0.1) #, c=timeSeries, cmap='inferno')
	axis.plot(tempSeries, voltSeries, "r-", linewidth=0.1)
	
	xmin = tempSeries.min()
	xmax = tempSeries.max()
	xfudge = (xmax - xmin) * 0.1
	
	ymin = voltSeries.min()
	ymax = voltSeries.max()
	yfudge = (ymax - ymin) * 0.1
	
	axis.set_xlim(xmin-xfudge, xmax+xfudge)
	axis.set_ylim(ymin-yfudge, ymax+yfudge)
	axis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.7f')%x))
	


# import the CSV data
sourceData = pd.read_csv(sourceFile, parse_dates=[0], skipinitialspace=True)

date_X = sourceData['DateTime']
T7_Y = sourceData['T7']
T8_Y = sourceData['T8']
C1V_Y = sourceData['C1']
C2V_Y = sourceData['C2']
C3V_Y = sourceData['C3']
C4V_Y = sourceData['C4']
C5V_Y = sourceData['C5']


C1V_Y_avg = C1V_Y.rolling(window=avgWindow).mean()
C2V_Y_avg = C2V_Y.rolling(window=avgWindow).mean()
C3V_Y_avg = C3V_Y.rolling(window=avgWindow).mean()
C4V_Y_avg = C4V_Y.rolling(window=avgWindow).mean()
C5V_Y_avg = C5V_Y.rolling(window=avgWindow).mean()

plt.rcParams['font.size'] = 4
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600
plt.rcParams['figure.titlesize'] = 'small'

# Create the basic axes 
nrows = 6
ncols = 2

figure = plt.figure(figsize=(7.5, 10.5))

tc1Axes = plt.subplot2grid( (nrows, ncols), (0, 0), rowspan=1, colspan=1 )
tc2Axes = plt.subplot2grid( (nrows, ncols), (1, 0), rowspan=1, colspan=1 )
tc3Axes = plt.subplot2grid( (nrows, ncols), (2, 0), rowspan=1, colspan=1 )
tc4Axes = plt.subplot2grid( (nrows, ncols), (3, 0), rowspan=1, colspan=1 )

v1Axes = plt.subplot2grid( (nrows, ncols), (0, 1), rowspan=1, colspan=1 )
v2Axes = plt.subplot2grid( (nrows, ncols), (1, 1), rowspan=1, colspan=1 )
v3Axes = plt.subplot2grid( (nrows, ncols), (2, 1), rowspan=1, colspan=1 )
v4Axes = plt.subplot2grid( (nrows, ncols), (3, 1), rowspan=1, colspan=1 )


c5Axes = plt.subplot2grid( (nrows, ncols), (4, 0), rowspan=1, colspan=ncols )
tempAxes = plt.subplot2grid( (nrows, ncols), (5, 0), rowspan=1, colspan=ncols )

###############################################################################
# Temp Coefficient Plots

temperatureData_Y = T8_Y		# choose which temperature to plot against

plot_series_and_average(v1Axes, date_X, C1V_Y, C1V_Y_avg, "b-", "C1")
plot_series_and_average(v2Axes, date_X, C2V_Y, C2V_Y_avg,  "b-", "C2")
plot_series_and_average(v3Axes, date_X, C3V_Y, C3V_Y_avg,  "b-", "C3")
plot_series_and_average(v4Axes, date_X, C4V_Y, C4V_Y_avg,  "b-", "C4")

v1Axes.legend(loc=2)
v2Axes.legend(loc=2)
v3Axes.legend(loc=2)
v4Axes.legend(loc=2)

plot_temp_coefficient(tc1Axes, temperatureData_Y, C1V_Y, date_X, "C1 TC")
plt.tight_layout()

plot_temp_coefficient(tc2Axes, temperatureData_Y, C2V_Y, date_X, "C2 TC")
plt.tight_layout()

plot_temp_coefficient(tc3Axes, temperatureData_Y, C3V_Y, date_X, "C3 TC")
plt.tight_layout()

plot_temp_coefficient(tc4Axes, temperatureData_Y, C4V_Y, date_X, "C4 TC")
plt.tight_layout()


###############################################################################
# power supply plot

# plot left axis
laxis = c5Axes
laxis.set_ylabel("Volts")
laxis.tick_params(axis='y', colors='b')
plot_series_and_average(laxis, date_X, C5V_Y, C5V_Y_avg, "b-", "Power Supply")

laxis.legend(loc=2)
plt.tight_layout()	

###############################################################################
# temperature subplots
laxis = tempAxes

# plot left axis
roomTplot = laxis.plot(date_X, T7_Y, "b-", label="Room Temp", linewidth=0.1)
windowTplot = laxis.plot(date_X, T8_Y, "r-", label="LM3900 Temp", linewidth=0.1)
		
laxis.set_ylabel("°C")

laxis.legend()

plt.tight_layout()	



#plt.show()
figure.savefig(sourceFile + '.pdf', format='pdf', orientation='portrait', papertype='a4' )