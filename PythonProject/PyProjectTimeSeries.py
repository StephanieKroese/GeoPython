import netCDF4
import numpy as np
import calendar
import matplotlib.pyplot as plt
import datetime

def createTimeSeries(fileName, variable='TEMP', depth=0, lonMin=190, lonMax=240, latMin=-5, latMax=5, filterNum=3, plot='Actual'):
    '''
    This function will plot the time series of a chosen variable from the specified CDF file. Required input
    is the url for the filename. Other inputs include the variable (default TEMP), and the depth level (default
    0), filter/smoothing number (default 3), latitude and longitude of location in question (default NINO 3.4 
    region).
    '''
    nc=netCDF4.Dataset(fileName)
    var=nc.variables[variable]
    time=nc.variables['TIME1']
    lon=np.array(nc.variables['LON'])
    lat=np.array(nc.variables['LAT'])
        
    # Define region for calculations for given variable (default is NINO3.4 region). Also create date list
    startDate=datetime.datetime.strptime(time.time_origin, "%d-%b-%Y %X")
    dateList=[]
    lonBounds=np.argwhere((lon>=lonMin) & (lon<=lonMax))
    latBounds=np.argwhere((lat>=latMin) & (lat<=latMax))
    if np.shape(var)==(364, 3, 330, 720):
        region=var[:, depth, latBounds[0]:(latBounds[-1]+1), lonBounds[0]:(lonBounds[-1]+1)]
        for n in range(len(var[:, 0, 0, 0])):
            daysPassed=datetime.timedelta((time[n]/(3600*24.)))
            dateList.append(startDate+daysPassed)
    else:
        region=var[:, latBounds[0]:(latBounds[-1]+1), lonBounds[0]:(lonBounds[-1]+1)]
        for n in range(len(var[:, 0, 0])):
            daysPassed=datetime.timedelta((time[n]/(3600*24.)))
            dateList.append(startDate+daysPassed)
    region=np.array(region)
        
    # Calculate mean value for variable over region for each time step
    regionMean=[]
    for n in range(len(region[:, 0, 0])):
        regionMean.append(np.mean(region[n, :, :]))
    regionMean=np.array(regionMean)
       
    # Calculate mean and standard deviations for annual cycle
    regionMeanAnnual=[]
    regionMeanCycle=[]
    regionStdDevAnnual=[]
    regionStdDevCycle=[]
    for n in range(((len(region[:, 0, 0]))/5)+1):
        regionMeanAnnual.append(np.mean(regionMean[n:(len(region[:, 0, 0])):((len(region[:, 0, 0]))/5)]))
    regionMeanAnnual=np.array(regionMeanAnnual)
    for n in range(len(regionMean)):
        regionMeanCycle.append(regionMeanAnnual[(n%(len(regionMeanAnnual)))])           
    regionMeanCycle=np.array(regionMeanCycle)
    for n in range(((len(region[:, 0, 0]))/5)+1):
        regionStdDevAnnual.append(np.std(regionMean[n:(len(region[:, 0, 0])):((len(region[:, 0, 0]))/5)]))
    regionStdDevAnnual=np.array(regionStdDevAnnual)
    for n in range(len(regionMean)):
        regionStdDevCycle.append(regionStdDevAnnual[(n%(len(regionStdDevAnnual)))])           
    regionStdDevCycle=np.array(regionStdDevCycle)
    
    # Calculate upper and lower bounds for values within one standard deviation of the mean
    upperBound=regionMeanCycle+regionStdDevCycle
    lowerBound=regionMeanCycle-regionStdDevCycle
    
    # Calculate anomaly
    regionAnomaly=regionMean-regionMeanCycle
    
    # Plot results
    if plot=='Actual':
        plt.fill_between(dateList, upperBound, lowerBound, color='k', alpha=0.15)
        plt.plot(dateList, regionMeanCycle, color='k', lw=0.5)
        plt.plot(dateList, regionMean, color='k')
        plt.fill_between(dateList, regionMean, regionMeanCycle, where=regionMean>regionMeanCycle, color='r', alpha=0.2)
        plt.fill_between(dateList, regionMean, regionMeanCycle, where=regionMean<regionMeanCycle, color='b', alpha=0.2)
        plt.xticks(rotation=45)
        plt.ylabel(var.units)
        plt.show()
    
    elif plot=='Anomaly':
        plt.fill_between(dateList, regionStdDevCycle, -(regionStdDevCycle), color='k', alpha=0.15)
        plt.plot(dateList, regionAnomaly, color='k')
        plt.axhline(y=0, color='k')
        plt.fill_between(dateList, regionAnomaly, 0, where=regionAnomaly>0, color='r', alpha=0.2)
        plt.fill_between(dateList, regionAnomaly, 0, where=regionAnomaly<0, color='b', alpha=0.2)
        plt.xticks(rotation=45)
        plt.show()
    
    
    
    
# Call function
createTimeSeries('http://sodaserver.tamu.edu:80/opendap/TEMP/SODA_2.3.1_01-01_python.cdf')

