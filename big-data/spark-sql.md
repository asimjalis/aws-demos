# Spark SQL Demo

## Install Spark

Install Spark: Go to <http://spark.apache.org> then click on
*Download*. Select the latest version and choose package pre-built for
latest version of Apache Hadoop. Download the file. Unpack the
download.


## Configure Spark

Replace `spark-2.3.0` with the latest version of Spark in the
statements below. Configure environment in your `.profile` or
`.bashrc` file by appending these commands.

```sh
export SPARK_HOME=${HOME}/spark-2.3.0-bin-hadoop2.7
export PATH=${PATH}:${SPARK_HOME}/bin
export SPARK_LOCAL_IP=127.0.0.1
```

## Create Data

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

# Start Spark SQL.
spark-sql
```

## Create Table

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS sales (
  id INT,
  date DATE,
  store INT,
  state STRING,
  product INT,
  amount DOUBLE) 
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 'sales-data';

SHOW TABLES;
DESCRIBE SALES;
DESCRIBE FORMATTED sales;
DESCRIBE EXTENDED sales;
```

Note that `LOCATION` is directory, not file.

## Analytics

```sql
SHOW TABLES;

SELECT * FROM SALES;

SELECT state, COUNT(*) AS count 
FROM sales GROUP BY state ORDER BY count DESC;
```

## Cache Table

Can we improve performance with caching?

View state of cache: Go to <http://localhost:4040> and click on
*Storage*.

```
CACHE TABLE sales;

SELECT state, COUNT(*) AS count 
FROM sales GROUP BY state ORDER BY count DESC;

SELECT state, COUNT(*) AS count 
FROM sales GROUP BY state ORDER BY count DESC;

SELECT state, COUNT(*) AS count 
FROM sales GROUP BY state ORDER BY count DESC;
```

View state of cache: Go to <http://localhost:4040> and click on
*Storage*.

## Drop Table

```sql
DROP TABLE SALES;
```

Is the data still there?

```bash
!find sales-data;
```

## Quit

```sql
quit;
```

