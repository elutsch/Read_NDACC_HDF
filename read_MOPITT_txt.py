import os, sys
import numpy as np 
import pandas as pd
import datetime as dt

main_dir ='/data/02/elutsch/MOPITT/'
#start, end = dt.date(1999,1,1),dt.date(2017,1,1)
#site = 'Eureka'

#if __name__ == "__main__":
def read_mopitt(site,start,end):

    	dates = [start + dt.timedelta(days=x) for x in range((end-start).days)]
    	dataMOPITT = []
	found, missing = 0, 0

    	for date in dates:
		mopitt_file = os.path.join(main_dir,site,site+'_MOPITT_'+date.strftime('%Y%m%d')+'.txt')
	
		if os.path.isfile(mopitt_file):
			temp = pd.read_csv(mopitt_file,header=None,sep=' ', \
				names = ['i','datetime','latitude','longitude','column','error','dx'])
			time = []
			for x in np.array(temp['datetime']):
				try: 
					time_new = dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
				except:
					time_new = dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
					#time.append((time_new-dt.datetime(2000,1,1,0,0,0)).total_seconds())
				time.append(time_new)	    
			temp['datetime'] = np.array(time)

			found += 1 
			dataMOPITT.append(temp)
			del temp
		else:
			missing += 1

	print '\n MOPITT Files Found: '+str(found)+' Files missing: '+str(missing)
	dataMOPITT = pd.concat(dataMOPITT) 
	dataMOPITT.index = pd.to_datetime(dataMOPITT['datetime'])
	del dataMOPITT['i']

	return dataMOPITT


	

