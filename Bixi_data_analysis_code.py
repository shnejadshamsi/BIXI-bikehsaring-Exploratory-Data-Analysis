import pandas as pd
import numpy as np
import os

# I first begin by loading the station info.
stationInfo = pd.read_csv('C:/Users/test/Desktop/Milad_project/BIXI/Data/2019/Stations_2019.csv', encoding='utf8')



# I'll use the directory listing list to more easily load the separate CSV files into one dataframe
fileList = os.listdir('C:/Users/test/Desktop/Milad_project/BIXI/Data/2019')
print(fileList)

data = pd.concat([pd.read_csv('C:/Users/test/Desktop/Milad_project/BIXI/Data/2019/'+fileName,encoding='utf8')
                   for fileName in fileList[1:-1]],
                  sort=False,ignore_index=True)

data.loc[:,'start_date'] = pd.to_datetime(data['start_date'])
data.loc[:,'end_date'] = pd.to_datetime(data['end_date'])
data['tripStartHour'] = data['start_date'].dt.hour

stationInfo.head()