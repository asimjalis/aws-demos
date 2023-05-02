import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Setup context.
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read DynamicFrame.
dynf = glueContext.create_dynamic_frame.from_catalog(
        database = "default", 
        table_name = "sales", 
        transformation_ctx = "dynf")

# Convert to DataFrame.
df = dynf.toDF()

# Put table on DataFrame.
df.createOrReplaceTempView("sales_tmp")

# Run SQL.
sql_df = spark.sql("SELECT id, date, store, state, product, amount * 2.1 from sales_tmp")

# Convert back to DynamicFrame.
dynf_new = DynamicFrame.fromDF(sql_df, glueContext, "df")
datasink4 = glueContext.write_dynamic_frame.from_catalog(
        frame = dynf_new,
        database = "default", 
        table_name = "sales1", 
        transformation_ctx = "datasink4")

# Commit.
job.commit()
