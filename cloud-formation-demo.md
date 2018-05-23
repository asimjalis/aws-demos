# CloudFormation

## Overview

We will create a CloudFormation stack containing an SQS queue and two
lambdas. The first lambda will take a string and enqueue it. The
second will dequeue a string and return it.

## Template

Save this into a file called `demo.yaml`.

```yaml
Resources:
  MessageQueue:
    Type: "AWS::SQS::Queue"

  MessageProducerLambda:
    Type: "AWS::Lambda::Function"
    Properties: 
      Handler: "index.handler"
      Role: !Sub ${MessageQueueAccessRole.Arn}
      Runtime: "python2.7"
      Timeout: "60"
      Environment:
        Variables:
          MessageQueueName: !Sub ${MessageQueue.QueueName}
      Code:
        ZipFile: |
            import os
            import boto3

            # This runs once on container initialization.
            sqs = boto3.resource('sqs')
            queue_name = os.environ.get("MessageQueueName")
            queue = sqs.get_queue_by_name(QueueName=queue_name)

            # This runs on each invocation.
            def handler(event, context):
                # Convert event to string in case it is JSON object.
                message_body = str(event)
                queue.send_message(MessageBody=message_body)

  MessageConsumerLambda:
    Type: "AWS::Lambda::Function"
    Properties: 
      Handler: "index.handler"
      Role: !Sub ${MessageQueueAccessRole.Arn}
      Runtime: "python2.7"
      Timeout: "60"
      Environment:
        Variables:
          MessageQueueName: !Sub ${MessageQueue.QueueName}
      Code:
        ZipFile: |
            import os
            import boto3

            # This runs once on container initialization.
            sqs = boto3.resource('sqs')
            queue_name = os.environ.get("MessageQueueName")
            queue = sqs.get_queue_by_name(QueueName=queue_name)

            # This runs on each invocation.
            def handler(event, context):
                # Return None (meaning null) if no messages received.
                messages = queue.receive_messages(MaxNumberOfMessages=1)
                if len(messages) == 0: 
                    return None
                else:
                    message = messages[0]
                    message.delete()
                    return message.body

  MessageQueueAccessRole:
    Type: "AWS::IAM::Role"
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal: { Service: lambda.amazonaws.com }
            Action: "sts:AssumeRole"
      Path: "/"
      Policies:
        - PolicyName: LambdaExecutionPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement: 
              - Effect: Allow
                Action: ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"]
                Resource: "*"
              - Effect: Allow
                Action: ["sqs:*"]
                Resource: !Sub ${MessageQueue.Arn}
Outputs:
  MessageProducerName:
    Value: !Sub ${MessageProducerLambda}
  MessageConsumerName:
    Value: !Sub ${MessageConsumerLambda}
  MessageQueueName:
    Value: !Sub ${MessageQueue.QueueName}
```

## Deploy

Next let's deploying the template. 

```bash
# Give CloudFormation stack unique name.
StackName=s1; 

# Deploy stack. Needs CAPABILITY_IAM since creating roles.
aws cloudformation deploy \
  --stack-name $StackName \
  --template-file demo.yaml \
  --capabilities CAPABILITY_IAM
```

## Get Function and Queue Names

Next let's get the names of the functions and the queue. 

I deliberately did not specify the names in the CloudFormation
resources. If I had hard-coded the names I would get name collisions
if I deployed the template twice.

Much better to let CloudFormation auto-generate the names. The names
are based on the stack name and the logical names of the resources.
This makes them meaningful and recognizable. This is what they look
like:

```
s13-MessageProducerLambda-177VR7VN5P1UY
s13-MessageConsumerLambda-18AFJ54AHMIF
s13-MessageProducerLambda-177VR7VN5P1UY
```

Except there is no risk of conflicts.

Let's save the names in environment variables.

```bash
# Get message producer function name from stack outputs.
MessageProducerLambda=$(aws cloudformation describe-stacks \
  --stack-name $StackName \
  --query "Stacks[].Outputs[?OutputKey=='MessageProducerName'][].OutputValue" \
  --output text) 
echo $MessageProducerLambda 

# Get message consumer function name from stack outputs.
MessageConsumerLambda=$(aws cloudformation describe-stacks \
  --stack-name $StackName \
  --query "Stacks[].Outputs[?OutputKey=='MessageConsumerName'][].OutputValue" \
  --output text) 
echo $MessageConsumerLambda 

# Get message queue name from stack outputs.
MessageQueueName=$(aws cloudformation describe-stacks \
  --stack-name $StackName \
  --query "Stacks[].Outputs[?OutputKey=='MessageProducerName'][].OutputValue" \
  --output text) 
echo $MessageQueueName 
```

## Test

Let's test the stack. We will send some messages to the producer. The
producer will enqueue them on the queue. Then we will get the consumer
to retrieve them from the queue and return them to us.

```bash
# Send some messages to the queue.
aws lambda invoke \
  --function-name $MessageProducerLambda \
  --payload '"Message 1"' \
  out.txt ; cat out.txt ; echo
aws lambda invoke \
  --function-name $MessageProducerLambda \
  --payload '"Message 2"' \
  out.txt ; cat out.txt ; echo 
aws lambda invoke \
  --function-name $MessageProducerLambda \
  --payload '"Message 3"' \
  out.txt ; cat out.txt ; echo

# Receive the messages from the queue.
aws lambda invoke \
  --function-name $MessageConsumerLambda \
  out.txt ; cat out.txt ; echo
aws lambda invoke \
  --function-name $MessageConsumerLambda \
  out.txt ; cat out.txt ; echo
aws lambda invoke \
  --function-name $MessageConsumerLambda \
  out.txt ; cat out.txt ; echo

# Try receiving more messages.
aws lambda invoke \
  --function-name $MessageConsumerLambda \
  out.txt ; cat out.txt ; echo
aws lambda invoke \
  --function-name $MessageConsumerLambda \
  out.txt ; cat out.txt ; echo
aws lambda invoke \
  --function-name $MessageConsumerLambda \
  out.txt ; cat out.txt ; echo
```

# Delete

One of the neat things about CloudFormation is that clean up is easy:
delete the stack and all its resources go away.

```bash
# Delete the stack.
aws cloudformation delete-stack \
  --stack-name $StackName
```
