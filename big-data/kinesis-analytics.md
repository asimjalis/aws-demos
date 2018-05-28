# Kinesis Analytics

## Kinesis Analytics Limits

Element | Limit
------- | -----
Row size | 512 KB
SQL code | 100 KB
Mapping parallelism | 64
Destination streams | 3

Note: Kinesis uses 1 KB of metadata which counts against row size.

## Metadata

- Source stream called `SOURCE_SQL_STREAM_001`
- Metadata columns: `ROWTIME`, `PARTITION_KEY`, `SEQUENCE_NUMBER`

## Column Names

- Unquoted column names uppercased automatically.
- To force lowercase, quote column names.
- Use uppercase column names in destination tables, to minimize quotes.

## Producer

```sh
aws kinesis create-stream --stream-name donut-sales --shard-count 2
aws kinesis list-streams
aws kinesis describe-stream --stream-name "donut-sales"
aws kinesis put-record \
  --stream-name 'donut-sales' \
  --data '{"flavor":"chocolate","quantity":12}' \
  --partition-key "on"
```

## Generate Random Data

```sh
flavors=(chocolate glazed apple birthday)
locations=(on qc bc ab)
quantities=(1 6 12 20 40)
while true ; do 
  date
  flavor=${flavors[RANDOM%${#flavors[@]}]} 
  location=${locations[RANDOM%${#locations[@]}]} 
  quantity=${quantities[RANDOM%${#quantities[@]}]} 
  aws kinesis put-record \
    --stream-name 'donut-sales' \
    --data '{ "flavor":"'$flavor'", "quantity":"'$quantity'" }' \
    --partition-key $location; 
  sleep 1
done 
```

## Continuous 

```sql
CREATE OR REPLACE STREAM SALES (
    FLAVOR VARCHAR(256), 
    PRICE DECIMAL, 
    QUANTITY INTEGER,
    LOCATION VARCHAR(256)
);

CREATE OR REPLACE PUMP SOURCE_TO_SALES AS 
INSERT INTO SALES
SELECT STREAM "flavor", "price", "quantity", PARTITION_KEY AS LOCATION
FROM SOURCE_SQL_STREAM_001;
```

## Tumbling Window 

```sql
CREATE OR REPLACE STREAM SALES_BY_LOCATION (
    LOCATION VARCHAR(256),
    LOCATION_COUNT INTEGER
);

CREATE OR REPLACE PUMP SALES_TO_SALES_BY_LOCATION AS 
INSERT INTO SALES_BY_LOCATION
SELECT STREAM LOCATION, COUNT(*) AS LOCATION_COUNT
FROM SALES
GROUP BY LOCATION, STEP(SALES.ROWTIME BY INTERVAL '60' SECOND);
```

## Sliding Window

```sql
CREATE OR REPLACE STREAM SALES_BY_FLAVOR (
    FLAVOR VARCHAR(256),
    FLAVOR_COUNT INTEGER
);

CREATE OR REPLACE PUMP SALES_TO_SALES_BY_FLAVOR AS 
INSERT INTO SALES_BY_FLAVOR
SELECT STREAM FLAVOR, COUNT(*) OVER SLIDING_WINDOW AS FLAVOR_COUNT
FROM   SALES
WINDOW SLIDING_WINDOW AS (
   PARTITION BY LOCATION
   RANGE INTERVAL '30' SECOND PRECEDING);
```

