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

avgWindow = avgWindow * 2

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

# Create the basic axes 
nrows = 6
ncols = 2

figure = plt.figure(figsize=(7.5, 10.5))

edcAxes = plt.subplot2grid( (nrows, ncols), (0, 0), rowspan=2, colspan=ncols )
jvrAxes = plt.subplot2grid( (nrows, ncols), (2, 0), rowspan=2, colspan=ncols )
tempAxes = plt.subplot2grid( (nrows, ncols), (4, 0), rowspan=1, colspan=ncols )
edcTcAxes = plt.subplot2grid( (nrows, ncols), (5, 0), rowspan=1, colspan=1 )
jvrTcAxes = plt.subplot2grid( (nrows, ncols), (5, 1), rowspan=1, colspan=1 )


###############################################################################
# EDC subplots
edcAxes.get_xaxis().set_visible(False)

# plot left axis
laxis = edcAxes
laxis.set_ylabel("Volts")
laxis.tick_params(axis='y', colors='b')
plot_series_and_average(laxis, date_X, k2015a_edcV_Y, k2015a_edcV_Y_avg, "b-", "K2015_EDC")

# plot right axis
raxis = laxis.twinx()
raxis.set_ylabel("Volts")
raxis.tick_params(axis='y', colors='r')
plot_series_and_average(raxis, date_X, k196a_edcV_Y, k196a_edcV_Y_avg, "r-", "K196_EDC")

laxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.7f')%x))
raxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.5f')%x))

laxis.legend(loc=2)
raxis.legend(loc=1)


###############################################################################
# JFR subplots
laxis = jvrAxes
laxis.get_xaxis().set_visible(False)

# plot left axis
laxis.set_ylabel("Volts")
laxis.tick_params(axis='y', colors='b')
plot_series_and_average(laxis, date_X, k2015a_jvrV_Y, k2015a_jvrV_Y_avg, "b-", "K2015_JVR")

# plot right axis
raxis = laxis.twinx()
raxis.set_ylabel("Volts")
raxis.tick_params(axis='y', colors='r')
plot_series_and_average(raxis, date_X, k196a_jvrV_Y, k196a_jvrV_Y_avg, "r-", "K196_JVR")

laxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.7f')%x))
raxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.5f')%x))

laxis.legend(loc=2)
raxis.legend(loc=1)

###############################################################################
# temperature subplots
laxis = tempAxes

# plot left axis
roomTplot = laxis.plot(date_X, roomT_Y, "b-", label="Room Temp", linewidth=0.1)
windowTplot = laxis.plot(date_X, windowT_Y, "r-", label="Window Temp", linewidth=0.1)
		
laxis.set_ylabel("°C")

laxis.legend()

plt.tight_layout()	

###############################################################################
# EDC Temp Co 
plot_temp_coefficient(edcTcAxes, roomT_Y, k2015a_edcV_Y_avg, date_X, "EDC/K2015")


############################################################################### 
# JVR Temp Co 
plot_temp_coefficient(jvrTcAxes, roomT_Y, k2015a_jvrV_Y_avg, date_X, "JVR/K2015")


plt.tight_layout()

#plt.show()
figure.savefig(sourceFile + '.pdf', format='pdf', orientation='portrait', papertype='a4' )