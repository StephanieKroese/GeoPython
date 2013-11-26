import numpy as np
from mpl_toolkits.basemap import Basemap,cm
import matplotlib.pyplot as plt
import datetime
from matplotlib.patches import Polygon

def plot_and_timeSeries(url, var, var2, tlvl, dlvl, time, time2, lon, lat, llat, ulat, llon, rlon):
    
    # setting up data into basemap with given projection
    lons, lats = np.meshgrid(lon, lat)
    #fig = plt.figure()
    plt.subplot2grid((4, 6), (0, 0), colspan=6, rowspan=3)
    #ax = fig.add_axes([0.1,0.1,0.8,0.8])
    m = Basemap(llcrnrlat=llat,urcrnrlat=ulat,\
            llcrnrlon=llon,urcrnrlon=rlon,\
            projection='mill')
    x,y = m(lons, lats)

    # drawing the map
    m.fillcontinents(color='gray',lake_color='gray')
    m.drawcoastlines(linewidth = 0.4)
    m.drawparallels(np.arange(-90.,90.,15.), labels =[1,0,0,1],fontsize=10)
    m.drawmeridians(np.arange(-180.,181.,40.),labels =[0,1,0,1],fontsize=10)
    m.drawmapboundary()

    # plotting data on the map
    plt.contourf(x,y,var[tlvl,dlvl,:,:],cmap=cm.sstanom)
    cb = plt.colorbar(orientation='horizontal')
    #cb.set_label(r'Sea Surface Temperature (deg C)',fontsize=14,style='italic')
    plt.title(r'Sea Surface Temperature (deg C)',fontsize=14,style='italic')
    
    
    # Define region for calculations for given variable (default is NINO3.4 region). Also create date list
    startDate=datetime.datetime.strptime(time2.time_origin, "%d-%b-%Y %X")
    dateList=[]
    depth=0
    lonMin=190
    lonMax=240
    latMin=-5
    latMax=5
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
    plt.subplot2grid((4, 6), (3, 0), colspan=4, rowspan=1)
    plot='Actual'
    if plot=='Actual':
        plt.fill_between(dateList, upperBound, lowerBound, color='k', alpha=0.15)
        plt.plot(dateList, regionMeanCycle, color='k', lw=0.5)
        plt.plot(dateList, regionMean, color='k')
        plt.fill_between(dateList, regionMean, regionMeanCycle, where=regionMean>regionMeanCycle, color='r', alpha=0.2)
        plt.fill_between(dateList, regionMean, regionMeanCycle, where=regionMean<regionMeanCycle, color='b', alpha=0.2)
        plt.xticks(rotation=45)
        plt.ylabel(var2.units)
        dotX=dateList[50]
        dotY=regionMean[50]
        plt.scatter(dotX, dotY, s=75, marker='o', color='r')
        
    elif plot=='Anomaly':
        plt.fill_between(dateList, regionStdDevCycle, -(regionStdDevCycle), color='k', alpha=0.15)
        plt.plot(dateList, regionAnomaly, color='k')
        plt.axhline(y=0, color='k')
        plt.fill_between(dateList, regionAnomaly, 0, where=regionAnomaly>0, color='r', alpha=0.2)
        plt.fill_between(dateList, regionAnomaly, 0, where=regionAnomaly<0, color='b', alpha=0.2)
        plt.xticks(rotation=45)
        dotX=dateList[50]
        dotY=regionAnomaly[50]
        plt.scatter(dotX, dotY, s=100, marker='o', color='r')
                
        
    plt.subplot2grid((4, 6), (3, 4), colspan=2)
    lats = [ -5, 5, 5, -5 ]
    lons = [ -170, -170, -120, -120 ]
    mapAttempt1 = Basemap(projection='robin',lon_0=180)
    mapAttempt1.fillcontinents('k')
    x, y = mapAttempt1( lons, lats )
    xy = zip(x,y)
    poly = Polygon(xy, edgecolor='r', facecolor='none', lw=2 )
    plt.gca().add_patch(poly)
        
    plt.show()
