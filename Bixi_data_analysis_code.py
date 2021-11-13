import pandas as pd
import numpy as np
import os
import glob
os.chdir("C:/Users/test/Desktop/Milad_project/BIXI/Data/2019")

from IPython.display import Image
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib


# I first begin by loading the station info.
stationInfo = pd.read_csv('C:/Users/test/Desktop/Milad_project/BIXI/Data/2019/Stations_2019.csv', encoding='utf8', 
dtype={"Code": int, "name": str, "latitude": float, "longitude": float})

stationInfo.head()
print (stationInfo.head())


print ('-------------------------------------------------------------------------------------------------')

# I'll use the directory listing list to more easily load the separate CSV files into one dataframe
fileList = os.listdir('C:/Users/test/Desktop/Milad_project/BIXI/Data/2019')

#extension = 'csv'
#fileList = [i for i in glob.glob('*.{}'.format(extension))]

print(fileList)

print ('-------------------------------------------------------------------------------------------------')
#data1 = pd.read_csv("C:/Users/test/Desktop/Milad_project/BIXI/Data/2019/OD_2019-04.csv", nrows=1)
#print(data1)
#data1.info()
#print ('-------------------------------------------------------------------------------------------------')


#from datetime import datetime
#dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')


dfs = []
for fileName in fileList :
    dfs.append(pd.read_csv(fileName))

data=pd.concat(dfs, ignore_index=True)


#data = pd.concat([pd.read_csv('C:/Users/test/Desktop/Milad_project/BIXI/Data/2019/'+fileName,encoding='utf8')
 #                 for fileName in fileList[1:-1]],
 #                 sort=False,ignore_index=True)


#dtype={"Code": int, "name": str, "latitude": float, "longitude": float, "start_station_code": int, "start_date": object, "end_date": object, "end_station_code": int,"duration_sec": int,"is_member": int}


data.loc[:,'start_date'] = pd.to_datetime(data['start_date'])
data.loc[:,'end_date'] = pd.to_datetime(data['end_date'])
data['tripStartHour'] = data['start_date'].dt.hour

print (data.head())

print ('--------------------------------------------------------------------------------------------')

print(data[['duration_sec','is_member']].describe().style.format('{:.2f}'))

print ('--------------------------------------------------------------------------------------------')

print(data['duration_sec'].quantile(0.99))

print ('--------------------------------------------------------------------------------------------')

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
        lat=stationInfo['latitude'],
        lon=stationInfo['longitude'],
        text=stationInfo['name']
    )
)

fig.update_layout(
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=open('mapboxToken.txt','r').read(),
        center=go.layout.mapbox.Center(
            lat=stationInfo['latitude'].mean()-0.0075,
            lon=stationInfo['longitude'].mean()),
        zoom=11
        )    
)

#fig.show()
img_bytes = fig.to_image(format="jpg",width=1200,height=1000)
Image(img_bytes)


print ('--------------------------------------------------------------------------------------------')


fig = go.Figure()

fig.add_trace(go.Histogram(x=data['tripStartHour']))
fig.update_layout(title='Bixi Bikeshare Usage by Time of Day - 2019',
    shapes=[
    go.layout.Shape(
        type='line',
        yref='paper',
        x0=x,
        x1=x,
        y0=0,
        y1=1,
        line={'color':'black','dash':'longdash'}
    )
    for x in [5.5,9.5,15.5,18.5]]
)


fig.show()
Image(fig.to_image(format="jpg",width=1200,height=1000))
#Image(img_bytes)
fig.savefig('C:/Users/test/Desktop/Milad_project/BIXI/Data/2019')


print ('--------------------------------------------------------------------------------------------')


fig = make_subplots(rows=2, cols=2)

rowsCols = [(1,1),(1,2),(2,1),(2,2)]
labels = ['Weekday Members','Weekend Members','Weekday Non-Members','Weekend Non-Members']


member = (data['is_member']==1)
nonmember = (data['is_member']==0)
weekday = (data['start_date'].dt.weekday<5)
weekend = (data['start_date'].dt.weekday>=5)
masks = [(member & weekday),(member & weekend),(nonmember & weekday),(nonmember & weekend)]

for mask,label,rowCol in zip(masks, labels, rowsCols):
    fig.add_trace(go.Histogram(
            x=data.loc[mask,'tripStartHour'],
            histnorm='percent',
            name=label),
        row=rowCol[0],col=rowCol[1])

fig.update_layout(title='Percentage Histograms of Bixi Usage, by Membership and Time of Week - 2019',
                 legend_orientation='h')
fig.update_xaxes(title='Hour of Day',)
fig.show()
Image(fig.to_image(format="jpg",width=1200,height=600))