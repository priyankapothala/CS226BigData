#!/usr/bin/env python
# coding: utf-8

# In[1]:


import shapely
import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Qol").getOrCreate()


# In[3]:


import geopandas as gpd

from geospark.register import upload_jars
from geospark.register import GeoSparkRegistrator
upload_jars()
GeoSparkRegistrator.registerAll(spark)


# In[4]:


import requests
#get cities co-ordinates
with open('all_cities_census.txt') as f:
        content = f.readlines();

cities = [x.strip() for x in content]


# In[5]:


json_obj ={
    "type":"FeatureCollection",
    "features":[]
}
for c in cities:
    City = c.split(',')[0]
    state = c.split(',')[1]
    response = requests.get('https://nominatim.openstreetmap.org/search.php?q='+City+", "+state+'&polygon_geojson=1&format=json')
    if response:
        data = response.json()
        try:        
            geo_json= data[0]['geojson'];
            json_obj["features"].append({
                "type":"Feature",
                "properties":{
                    "State":state,
                    "City": City
                },
                "geometry":geo_json
            })
        except:
            print("Exception occured for City,", City)
    else:
        print("error occured for City,", City)
    

import json
with open('City.json', 'w') as f:
    json.dump(json_obj, f)


# In[6]:


cities = gpd.read_file('City.json')


# In[ ]:


#Read the parks 
parks = gpd.read_file('OSM2015_parks_data_index.geojson')


# In[ ]:


#Read the lakes 

parks = gpd.read_file('OSM2015_lakes_data_index.geojson')


# In[ ]:


lakes.createOrReplaceTempView("lakes")
cities.createOrReplaceTempView("cities")

cities_lakes_join_result = spark.sql(
    """SELECT c.City,c.State,c.geometry
        FROM cities AS c, lakes AS l
        WHERE ST_Intersects(c.geometry, l.geometry)""")


# In[ ]:


#groupby_count

cities_lakes_join_result.createOrReplaceTempView("cities_lakes")
cities_to_lakes=spark.sql("""SELECT c.City,c.State, count(*) as lakes_count
        FROM cities_lakes As c Groupby c.City, c.State """)


# In[ ]:


# write the dataframe to csv


# In[ ]:


parks.createOrReplaceTempView("parks")
cities.createOrReplaceTempView("cities")

cities_park_join = spark.sql(
    """SELECT c.City,c.State,c.geometry
        FROM cities AS c, parks AS p
        WHERE ST_Intersects(c.geometry, p.geometry)""")


# In[ ]:


# groupby count


cities_park_join.createOrReplaceTempView("cities_park")
cities_to_parks=spark.sql("""SELECT c.City,c.State, count(*) as parks_count
        FROM cities_park As c Groupby c.City, c.State """)


# In[ ]:


#join to df's 
cities_to_lakes.createOrReplaceTempView("cities_to_lakes")
cities_to_parks.createOrReplaceTempView("cities_to_parks")

City_park_lakes = spark.sql(
    """SELECT c.City,c.State,c.lakes_count,l.parks_count
        FROM cities_to_lakes AS c Inner Join cities_to_parks AS l on c.City=l.City and c.State=l.State""")


# In[ ]:


temp_df=City_park_lakes.toPandas()
temp_df.to_csv("Datasets/lakes_parks.csv",index=False)

