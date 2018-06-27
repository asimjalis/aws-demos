# S3 Demo

## Test API

```python
import boto3

key='1.txt'
file1_path='1.txt'
file2_path='2.txt'

with open(file1_path, "w") as f: 
    f.write("Hello world!!")

s3 = boto3.client('s3')

# Create bucket
bucket_name = 'asimj-demo'
s3.create_bucket(Bucket=bucket_name)
print s3.list_buckets()

# Upload file.
s3.upload_file(file1_path, bucket, key)

# Download file.
s3.download_file(bucket, key, file2_path)

# Check content.
with open(file2_path, "r") as f:
    print f.read()
```

## Test List

```bash
# Create bucket
aws s3 mb s3://asimj-iad

# Put some objects in it
echo "hello world" > 1.txt
aws s3 cp 1.txt s3://asimj-iad/a/b/c/1.txt
aws s3 cp 1.txt s3://asimj-iad/a-b-c-1.txt
```

```python
import boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket('asimj-iad')

for f in bucket.objects.all(): print f

for f in bucket.objects.filter(Prefix='').all(): print f

for f in bucket.objects.filter(Prefix='',Delimiter='/').all(): print f

# Treat "/" as folder delimiter.
for f in bucket.objects.filter(Prefix='a/b/c/',Delimiter='/').all(): print f

# Treat "-" as folder delimiter.
for f in bucket.objects.filter(Prefix='',Delimiter='-').all(): print f
```
