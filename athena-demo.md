# Athena Demo

## Setup

### Install AWSCLI

    pip install --upgrade awscli

### Configure Credentials

Configure `~/.aws/credentials` with your AWS Access Key ID and Secret
Access Key.

## Demo

### Create Sales Data

```bash
#ID,Date,Store,State,Product,Amount
cat << END > sales.csv
101,2014-11-13,100,WA,331,300.00
104,2014-11-18,700,OR,329,450.00
102,2014-11-15,203,CA,321,200.00
106,2014-11-19,202,CA,331,330.00
103,2014-11-17,101,WA,373,750.00
105,2014-11-19,202,CA,321,200.00
END
```

### Make Bucket

Replace this bucket name with your own unique bucket name.

```bash
aws s3 mb s3://asimj-athena-example
```

### Stage Data 

```bash
aws s3 cp sales.csv s3://asimj-athena-example/data/sales.csv
```

### Verify Data

```bash
aws s3 cp s3://asimj-athena-example/data/sales.csv -
```

### Create Table

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
LOCATION 's3://asimj-athena-example/data/'
```

## Show Tables

```sql
SHOW TABLES IN DEFAULT
```

## Sales

```sql
SELECT * FROM SALES LIMIT 10
```

### States With Highest Transaction Count

```sql
SELECT state, COUNT(*) AS count 
FROM sales GROUP BY state ORDER BY count DESC
```

### States With Highest Revenue

```sql
SELECT state, SUM(amount) AS revenue
FROM sales GROUP BY state ORDER BY revenue DESC
```

### Drop Table

```sql
DROP TABLE sales
```


