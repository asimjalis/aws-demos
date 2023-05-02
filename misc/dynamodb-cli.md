# DynamoDB Demo

```bash
aws dynamodb create-table \
  --table-name sales \
  --attribute-definitions \
      AttributeName=customer,AttributeType=S \
      AttributeName=order,AttributeType=S \
  --key-schema \
      AttributeName=customer,KeyType=HASH \
      AttributeName=order,KeyType=RANGE \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

aws dynamodb put-item \
  --table-name sales \
  --item '{
      "customer": {"S": "alice"},
      "order"   : {"S": "001"},
      "product" : {"S": "coffee"},
      "price"   : {"N": "10"} }' \
  --return-consumed-capacity TOTAL

aws dynamodb put-item \
  --table-name sales \
  --item '{
      "customer": {"S": "alice"},
      "order"   : {"S": "002"},
      "product" : {"S": "sugar"},
      "price"   : {"N": "15"} }' \
  --return-consumed-capacity TOTAL

aws dynamodb put-item \
  --table-name sales \
  --item '{
      "customer": {"S": "alice"},
      "order"   : {"S": "003"},
      "product" : {"S": "half-n-half"},
      "price"   : {"N": "20"} }' \
  --return-consumed-capacity TOTAL

aws dynamodb get-item \
  --table-name sales \
  --key '{ "customer": {"S": "alice"}, "order": {"S": "001"} }'

aws dynamodb get-item \
  --table-name sales \
  --key '{ "customer": {"S": "alice"}, "order": {"S": "002"} }'

aws dynamodb scan \
  --table-name sales

aws dynamodb scan \
  --table-name sales \
  --filter-expression "customer = :a" \
  --projection-expression "#F1, #F2" \
  --expression-attribute-names '{"#F1":"product","#F2":"price"}' \
  --expression-attribute-values '{ ":a" : {"S":"alice"} }'

aws dynamodb query \
  --table-name sales \
  --projection-expression "product" \
  --key-condition-expression "customer = :v1" \
  --expression-attribute-values '{ ":v1": {"S":"alice"} }'

aws dynamodb describe-table \
  --table-name sales

aws dynamodb delete-table \
  --table-name sales
```

