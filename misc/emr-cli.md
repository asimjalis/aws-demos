## Create Cluster

```bash
cluster_id=$(aws emr create-cluster \
  --name "Test Cluster" \
  --release-label emr-5.13.0 \
  --log-uri s3://asimj-tmp/tmp-emr/logs/ \
  --applications Name=Hadoop Name=Hive Name=Spark \
  --use-default-roles \
  --ec2-attributes KeyName=isen \
  --instance-type m3.xlarge \
  --instance-count 3 
  --query ClusterId \
  --output text)

echo $cluster_id
```

## Describe Cluster

```bash
aws emr describe-cluster \
  --cluster-id "$cluster_id" 

aws emr describe-cluster \
  --cluster-id "$cluster_id" \
  --query Cluster.Status.State
```

## Terminate Cluster

```bash
aws emr terminate-clusters \
  --cluster-ids $cluster_id 
```

