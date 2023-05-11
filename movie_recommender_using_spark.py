# -*- coding: utf-8 -*-
"""movie_recommender_using_spark.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/4k5h1t/PySpark-Movie-Rec/blob/main/movie_recommender_using_spark.ipynb

# Movie Recommender Systems using Spark with PySpark

## Installing required dependencies
"""

!pip install findspark
!pip install pyspark

"""## Downloading the Dataset"""

!apt-get install -y aria2
!mkdir -p ./MovieLens/ 
!aria2c -s 16 -x 16 "https://files.grouplens.org/datasets/movielens/ml-25m.zip" -d ./MovieLens/

"""## Downloading SPARK and Java Dependencies"""

!apt-get install openjdk-8-jdk-headless -qq > /dev/null

!wget -q https://archive.apache.org/dist/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz

!tar xf spark-3.2.1-bin-hadoop3.2.tgz

"""## Extracting the Dataset"""

import zipfile
with zipfile.ZipFile("/content/MovieLens/ml-25m.zip", 'r') as zip_ref:
    zip_ref.extractall("/content/MovieLens")

"""## Start Setup Time"""

import time
setupst = time.time()

"""## Setting up SPARK and Java Paths"""

import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.2.1-bin-hadoop3.2"

"""## Importing PySpark"""

import findspark
findspark.init('/content/spark-3.2.1-bin-hadoop3.2')
import pyspark

"""## Starting up Spark Session, Clusters etc. """

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('recommendation').getOrCreate()

"""## Importing ALS model """

from pyspark.ml.recommendation import ALS

"""## Reading loaded Dataset"""

data = spark.read.csv('MovieLens/ml-25m/ratings.csv',inferSchema=True,header=True)
setupet = time.time()

"""## Describing / Showcasing Dataset"""

data.head()

data.printSchema()

data.describe().show()

"""## Implementing ML Algorithm and Evaluation

### Train Test Split
"""

(train_data, test_data) = data.randomSplit([0.7, 0.3], seed=42)
setupTime = setupet - setupst

"""Setting up and Training the ALS Model"""

trainst = time.time()
als = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="movieId", ratingCol="rating")
model = als.fit(train_data)
trainet = time.time()
trainTime = trainet - trainst

"""### Testing trained model"""

testst = time.time()
predictions = model.transform(test_data)
testet = time.time()
testTime = testet - testst

predictions.show()

"""## Extracting information of one user"""

single_user = test_data.filter(test_data['userId']==12).select(['movieId','userId'])

single_user.show()

"""## Running Model again for one selected user (testing)"""

test1st = time.time()
reccomendations = model.transform(single_user)
test1et = time.time()
test1Time = test1et - test1st

reccomendations.orderBy('prediction',ascending=False).show()

"""## Analysing with the help of supporting Datasets (Easier to Understand)"""

moviesdf = spark.read.csv(r"MovieLens/ml-25m/movies.csv", inferSchema = True, header = True)  
moviesdf.show()

"""## Final Predictions with Movie Titles"""

rec = reccomendations
joined = moviesdf.join(rec, ['movieId'],how="inner")
joined.select('userId', 'movieId', 'title', 'genres', 'prediction').orderBy('prediction', ascending=False).show()

print("Time to setup = ", setupTime)
print("Time to train = ", trainTime)
print("Time to test = ", testTime)
print("Time to test1 = ", test1Time)