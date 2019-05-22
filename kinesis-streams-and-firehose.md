# Kinesis Streams and Firehose Demo

## Make Bucket

Replace this bucket name with your own unique bucket name.

```bash
aws s3 mb s3://asimj-tmp1
```

## Create Schema

In Athena run this query.

```sql
-- Setup 
CREATE DATABASE demo1;
CREATE EXTERNAL TABLE IF NOT EXISTS demo1.sales (
  id INT, amount DOUBLE) 
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://asimj-tmp1/data/'
```

## Kinesis Data Streams

Next we will create a Kinesis Data Stream that will be consumed by two Kinesis Firehose Streams.

- Create a Kinesis Data Stream called `sales-kinesis`.
    - Configure it with a single shard.
 - Create a Kinesis Firehose Stream called `sales-json`.
    - Configure it to consume records from `sales-kinesis`.
    - Configure it to write to S3 at `s3://asimj-tmp1` with prefix `sales-json`.
 - Create a Kinesis Firehose Stream called `sales-parquet`.
    - Configure it to consume records from `sales-kinesis`.
    - Enable data format conversion to Parquet with schema `demo1.sales`.
    - Configure it to write to S3 at `s3://asimj-tmp1` with prefix `sales-json`.

## Put Records

Next let's put some records into this stream.

```bash
aws kinesis put-record --stream-name "sales-kinesis" --data '{"id":101,"amount":10.0}' --partition-key 101
aws kinesis put-record --stream-name "sales-kinesis" --data '{"id":101,"amount":10.0}' --partition-key 101
aws kinesis put-record --stream-name "sales-kinesis" --data '{"id":101,"amount":10.0}' --partition-key 101
```

Repeat this several times.

## Observe S3

Now let's observe the data arriving in S3.

```bash
aws s3 ls s3://asimj-tmp1 --recursive
```

Dump the contents of individual files to screen.

```bash
aws s3 cp s3://asimj-tmp1/sales-json/path - 
```

The records we published should be in both locations.

## Cleanup

In Athena, delete the table and database.

```sql
-- Cleanup
DROP TABLE `demo1.sales`;
DROP DATABASE demo1;
```
