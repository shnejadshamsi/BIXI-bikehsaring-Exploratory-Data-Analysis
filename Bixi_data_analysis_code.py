from datetime import datetime
import pandas as pd
import numpy as np
import os
import glob
os.chdir("C:/Users/test/Desktop/Milad_project/BIXI/Data/2019")

# I first begin by loading the station info.
stationInfo = pd.read_csv('C:/Users/test/Desktop/Milad_project/BIXI/Data/2019/Stations_2019.csv', encoding='utf8', dtype={"Code": int, "name": str, "latitude": float, "longitude": float})

stationInfo.head()
print (stationInfo.head())

# I'll use the directory listing list to more easily load the separate CSV files into one dataframe
#fileList = os.listdir('C:/Users/test/Desktop/Milad_project/BIXI/Data/2019')
#print(fileList)

extension = 'csv'
fileList = [i for i in glob.glob('*.{}'.format(extension))]
print(fileList)


date_cols = ["start_date","end_date"]
data=pd.concat([pd.read_csv(f, dtype={"Code": int, "name": str, "latitude": float, "longitude": float, "start_station_code": int, "end_station_code": int,"duration_sec": int,"is_member": bool}, parse_dates=date_cols) for f in fileList],)

#data = pd.concat([pd.read_csv(fileName) for fileName in fileList])

#'C:/Users/test/Desktop/Milad_project/BIXI/Data/2019/'+fileName,encoding='utf8', dtype={"Code": int, "name": str, "latitude": float, "longitude": float}

# data.loc[:,'start_date'] = pd.to_datetime(data['start_date'])
# data.loc[:,'end_date'] = pd.to_datetime(data['end_date'])
# data['tripStartHour'] = data['start_date'].dt.hour

