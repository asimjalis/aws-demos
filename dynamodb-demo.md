```python
import boto3

# Pretty print.
import pprint
pp = pprint.PrettyPrinter(indent=2)

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Check if table exists.
def table_exists(table_name):
    for table in dynamodb.tables.all():
        if table.name == table_name: return True
    return False

# Create table.
def table_create(table_name, partition_key, sort_key):
    table = dynamodb.create_table(TableName=table_name,
        KeySchema=[
            { 'AttributeName': partition_key, 'KeyType': 'HASH'  },
            { 'AttributeName': sort_key,      'KeyType': 'RANGE' } ],
        AttributeDefinitions=[
            { 'AttributeName': partition_key, 'AttributeType': 'S' },
            { 'AttributeName': sort_key,      'AttributeType': 'S' } ],
        ProvisionedThroughput={ 'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5 })

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    return table

# Create table.
if table_exists('orders'): 
    dynamodb.meta.client.delete_table(TableName='orders')
table = table_create('orders', 'customer', 'order')

# Put item.
table.put_item(Item={ 'customer': 'alice', 'order': '001', 'product': 'coffee', 'price': 100 })
response = table.get_item(Key={ 'customer': 'alice', 'order': '001' })
pp.pprint(response)

# Put item. Notice that price can be string: no type constraints.
table.put_item(Item={ 'customer': 'alice', 'order': '002', 'product': 'coffee', 'price': "hi"})
response = table.get_item(Key={ 'customer': 'alice', 'order': '001' })
pp.pprint(response['Item'])

# Scan all items.
pp.pprint(table.scan()['Items'])

# Update item.
table.update_item(Key={ 'customer': 'alice', 'order': '002' },
    UpdateExpression='SET price = :val1', 
    ExpressionAttributeValues={ ':val1': 26 })
response = table.get_item(Key={ 'customer': 'alice', 'order': '002' })
pp.pprint(response['Item'])

# Scan all items.
pp.pprint(table.scan()['Items'])

# Update item again.
table.update_item(Key={ 'customer': 'alice', 'order': '002' },
    UpdateExpression='SET #foo = :val1', 
    ExpressionAttributeNames={ '#foo': 'price' },
    ExpressionAttributeValues={ ':val1': 27 })
response = table.get_item(Key={ 'customer': 'alice', 'order': '002' })
pp.pprint(response['Item'])

# Scan all items.
pp.pprint(table.scan()['Items'])

# Delete item.
table.delete_item(Key={ 'customer': 'alice', 'order': '001' })

response = table.put_item(Item={ 'customer': 'alice', 'order': '001', 'price': 10})
pp.pprint(response['ResponseMetadata'])
response = table.put_item(Item={ 'customer': 'alice', 'order': '001', 'price': 20})
pp.pprint(response['ResponseMetadata'])

# Massive put.
for i in range(50):
    customer = 'cust' + str(i)
    order = '000'
    response = table.put_item(Item={ 'customer': customer, 'order': order })
    pp.pprint(response)

# Scan all items.
pp.pprint(table.scan()['Items'])

# Batch write.
with table.batch_writer() as batch:
    batch.put_item(Item={ 'customer': 'bob', 'order': '001',
      'product': 'tea', 'price': 5, 
      'address': { 
        'road': '1 Jefferson Street', 'city': 'Los Angeles', 
        'state': 'CA', 'zipcode': 90001 } })
    batch.put_item(Item={ 'customer': 'bob', 'order': '002',
      'product': 'coffee', 'price': 10, 
      'address': { 
        'road': '1 Jefferson Street', 'city': 'Los Angeles', 
        'state': 'CA', 'zipcode': 90001 } })

# Scan all items.
pp.pprint(table.scan()['Items'])

# Querying and scanning.
from boto3.dynamodb.conditions import Key, Attr

# Query.
response = table.query(KeyConditionExpression=Key('customer').eq('alice'))
pp.pprint(response['Items'])

# Scan.
response = table.scan(FilterExpression=Attr('price').lt(12))
pp.pprint(response['Items'])

# Table delete.
table.delete()
```
