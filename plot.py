"""
Test Plotting routines from CSV
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
 

sourceFile = '../../log-2017-07-22.csv'

avgWindow = 60

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

# import the CSV data
sourceData = pd.read_csv(sourceFile, parse_dates=[0], skipinitialspace=True)

date_X = sourceData['DateTime']
windowT_Y = sourceData['TWindow']
roomT_Y = sourceData['TRoom']
k2015aV_Y = sourceData['K2015A']
k2015aV_Y_avg = k2015aV_Y.rolling(window=avgWindow).mean()
k196aV_Y = sourceData['K196A']
k196aV_Y_avg = k196aV_Y.rolling(window=avgWindow).mean()



plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

plt.rcParams['figure.titlesize'] = 'small'


# first of 2 subplots
figure = plt.figure(1)



laxis = plt.subplot(211)
laxis.get_xaxis().set_visible(False)

laxis.set_ylabel("Volts")
laxis.tick_params(axis='y', colors='b')

# plot left axis
laxis.plot(date_X, k2015aV_Y, "b-", label="K2015", zorder=1, alpha=0.3, linewidth=0.1)
laxis.plot(date_X, k2015aV_Y_avg, "b-", label="K2015 SMA(%d)"%avgWindow, zorder=2, alpha=1, linewidth=0.2)
# plot right axis
raxis = plt.twinx()

raxis.set_ylabel("Volts")
raxis.tick_params(axis='y', colors='r')
raxis.plot(date_X, k196aV_Y, "r-", label="K196", zorder=1, alpha=0.3, linewidth=0.1)
raxis.plot(date_X, k196aV_Y_avg, "r-", label="K196 SMA(%d)"%avgWindow, zorder=1, alpha=1, linewidth=0.2)

laxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.7f')%x))
raxis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('%.5f')%x))

laxis.legend(loc=2)
raxis.legend(loc=1)

plt.tight_layout()

# second of 2 subplots
laxis = plt.subplot(212)


# plot left axis
roomTplot = laxis.plot(date_X, roomT_Y, "b-", label="Room Temp", linewidth=0.1)
windowTplot = laxis.plot(date_X, windowT_Y, "r-", label="Window Temp", linewidth=0.1)
		
laxis.set_ylabel("°C")

plt.legend()

plt.tight_layout()	

#plt.show()
figure.savefig(sourceFile + '.pdf', orientation='landscape', papertype='a4', bbox_inches='tight' )