# CloudFormation EMR Demo

## Create Template

Copy this YAML into `emr1.yaml`.

```yaml
Resources:
  TestCluster: 
    Type: "AWS::EMR::Cluster"
    Properties: 
      Name: MyTestCluster
      TerminationProtected: false
      Ec2KeyName: isen
      Applications:
        - Name: Hadoop
        - Name: Hive
        - Name: Spark
        - Name: Presto
      Instances: 
        MasterInstanceGroup: 
          InstanceCount: 1
          InstanceType: "m3.xlarge"
          Market: "ON_DEMAND"
          Name: "Master"
        CoreInstanceGroup: 
          InstanceCount: 2
          InstanceType: "m3.xlarge"
          Market: "ON_DEMAND"
          Name: "Core"
        TerminationProtected: true
      JobFlowRole: "EMR_EC2_DefaultRole"
      ServiceRole: "EMR_DefaultRole"
      ReleaseLabel: "emr-5.14.0"
      Tags: 
        - Key: "IsTest"
          Value: "True"
  TestInstanceGroupConfig: 
    Type: "AWS::EMR::InstanceGroupConfig"
    Properties: 
      InstanceCount: 2
      InstanceType: "m3.xlarge"
      InstanceRole: "TASK"
      Market: "ON_DEMAND"
      JobFlowId: !Sub ${TestCluster}
```

## Synchronously Deploy Template

```bash
aws cloudformation deploy \
  --stack-name s1 \
  --template-file emr1.yaml
```

## Asynchronously Deploy Template

```bash
aws s3 cp emr1.yaml s3://asimj-tmp/emr1.yaml
aws cloudformation create-stack \
  --stack-name s5 \
  --template-url http://asimj-tmp.s3.amazonaws.com/emr1.yaml
```

