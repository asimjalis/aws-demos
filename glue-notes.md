# AWS Glue Notes

## Use Cases

What are the use cases for Glue?

- Define *tables* in Data Catalog.
- Define *crawlers* to populate Data Catalog.
- Define *connections* to access JDBC databases.
- Define *jobs* to transform data sets across schema.

## Crawlers

What data sources can crawlers analyze?

- S3
- Redshift
- RDS
- JDBC

How do crawlers decide what to crawl?

- Crawlers crawl data sources you specify. 
- You can exclude paths in the data sources.

What happens when a crawler runs?

- Classifies data to determine format, schema, and properties (e.g. whether it is compressed).
- Groups data into tables or partitions. 
- Writes metadata to the Data Catalog.

What happens if the crawler finds a duplicate table name?

- Adds hash string to keep table names unique within a database.

What type of scheduling do crawlers support?

- Regular or on-demand. 

## Classifiers

What is a classifier?

- Crawlers use classifiers to extract schema from data.
- Glue has built-ins, and also allows custom classifiers.
- Custom classifiers have higher precedence than the built-in classifiers.
- The first classifier to recognize your data is used.

What do classifiers output?

- Data format (e.g. JSON)
- Schema
- Certainty number

What custom classifiers does Glue support?

- Grok
- JSON
- XML

How do custom classifers work?

- You specify patterns and associated field names.
- When the classifier encounters the pattern it names the field.

What is Grok?

- Pattern language used in Elasticsearch.
- Patterns look like this: `%{PATTERN:FieldName}`.
- Example: `%{TIMESTAMP_ISO8601:timestamp} %{GREEDYDATA:message}`
- `TIMESTAMP_ISO8601` and `GREEDYDATA` are defined using regex.
- Glue provides common built-in patterns e.g. `INT`, `UNIXPATH`, `IPV4`.

How do JSON and XML classifiers work?

- For JSON you specify the JSON path expression that maps JSON elements to table rows.
- For XML you specify the row tag that maps the XML elements to table rows.

## Jobs

How can I author jobs?

- Specify source schema, target schema, and transformation using GUI.
- Glue generates code for you.
- Customize the code. 

How are jobs triggered?

- Schedule
- Job events
- On-demand

## Development Workflow

How can I develop the code for the jobs?

- Use Glue to create a development endpoint.
- Either generate a public-private key pair.
- Or you can get the public key from your pem file and upload it.
- Here is how: `openssl rsa -in my-key.pem -pubout -out my-key.pub`
- SSH to the endpoint using the SSH commands in the console.

## Pricing

How does Glue pricing work?

- Crawlers and jobs are billed in Data Processing Unit (DPU).
- Each DPU provides 4 vCPU and 16 GB of memory.
- The current price is $0.44 per DPU-hour. 
- There is a 10-minute minimum.
- This information was last updated May 30, 2018.

## Job Bookmarks

What are Job Bookmarks?

- Glue uses job bookmarks to keep track of data processed by a job.
- For example, if you are processing data in S3, job bookmarks will track which files have successfully been processed.
- The goal is to prevent duplicate processing and duplicate data in the target data store.

## ETL Programming 

Where can I find out more about Glue and Glue ETL programming?

- Use the [Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html).

What languages does Glue ETL support?

- Python
- Scala

What does Glue ETL code look like?

- You can see an example of a Glue ETL application [here](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-samples-legislators.html).
