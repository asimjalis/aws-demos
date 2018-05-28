# CloudWatch Metrics

## Get Lambda Metrics

Assume the function name is `hello`.

- Here is how to get metrics on invocations using Bash.
    ```sh
    FUNC_NAME=hello
    aws cloudwatch get-metric-statistics \
      --namespace "AWS/Lambda" \
      --metric-name "Invocations" \
      --dimensions \
          Name=FunctionName,Value="$FUNC_NAME" \
          Name="Resource",Value="$FUNC_NAME" \
      --start-time $(date -u '+%FT%TZ' -d "6 hours ago")  \
      --end-time $(date -u '+%FT%TZ')  \
      --period 3600 \
      --statistics SampleCount
    ```
- Here is how to get metrics on invocations using PowerShell.
    ```powershell
    $FUNC_NAME = "hello"
    aws cloudwatch get-metric-statistics `
      --namespace "AWS/Lambda" `
      --metric-name "Invocations" `
      --dimensions "Name=FunctionName,Value=$FUNC_NAME Name=Resource,Value=$FUNC_NAME" `
      --start-time ((Get-Date).AddHours(-6) | Get-Date -Format o) `
      --end-time (Get-Date -Format o) `
      --period 3600 `
      --statistics SampleCount
    ```

