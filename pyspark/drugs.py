from pyspark import SparkContext
from pyspark.sql import SQLContext
import json
import requests

sc = SparkContext(appName='analyzeDrugs')
sqlContext = SQLContext(sc)

# TODO : there are ~24 million records! should we process them all?
url = 'https://data.cms.gov/resource/uggq-gnqc.json?$limit=100000'
r = requests.get(url)

df = sqlContext.createDataFrame(r.json())
df.average_drug_day_cost = df['total_day_supply']/df['total_drug_cost']

grouped = df.groupby('generic_name')
sorted_group_counts = grouped.count().sort("count", ascending=False).collect()


