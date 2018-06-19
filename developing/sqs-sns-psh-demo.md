# SQS and SNS

Here is how to subscribe SQS queues to SNS topics.

```bash
# Create SNS Topics and capture their ARNs.
$email_topic_arn = aws sns create-topic --name "EmailSNSTopic" --output text --query TopicArn
$order_topic_arn = aws sns create-topic --name "OrderSNSTopic" --output text --query TopicArn

# Subscribe email address to topic.
aws sns subscribe --topic-arn $email_topic_arn --protocol "email" `
  --notification-endpoint "foo@abc.com"

# Create queues.
aws sqs create-queue --queue-name "MySQSQueue_A"
aws sqs create-queue --queue-name "MySQSQueue_B"

# Get account ID and region.
$account_id = aws sts get-caller-identity --output text --query Account
$region = aws configure get region

# Generate queue ARNs.
$queue_a_arn = "arn:aws:sqs:${region}:${account_id}:MySQSQueue_A"
$queue_b_arn = "arn:aws:sqs:${region}:${account_id}:MySQSQueue_B"

# Subscribe queues to OrderSNSTopic.
aws sns subscribe --topic-arn $order_topic_arn --protocol sqs --notification-endpoint $queue_a_arn
aws sns subscribe --topic-arn $order_topic_arn --protocol sqs --notification-endpoint $queue_b_arn

# Get the queue subscription ARNs.
$queue_a_sub_arn = aws sns list-subscriptions --output text `
  --query "Subscriptions[?ends_with(Endpoint,'MySQSQueue_A')].SubscriptionArn" 

$queue_b_sub_arn = aws sns list-subscriptions --output text `
  --query "Subscriptions[?ends_with(Endpoint,'MySQSQueue_B')].SubscriptionArn" 

# Print subscriptions.
aws sns list-subscriptions

# Print topics ARNs.
echo $email_topic_arn
echo $order_topic_arn

# Print queue ARNs.
echo $queue_a_arn
echo $queue_b_arn

# Print queue subscription ARNs.
echo $queue_a_sub_arn
echo $queue_b_sub_arn
```
