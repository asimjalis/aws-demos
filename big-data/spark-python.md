# Python Spark 

## Install Spark

Install Spark from <http://spark.apache.org>. 

Configure your environment.

```sh
export SPARK_HOME=${HOME}/spark-2.3.0-bin-hadoop2.7
export PATH=${PATH}:${SPARK_HOME}/bin
```

## IPython Shell

```sh
PYSPARK_DRIVER_PYTHON=ipython pyspark
```

## RDD

```python
# RDD of simple types.
rdd = sc.parallelize([1,2,3,4])
rdd.map(lambda x: x + 1).collect()

# RDD of tuples.
rdd = sc.parallelize([["chicago",1],["new york",2]])
rdd.map(lambda (city,i): (city,i+1)).collect()

# Convert to data frame.
df = rdd.toDF()
df.registerTempTable('sales')
df.selectExpr('count(*)').show()
spark.sql('select count(*) from sales').show()
```

## Data Frames From CSV

```python
df = spark.read.csv('sales-data')
df.show()
df.printSchema()

df = spark.read.option("inferSchema",True).csv('sales-data')
df.printSchema()

df = df.toDF('id','date','store','state','product','amount')
df.printSchema()
```

## Data Frame Analytics

```python
# Sample
df.sample(0.5).show()

# Project 
df.select('state', 'amount').show()
df.drop('id').show()
df.withColumn('tax',df.amount * 0.15).show()

# Sort
df.orderBy('amount').show()
df.orderBy(df.amount).show()
df.orderBy(df.amount.desc()).show()
df.orderBy(df.state, df.amount).show()

# Filter
df.filter(df.amount > 500).show()

# Group By
df.groupBy('state').agg({'amount':'sum'}).show()
df.groupBy('state').agg({'amount':'max','product':'count'}).show()
```
