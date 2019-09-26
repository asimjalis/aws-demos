# Python Spark 

## Install Spark

Install Spark from <http://spark.apache.org>. 

Configure your environment.

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 1.8)
export SPARK_HOME=$(find $HOME/Downloads -maxdepth 1 -name 'spark*bin*' | 
  grep -v tgz | tail -n 1)
export PATH=${PATH}:${SPARK_HOME}/bin
```

## IPython Shell

```sh
PYSPARK_DRIVER_PYTHON=ipython
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

## Create Data

In a Bash shell, run these commands.

```bash
# Create directory.
mkdir sales-data

# Data file.
#ID,Date,Store,State,Product,Amount
cat << END > sales-data/file1.csv
101,2014-11-13,100,WA,331,300.00
104,2014-11-18,700,OR,329,450.00
102,2014-11-15,203,CA,321,200.00
106,2014-11-19,202,CA,331,330.00
103,2014-11-17,101,WA,373,750.00
105,2014-11-19,202,CA,321,200.00
END
```

## DataFrames From CSV

In the PySpark shell run these commands.

```python
df = spark.read.csv('sales-data')
df.show()
df.printSchema()

df = spark.read.option("inferSchema",True).csv('sales-data')
df.printSchema()

df = df.toDF('id','date','store','state','product','amount')
df.printSchema()
```

## DataFrame API

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

## SQL on DataFrames

We can use SQL instead of the DataFrame API.

```python
df.registerTempTable('sales')
spark.sql('select SUM(amount) FROM sales').show()
```
