#!/usr/bin/env python
# coding: utf-8

import requests
import json
import pandas as pd
import datetime
from pprint import pprint
import time

#Prepare to load Data Frames with SQLAlchemy
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()


def BikerData():

    url = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Transportation_WebMercator/MapServer/5/query?where=1%3D1&outFields=*&outSR=4326&f=json"

    response = requests.get(url)
    data = response.json()

    obj_id = []
    term_id = []
    address = []
    term_num = []
    lat = []
    lng = []
    installed = []
    locked = []
    install_date = []
    removal_date = []
    temp_install = []
    num_bikes = []
    num_empty_docks = []

    time_stamp = []
 
    now = datetime.datetime.now()
    time = pd.Timestamp(now.year,now.month,now.day,now.hour,now.minute)
    for index,item in enumerate(data["features"]):
        address.append(data["features"][index]["attributes"]["ADDRESS"])
        term_id.append(data["features"][index]["attributes"]["ID"])
        lat.append(data["features"][index]["attributes"]["LATITUDE"])
        lng.append(data["features"][index]["attributes"]["LONGITUDE"])
        num_bikes.append(data["features"][index]["attributes"]["NUMBER_OF_BIKES"])
        num_empty_docks.append(data["features"][index]["attributes"]["NUMBER_OF_EMPTY_DOCKS"])
        # obj_id.append(data["features"][index]["attributes"]["OBJECTID"])
        # term_num.append(data["features"][index]["attributes"]["TERMINAL_NUMBER"])
        # installed.append(data["features"][index]["attributes"]["INSTALLED"])
        # locked.append(data["features"][index]["attributes"]["LOCKED"])
        # install_date.append(data["features"][index]["attributes"]["INSTALL_DATE"])
        # removal_date.append(data["features"][index]["attributes"]["REMOVAL_DATE"])
        # temp_install.append(data["features"][index]["attributes"]["TEMPORARY_INSTALL"])
        time_stamp.append(time)

    biker_data = {"time":time_stamp,"term_id": term_id, "address": address, "lat": lat, "long": lng, "num_bikes":num_bikes,
                  "num_empty_docks":num_empty_docks}






#to do... read API feed.  pull down information.  add to dictionary/list.  compare to previous dictionary/list
#if difference between empty docks, then add data to new list with lats/longs.  add lat/long list to ping layer  



    biker_data = pd.DataFrame(biker_data)
    biker_data.to_sql(name='bikeshare', if_exists='append', con=conn, index=False)
    
    with open('bike_data.csv', 'a') as f:
        biker_data.to_csv(f, header=False,index=False)

while(True):
    BikerData()
    time.sleep(60)




