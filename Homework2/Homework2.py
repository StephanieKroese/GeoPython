# Stephanie Kroese
# 15 October 2013
# Homework 2

# This script will run a function that reads stream discharge data from a webpage
# usling urllib and will calculate and return the mean and standard deviation 
# for each day. It will then plot the results as a time series. The function is 
# designed to take inputs from the user to allow flexibility in choosing the 
# start and end dates used in the calculation, as well as which dates are plotted. 

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import urllib
from datetime import timedelta


def createTimeSeries(siteNumber, plotBegin, plotEnd, climoBegin='1900-01-01', climoEnd='2010-12-31'):
    '''
    This function will take 5 input values and return a plot showing the stream
    discharge from a location over time. The five required input values are 
    
    siteNumber: The location code for the river discharge measurement
    plotBegin: The begin date that is actually plotted
    plotEnd: The end date for what is actually plotted
    climoBegin: The begin date for which the mean and standard deviations are 
        calculated (default is the earliest recorded value)
    climoEnd: The end date for which the mean and standard deviations are 
        calculated (default is 2010-12-31)

    
    This enables the user to compare just a few years of data to a long term
    average. The plot begin and end dates must be within the range of the 
    climatology dates. Dates should be entered in format 'YYYY-MM-DD'. All data
    should be entered in single quotes. Function will also return the annual 
    mean for the selected climatology years, standard deviation for selected 
    climatology years, and the discharge for the selected plotting years as arrays.
    '''
    
    # Open URL, get data
    url='http://waterdata.usgs.gov/az/nwis/dv?cb_00060=on&format=rdb&period=&begin_date='+climoBegin+'&end_date='+climoEnd+'&site_no='+siteNumber+'&referred_module=sw'
    f=urllib.urlopen(url)

    # Get data from webpage, store and convert to array
    dates=[]
    discharge=[]
    for line in f.readlines()[27:]:
        data=line.split()
        dates.append(data[2])
        discharge.append(float(data[3]))
    discharge=np.array(discharge)
    
    # Convert discharge to correct units (from ft^3/s to m^3/s)
    discharge*=0.0283168
    
    # Convert dates into datetime objects, separate year, month, and day into arrays
    for n in range(len(discharge)):
        dates[n]=(datetime.strptime(dates[n], "%Y-%m-%d"))
    monthParsed=[]
    yearParsed=[]
    dayParsed=[]
    for n in range(len(discharge)):
        monthParsed.append(dates[n].month)
        yearParsed.append(dates[n].year)
        dayParsed.append(dates[n].day)
    monthParsed=np.array(monthParsed)
    dayParsed=np.array(dayParsed)
    yearParsed=np.array(yearParsed)
    
    # Calculate daily means and standard deviations, convert to arrays
    dailyMean=[]
    dailyStdDev=[]
    for m in range(12):
        for d in range(31):
            idx=np.where((monthParsed==m+1) & (dayParsed==d+1))
            dailyMean.append(np.mean(discharge[idx]))
            dailyStdDev.append(np.std(discharge[idx]))
            
    # Remove dates that do not exist
    dailyMeans=[]
    dailyStdDevs=[]
    dailyMeans=np.delete(dailyMean, [60, 61, 123, 185, 278, 340])
    dailyStdDevs=np.delete(dailyStdDev, [60, 61, 123, 185, 278, 340])
        
    # Create longer arrays that correspond to the dates that will be plotted
    plotBeginDate=datetime.strptime(plotBegin, '%Y-%m-%d')
    plotEndDate=datetime.strptime(plotEnd, '%Y-%m-%d')
    climoBeginDate=(dates[0])
    plotDateRange=plotEndDate-plotBeginDate
    daysUntilBegin=plotBeginDate-climoBeginDate
    
    longTermCycle=[]
    longTermStdDev=[]
    daysSinceYrBegin=plotBeginDate-datetime((plotBeginDate.year), 01, 01)
    for n in range((plotDateRange.days+1)):
        longTermCycle.append(dailyMeans[(n%366)-(daysSinceYrBegin.days)])
        longTermStdDev.append(dailyStdDevs[(n%366)-(daysSinceYrBegin.days)])
    
    # Convert new longer lists to arrays
    longTermCycle=np.array(longTermCycle)
    longTermStdDev=np.array(longTermStdDev)
   
    # Calculate upper and lower bounds of standard deviations from mean
    longTermUpper=longTermCycle+longTermStdDev
    longTermLower=longTermCycle-longTermStdDev
    dateList=[plotBeginDate+timedelta(days=n) for n in range(plotDateRange.days+1)]
    
    # Set negative values equal to zero because negative stream discharge can't exist
    for n in range(len(longTermLower)):
        if longTermLower[n] < 0:
            longTermLower[n] = 0 
  
    # Plot the resulting calculations
    plt.plot_date(dateList, discharge[(daysUntilBegin.days):((daysUntilBegin.days)+(plotDateRange.days)+1)], 'k', lw=0.5)
    plt.fill_between(dateList, longTermUpper, longTermLower, color='k', alpha=0.25)
    plt.plot(dateList, longTermCycle, 'r', lw=1.5)
    plt.title('Annual stream discharge')
    plt.ylabel('Stream discharge (m^3 per second)')
    plt.xticks(rotation=30)
    plt.ylim(ymin=0)
    plt.show()

    return dailyMeans, dailyStdDevs, discharge[(daysUntilBegin.days):((daysUntilBegin.days)+(plotDateRange.days)+1)]    
    

# Here is an example of the function when it is run. The site is the Colorado 
#River at the Grand Canyon. Three years of data will be plotted and the default 
# climatology dates are used.
x, y, z=createTimeSeries(siteNumber='09402500', plotBegin='1954-01-01', plotEnd='1956-12-31')

