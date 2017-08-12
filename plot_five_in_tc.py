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

	
def plot_temp_coefficient(axis, tempSeries, voltSeries, timeSeries, label):
	axis.set_xlabel("°C")
	axis.set_ylabel("Volts")
	axis.set_title(label)
	
	axis.scatter(tempSeries, voltSeries, marker='.', linewidths=0.2, s=0.1, c=timeSeries, cmap='inferno')
	
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
C5V_Y_avg = C5V_Y.rolling(window=avgWindow).mean()

plt.rcParams['font.size'] = 4
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600
plt.rcParams['figure.titlesize'] = 'small'

# Create the basic axes 
nrows = 3
ncols = 2

figure = plt.figure(figsize=(7.5, 10.5))

tc1Axes = plt.subplot2grid( (nrows, ncols), (0, 0), rowspan=1, colspan=1 )
tc2Axes = plt.subplot2grid( (nrows, ncols), (0, 1), rowspan=1, colspan=1 )
tc3Axes = plt.subplot2grid( (nrows, ncols), (1, 0), rowspan=1, colspan=1 )
tc4Axes = plt.subplot2grid( (nrows, ncols), (1, 1), rowspan=1, colspan=1 )

c4Axes = plt.subplot2grid( (nrows, ncols), (2, 0), rowspan=1, colspan=ncols )


###############################################################################
# Temp Coefficient Plots

temperatureData_Y = T7_Y		# choose which temperature to plot against

plot_temp_coefficient(tc1Axes, temperatureData_Y, C1V_Y, date_X, "C1")
plt.tight_layout()

plot_temp_coefficient(tc2Axes, temperatureData_Y, C2V_Y, date_X, "C2")
plt.tight_layout()

plot_temp_coefficient(tc3Axes, temperatureData_Y, C3V_Y, date_X, "C3")
plt.tight_layout()

plot_temp_coefficient(tc4Axes, temperatureData_Y, C4V_Y, date_X, "C4")
plt.tight_layout()


###############################################################################
# power supply plot

# plot left axis
laxis = c4Axes
laxis.set_ylabel("Volts")
laxis.tick_params(axis='y', colors='b')
plot_series_and_average(laxis, date_X, C5V_Y, C5V_Y_avg, "b-", "Power Supply")

laxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.7f')%x))

laxis.legend(loc=2)

plt.tight_layout()	


#plt.show()
figure.savefig(sourceFile + '.pdf', format='pdf', orientation='portrait', papertype='a4' )