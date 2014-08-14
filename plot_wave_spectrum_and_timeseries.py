# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ### This notebook retrieves wave spectrum data from the thredds server and plots the spectrum

# <markdowncell>

# #### import libraries

# <codecell>

import os
import os.path

import netCDF4
from netCDF4 import num2date, date2num
from netcdftime import utime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import folium
import numpy as np
import prettyplotlib as ppl

# <markdowncell>

# #### Get the data

# <codecell>

# Get the URL of the file on the thredds server
url = 'http://10.90.69.31:9000/thredds/dodsC/frfData/waves/awac/awac03/2013/awacSpec.03.201302.nc'
nc = netCDF4.Dataset(url, 'r')
print nc
nc_time = nc.variables['time']
freq = nc.variables['dwfhz'][:]
deg = nc.variables['dwdeg'][:]
spectra = nc.variables['espt']

dates = num2date(nc_time[:], units=nc_time.units)
noutcdates = []
for date in dates:
    noutcdates.append(date.replace(tzinfo=None))

# <markdowncell>

# #### Plot the data

# <codecell>

# Set the font dictionaries (for plot title and axis titles)
title_font = {'fontname':'Arial', 
              'size':'18', 
              'color':'black', 
              'weight':'bold',
              'verticalalignment':'bottom'} # Bottom vertical alignment for more space
axis_font = {'fontname':'Arial', 
             'size':'14'}

# Now plot the spectra
fig, ax = plt.subplots(figsize=(12,6))

spectrum = np.array(spectra[0,:,:]).transpose()
contour_levels = np.log10(spectrum)
nlevels = len((contour_levels)) if len((contour_levels)) < 7 else 12

cmap = cm.jet

h = plt.contourf(freq, deg, spectrum, nlevels, cmap=cmap)
# h = plt.pcolor(freq, deg, spectrum)
# fig.colorbar(h, aspect=5)

ax.set_ylabel('Direction (deg)', **axis_font)
ax.set_xlabel('Frequency (Hz)', **axis_font)
ax.set_title('Contour 2D Spectrum', **title_font)

# <codecell>

# Now plot the wave heights
fig, ax = ppl.subplots(3, 1, figsize=(12, 18))

hs = nc.variables['hs'][:]
h = ppl.plot(ax[0], noutcdates, hs, linewidth=2.0, color='b')
ax[0].set_ylabel('Significant Wave Height (m)')
ax[0].set_title('Wave Height', **title_font)

# Now plot the wave period

tp = 1/nc.variables['fp'][:]
h = ppl.plot(ax[1], noutcdates, tp, linewidth=2.0, color='r')
ax[1].set_ylabel('Peak Period (s)')
ax[1].set_title('Wave Period', **title_font)

# Now plot the wave direction

thetap = nc.variables['thetap'][:]
h = ppl.plot(ax[2], noutcdates, thetap, linewidth=2.0, color='g')
ax[2].set_ylabel('Peak Direction (deg)')
ax[2].set_title('Wave Direction', **title_font)
ax[2].set_ylim([0, 360])

# <codecell>

def unix_to_matlab_time(unix_time):
    unix_epoch = 719529
    return np.array(unix_time)/86400 + unix_epoch;

# <codecell>

# Now plot the spectrograph
spec1d = np.array(nc.variables['dwAvv'][:,:]).transpose()
# print np.log10(spec1d)
fig, ax = plt.subplots(figsize=(12, 6))
x = unix_to_matlab_time(nc_time)
y = freq
h = pcolor(x, y, np.log10(spec1d))

ax.set_ylabel('Frequency (Hz)')
ax.set_title('Spectrogram', **title_font)
plt.axis([x.min(), x.max(), y.min(), y.max()])

ax.xaxis_date()

