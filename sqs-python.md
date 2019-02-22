```python
# Test SQS.
import boto3

# Pretty print.
import pprint
pp = pprint.PrettyPrinter(indent=2)

# Create queue.
sqs = boto3.resource('sqs')
queue = sqs.create_queue(QueueName='test')
print(queue.url)

# Get existing queue.
queue = sqs.get_queue_by_name(QueueName='test')
print(queue.url)

# Get all queues.
for queue in sqs.queues.all(): print queue

# Send message.
response = queue.send_message(MessageBody='world')
pp.pprint(response)

# Send batch.
response = queue.send_messages(Entries=[
    { 'Id': '1', 'MessageBody': 'world' },
    { 'Id': '2', 'MessageBody': 'hello' } ])
pp.pprint(response)

# Process and delete all messages.
for message in queue.receive_messages():
    pp.pprint(message)
    message.delete()
```
