# Stephanie Kroese
# 10 October 2013
# This script contains a function that will read information about a colormap
# from a webpage and then create that colormap. It will then return the colormap
# The end of the script runs the function and shows a plot using the colormap


import urllib
import numpy as np
import matplotlib.pyplot as plt           

def createColorMap(url):
    '''
    This function will return a colormap based on information from a webpage
    creating the desired colormap. The url of the webpage must be included in 
    the function call, in single quotes.
    '''
    f=urllib.urlopen(url)
    
    red=[]
    green=[]
    blue=[]
    
    for line in f.readlines()[2:]:
        data=line.split()
        red.append(data[0])
        green.append(data[1])
        blue.append(data[2])
    
    length=len(red)
    for n in range(length):
        red[n]=float(red[n])
        green[n]=float(green[n])
        blue[n]=float(blue[n])
   
    reds=[]
    greens=[]
    blues=[]
    
    for n in range(length):
        reds.append((n/(float(length-1)), red[n-1], red[n]))
        greens.append((n/(float(length-1)), green[n-1], green[n]))
        blues.append((n/(float(length-1)), blue[n-1], blue[n]))
    
    colorMap={'red': reds, 'green': greens, 'blue': blues}
    newCmap = plt.matplotlib.colors.LinearSegmentedColormap('newCmap',colorMap,256)
    return newCmap
    
x=range(100)
y=range(100)
x, y=np.meshgrid(x, y)
z=x**2+y**2
plt.pcolormesh(z, cmap=createColorMap('http://geography.uoregon.edu/datagraphics/color/GrMg_16.txt'))
plt.colorbar()
plt.show() 
