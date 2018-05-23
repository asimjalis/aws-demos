# CloudWatch Metrics

## Get Lambda Metrics

Assume the function name is `hello`.

Use this to get metrics on its invocation.

```sh
FUNC_NAME=hello
aws cloudwatch get-metric-statistics \
  --namespace "AWS/Lambda" \
  --metric-name "Invocations" \
  --dimensions \
      Name=FunctionName,Value="$FUNC_NAME" \
      Name="Resource",Value="$FUNC_NAME" \
  --start-time $(date -u '+%FT%TZ' -d "6 hours ago")  \
  --end-time $(date -u '+%FT%TZ' -d "1 hours ago")  \
  --period 3600 \
  --statistics SampleCount
```

