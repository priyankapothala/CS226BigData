# Rank cities in US by the quality of life

## Dependencies
- Python
- PySpark
- NodeJS
- MongoDB

## For Spatial processing
- geospark.jar
- geospark-sql.jar
- geo_wrapper.jar
- geoPandas
- geoSpark


## Steps to run

### Spark
Navidage to ```spark``` folder and run the following command.
```
spark-submit main.py
```
Rename the processed csv file in ```spark/result``` folder to ```cities.csv``` and place this csv file in ```cs266-node```

### Mongodb
Navigate to cs226-node and run the following commands.
```
$ chmod +x db-start.sh
$ ./db-start.sh
```

### Web UI

Navigate to cs226-node and install the dependencies using
```
$ npm install
```
Run ```node db.js``` to upload the data to mongodb. Now run ```npm start``` from the terminal and the Web UI can now be accessed at ```http://localhost:8000```
