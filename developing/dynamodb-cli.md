# DynamoDB Demo

```bash
aws dynamodb create-table \
  --table-name MusicCollection \
  --attribute-definitions \
      AttributeName=Artist,AttributeType=S \
      AttributeName=SongTitle,AttributeType=S \
  --key-schema \
      AttributeName=Artist,KeyType=HASH \
      AttributeName=SongTitle,KeyType=RANGE \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

aws dynamodb put-item \
  --table-name MusicCollection \
  --item '{
      "Artist":     {"S": "No One You Know"},
      "SongTitle":  {"S": "Call Me Today"},
      "AlbumTitle": {"S": "Somewhat Famous"} }' \
  --return-consumed-capacity TOTAL

aws dynamodb get-item \
  --table-name MusicCollection \
  --key '{ "Artist": {"S": "No One You Know"}, "SongTitle": {"S": "Call Me Today"} }'

aws dynamodb get-item \
  --table-name MusicCollection \
  --key '{ "Artist": {"S": "Acme Band"}, "SongTitle": {"S": "Happy Day"} }'

aws dynamodb scan \
  --table-name MusicCollection

aws dynamodb scan \
  --table-name MusicCollection \
  --filter-expression "Artist = :a" \
  --projection-expression "#ST, #AT" \
  --expression-attribute-names '{"#ST":"SongTitle","#AT":"AlbumTitle"}' \
  --expression-attribute-values '{":a":{"S":"No One You Know"}}'

aws dynamodb query \
  --table-name MusicCollection \
  --projection-expression "SongTitle" \
  --key-condition-expression "Artist = :v1" \
  --expression-attribute-values '{ ":v1": {"S": "No One You Know"} }'

aws dynamodb delete-table \
  --table-name MusicCollection

aws dynamodb describe-table \
  --table-name MusicCollection
```

