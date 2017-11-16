import numpy as np
import pandas as pd 
import datetime as dt 
import matplotlib.pyplot as plt 
import os, sys, time, ccgfilt, netCDF4, calendar
#import palettable
cal= calendar.Calendar()  

from pyhdf import SD
from numpy import pi, sin, cos
from scipy.stats import linregress
from scipy.optimize import curve_fit
from matplotlib import rc
from matplotlib.dates import num2date, DateFormatter, MonthLocator, YearLocator, \
     DayLocator
from york_fit import york_fit
from inputData import *

main_dir = '/data/02/elutsch/IASI/'
start = dt.datetime(2006,1,1)
end = dt.datetime(2017,12,31)
site = 'Eureka'

def read_iasi(site,start,end):
#if __name__ == "__main__":	
    dates = [start + dt.timedelta(days=x) for x in range((end-start).days)]
    dataIASI = [] 
    
    found, missing = 0, 0 
    
    for date in dates:
	iasi_file = os.path.join(main_dir,site,site+'_IASI_'+date.strftime('%Y%m%d')+'.nc')
	
	if os.path.isfile(iasi_file):
	    #print iasi_file
	    try:    
		    iasi_nc = netCDF4.Dataset(iasi_file)
		    datetime = [dt.datetime(2000,1,1)+dt.timedelta(seconds=x) for x in iasi_nc.variables['datetime'][:]]
		    temp = pd.DataFrame(datetime,columns=['datetime'])
		    iasi_flg = True
		    found += 1
	    except:
		    iasi_flg = False
	    
	    if iasi_flg: 
		temp['latitude']=iasi_nc.variables['lat'][:]
		temp['longitude']=iasi_nc.variables['lon'][:]
		temp['column']=iasi_nc.variables['column'][:]
		temp['error']=iasi_nc.variables['error'][:]
		#temp['apriori']=list(iasi_nc.variables['apriori'])
		#temp['avk']=list(iasi_nc.variables['avk'][:])
		#temp['dt']=iasi_nc.variables['dt'][:]
		temp['dx']=iasi_nc.variables['dx'][:]
    
		dataIASI.append(temp)
		del temp		
	else:
	    missing += 1
	    #print 'No file: '+iasi_file
	
    print '\n IASI Files Found: '+str(found)+' Files missing: '+str(missing)
    dataIASI = pd.concat(dataIASI)
    dataIASI.index = pd.to_datetime(dataIASI['datetime'])
    #del dataIASI['datetime']
    
    return dataIASI
                      
