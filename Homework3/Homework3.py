# Stephanie Kroese
# 17 October 2013
# Assignment 3

# This script will read a netCDF file from a webpage containing data about 
# specific humidity (among other things). It will then plot the data on a world
# map using basemap. It also creates a pandas object of the annual cycle of 
# specific humidity for a certain point and plots the annual cycle. It then 
# displays all this information in a graphic.

import numpy as np
import datetime
import netCDF4
import matplotlib.pyplot as plt
from mpl_toolkits import basemap
import pandas as pd

# Open webpage and netCDF file, get data on specific humidity, latitude, and 
# longitude
nc1=netCDF4.Dataset('http://apdrc.soest.hawaii.edu:80/dods/public_data/satellite_product/GSSTF/clima')
humidity=nc1.variables['qsfc']
humidity1=humidity[0, :, :]

lat=nc1.variables['lat']
lon=nc1.variables['lon']

# Turn data into basemap projection. Robinson projection is used in this case
lon, lat=np.meshgrid(lon, lat)

mapAttempt1=basemap.Basemap(projection='robin', lon_0=0)
x, y=mapAttempt1(lon, lat)

# Create map showing specific humidity
plt.subplot2grid((3, 3), (0, 0), rowspan=2, colspan=3)
mapAttempt1.fillcontinents()
mapAttempt1.drawcoastlines()
plt.pcolormesh(x, y, humidity1, cmap='Greens')
plt.title('Surface specific humidity (Jan. 1988-2000 climatology)')
cb=plt.colorbar(orientation='vertical')
cb.set_label('g/kg of water vapor')


# Select a point to find the annual cycle of humidity, plot cycle (35N, 160E)
# Create Pandas time series for the specific humidity for the year
months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December']
humiditySeries=pd.DataFrame(humidity[:, 125, 340], index=months)

# Make lists to plot to show annual cycle repeated over several years
dates=[datetime.datetime(year, month, 15) for year in range(1988, 2000) for month in range(1, 13)]
humidityPoint=[humiditySeries.iloc[month] for year in range(1988, 2000) for month in range (len(months))]

# Plot timeseries data
plt.subplot2grid((3, 3), (2, 0), colspan=2)
plt.plot(dates, humidityPoint)
plt.title('Specific Humidity for 35$^\circ$N, 160$^\circ$E')
plt.ylabel('Specific humidity (g/kg)')
plt.xlabel('Year')

# Create map showing where this point is (just for reference)
pointLat=125
pointLon=340
plt.subplot2grid((3, 3), (2, 2))
mapAttempt1.fillcontinents('k')
plt.title('Location of point')
pointLon, pointLat=mapAttempt1(160, 35)
plt.scatter(pointLon, pointLat, marker='*', color='r')

plt.show()
