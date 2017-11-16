""" Modified Nov. 7 2017 
Read in all HDF files from specified directory for specified gas
""" 

from pyhdf import SD
import os
##################################################################################
import numpy as np
import pandas as pd
import datetime as dt
##################################################################################
def read_ftir(FILE_NAME):
    """ Read NDACC HDF file. File and variable names to be specified by user
    when under name == main """
    
    hdf=SD.SD(FILE_NAME)
    
    # read attributes 
    lst = hdf.attributes()
    var = lst['DATA_VARIABLES'].split(';')
    data = [] 

    #----------------------------------------
    for v in var:
	#--------------------------------    
	try:
	    sds = hdf.select(v)
	    data.append(sds.get())     
	except:
	    print 'No SDS found: '+v
	    var.pop(v)           
	#-------------------------------- 	    

    #----------------------------------------
    return var, data[0], data[1], data[2], data[6], data[7], data[8:]
    
#if __name__ == '__main__':

def read_hdf(hdf_dir,spec):

#    hdf_dir = sys.argv[1]
    
    files = [x for x in os.listdir(hdf_dir) if x.endswith('.hdf')]

    dataFTIR = pd.DataFrame()
    
    for f in files:
        gas = f.split('_')[1][5:].strip()
        GAS = ''.join(map(lambda x:x.upper(),gas)).replace('L','l')

	if GAS == spec:
	    start_date = dt.datetime.strptime(f.split('_')[4][:8],'%Y%m%d').date()
	    end_date = dt.datetime.strptime(f.split('_')[5][:8],'%Y%m%d').date()	    
		    
	    file_name = os.path.join(hdf_dir,f)
	    var, date, lat, lon, ftir_alt, ftir_levels, data_temp = read_ftir(file_name)
	    ftir_dz = np.array(ftir_levels[0]-ftir_levels[1]) 
	    ftir_data = []
		    
	    # -------------------------------------------------------------------------
	    # Convert FTIR Data to DataFrame
	    # -------------------------------------------------------------------------    
    
	    for k in map(list,zip(date,*data_temp)):
		dtm_mjd2k_s = k[0]
		k[0] = dt.datetime(2000,1,1,0,0,0)+dt.timedelta(days=np.float64(dtm_mjd2k_s))
		k.insert(1,ftir_alt)
		k.insert(2,ftir_dz) 
		ftir_data.append(k)
		    
	    ftir_data = np.array(ftir_data)
	    dataFTIR = dataFTIR.append(pd.DataFrame(ftir_data,columns=['DATETIME','ALTITUDE', 'LAYER.THICKNESS']+var[8:]))
    
    dataFTIR.index = pd.to_datetime(dataFTIR['DATETIME'])
    dataFTIR = dataFTIR.sort_values('DATETIME') 
    
    #del dataFTIR['DATETIME']
    
    # Redimension variables to correct array sizes  
    #date = str(dataFTIR.index[0])
    #for var in dataFTIR.iterkeys()
    
    #dataFTIR = pd.to_numeric(dataFTIR)
    
    return dataFTIR

	
