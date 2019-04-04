#!/usr/bin/env python
# coding: utf-8

import requests
import json
import pandas as pd
import datetime
import time

#Prepare to load Data Frames with SQLAlchemy
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

#from config import remote_db_endpoint, remote_db_port
#from config import remote_gwsis_dbname, remote_gwsis_dbuser, remote_gwsis_dbpwd

# AWS Database Info - Put in Config file!
remote_db_endpoint = 'gwcodingbootcamp.cr0gccbv4ylw.us-east-2.rds.amazonaws.com'
remote_db_port = '3306'
remote_gwsis_dbname = 'bikeshare_db'
remote_gwsis_dbuser = 'root'
# ADD PASSWORD HERE FOR AWS DATABASE - i know i shouldn't put it, 
#but couldn't get separate users to work
remote_gwsis_dbpwd = 'braddocks'

# AWS Database Connection
engine = create_engine(f"mysql://{remote_gwsis_dbuser}:{remote_gwsis_dbpwd}@{remote_db_endpoint}:{remote_db_port}/{remote_gwsis_dbname}")
# Create a remote database engine connection
conn = engine.connect()

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
        obj_id.append(data["features"][index]["attributes"]["OBJECTID"])
        term_num.append(data["features"][index]["attributes"]["TERMINAL_NUMBER"])
        installed.append(data["features"][index]["attributes"]["INSTALLED"])
        locked.append(data["features"][index]["attributes"]["LOCKED"])
        install_date.append(data["features"][index]["attributes"]["INSTALL_DATE"])
        removal_date.append(data["features"][index]["attributes"]["REMOVAL_DATE"])
        temp_install.append(data["features"][index]["attributes"]["TEMPORARY_INSTALL"])
        time_stamp.append(time)

    biker_data = {"time":time_stamp,"term_id": term_id, "address": address, "lat": lat, "long": lng, "num_bikes":num_bikes,
                "num_empty_docks":num_empty_docks, "obj_id":obj_id,"term_num":term_num,"installed":installed, 
                "locked":locked,"install_date":install_date,"removal_date":removal_date,"temp_install":temp_install}
    #print(biker_data["time"][0])
    biker_df = pd.DataFrame(biker_data)
    biker_df.to_sql(name='bikeshare', if_exists='append', con=conn, index=False)

def periodic_work(interval):
    while(True):
        BikerData()
        time.sleep(interval)

periodic_work(180)





