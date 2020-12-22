from pyspark.sql import SparkSession
from pyspark.sql.functions import split, trim, col, regexp_replace, round
import time

if __name__ == "__main__":
    spark = SparkSession.builder.master("local").appName('CS226').getOrCreate()
    start_time = time.time()
    statesDF = spark\
        .read\
        .format("csv")\
        .options(inferschema='true', header='true')\
        .load('Datasets/states.csv')

    wagesDF = spark\
        .read\
        .format("csv")\
        .options(inferschema='true', header='true')\
        .load('Datasets/min_wage.csv')\
        .withColumnRenamed('2020 Minimum Wage', 'min_wage')\
        .drop('2021 Minimum Wage')\
        .join(statesDF, ['State'], how='inner')\


    """
    SUMLEV = 040 indicates state
    SUMLEV = 050 indicates county
    """
    censusDF = spark\
        .read\
        .format("csv")\
        .options(inferschema='true', header='true')\
        .load('Datasets/sub-est2019_all.csv')\
        .filter("SUMLEV <> 050 and SUMLEV <> 040 and POPESTIMATE2019 > 50000 and lower(NAME) not like '%balance%'")\

    newCensusDF = censusDF.withColumn("NAME", regexp_replace(col("NAME"), ' city', ''))\
        .withColumn("NAME", regexp_replace(col("NAME"), ' village', ''))\
        .withColumn("NAME", regexp_replace(col("NAME"), ' \(pt\.\)', ''))

    censusFinalDF = newCensusDF.selectExpr(
        "NAME as City",
        "STNAME as State",
        'POPESTIMATE2010 as population')\
        .join(statesDF, ['State'], how='left')\
        .dropDuplicates(['City', 'State'])

    citiesDF = spark\
        .read\
        .format("csv")\
        .options(inferschema='true', header='true')\
        .load('Datasets/cities_new.csv')

    parksDF = spark\
        .read\
        .format("csv")\
        .options(inferschema='true', header='true')\
        .load('Datasets/lakes_parks.csv')

    newCitiesDF = citiesDF.join(parksDF,['State', 'City'],how='inner')

    finalDF = newCitiesDF.join(censusFinalDF, ['State', 'City', 'Abbreviation'], how='inner')\
        .join(wagesDF, ['State', 'Abbreviation'], how='inner')

    resultDF = finalDF.dropDuplicates(['City', 'State'])\
        .withColumn('quality_of_life',
                    round((100 + col('safety_index')/2.0 + col('health_care_index')/2.5 - col('traffic_index')/2.0 - (col('pollution_index') * 2.0 / 3.0) +
                     col('population')/50000 - col('min_wage')/2.5 + col('rent_index') / 2.5 + col('parks_count')/3.0 + col('lakes_count') / 2.0 - col('property_price_to_income_ratio') +col('safety_index') * 2.0),2)
                    ).drop('coordinates')

    #resultDF.selectExpr('City','quality_of_life').show(50)
    resultDF.coalesce(1).write.format("csv").mode('overwrite').option("header", "true").save('result')

    print("--- Execution time %s seconds ---" % (time.time() - start_time))
