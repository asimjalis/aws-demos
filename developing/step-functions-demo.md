# Step Functions

## State Machine

Create state machine with this JSON.

```json
{
  "StartAt": "A",
  "States": {
    "A": {
      "Type": "Pass",
      "Next": "B"
    },
    "B": {
      "Type": "Pass",
      "Next": "C"
    },
    "C": {
      "Type": "Pass",
      "End": true
    }
  }
}
```

# I/O Processing

## Simple

Create state machine with this JSON.

```json
{
  "StartAt": "A",
  "States": {
    "A": {
      "Type": "Pass",
      "Result": "A!",
      "ResultPath": "$.a",
      "OutputPath": "$",
      "Next": "B"
    },
    "B": {
      "Type": "Pass",
      "Result": "B!",
      "ResultPath": "$.b",
      "OutputPath": "$",
      "Next": "C"
    },
    "C": {
      "Type": "Pass",
      "Result": "C!",
      "ResultPath": "$.c",
      "OutputPath": "$",
      "End": true
    }
  }
}
```

## Calculate Amount

Create state machine with this JSON.

```json
{
  "StartAt": "CreateOrder",
  "States": {
    "CreateOrder": {
      "Type": "Pass",
      "Result": { 
        "Order" :  {
          "Customer" : "Alice",
          "Product" : "Coffee",
          "Billing" : { "Price": 10.0, "Quantity": 4.0 }
        }
      },
      "Next": "CalculateAmount"
    },
    "CalculateAmount": {
      "Type": "Pass",
      "Result": 40.0,
      "ResultPath": "$.Order.Billing.Amount",
      "OutputPath": "$.Order.Billing",
      "End": true
    }
  }
}
```

## Output

What will the state machine produce?

```json
{
  "output": {
    "initial": "Initial input object",
    "a": "A!",
    "b": "B!",
    "c": "C!"
  }
}
```

# Task 

## Lambda Task

Create CloudFormation stack with this YAML.

```javascript
AWSTemplateFormatVersion: "2010-09-09"
Description: "Step Functions using Lambda."
Resources:
  LambdaExecutionRole:
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
            Statement: [ { Effect: Allow, Action: [ "logs:*" ], Resource: "*" } ]
  StatesExecutionRole:
    Type: "AWS::IAM::Role"
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: "Allow"
            Principal: { Service: !Sub "states.${AWS::Region}.amazonaws.com" }
            Action: "sts:AssumeRole"
      Path: "/"
      Policies:
        - PolicyName: StatesExecutionPolicy
          PolicyDocument:
            Version: "2012-10-17"
            Statement: [
              { Effect: Allow, Action: [ "lambda:InvokeFunction" ], Resource: "*" }
            ]

  CalculateAmountFunction:
    Type: "AWS::Lambda::Function"
    Properties:
      Handler: "index.handler"
      Role: !GetAtt [ LambdaExecutionRole, Arn ]
      Code:
        ZipFile: |
          exports.handler = (event, context, callback) => {
            var price = event.price;
            var quantity = event.quantity;
            var amount = price * quantity
            callback(null, amount);
          };
      Runtime: "nodejs4.3"
      Timeout: "60"

  OrderProcessingMachine:
    Type: "AWS::StepFunctions::StateMachine"
    Properties:
      DefinitionString:
        !Sub
          - |-
            {
              "Comment": "Input should look like {'price':3.12,'quantity':4}",
              "StartAt": "CalculateAmount",
              "States": {
                "CalculateAmount": {
                  "Type": "Task",
                  "Resource": "${CalculateAmountFunctionArn}",
                  "End": true,
                  "ResultPath": "$.amount"
                } 
              } 
            }
          - { CalculateAmountFunctionArn: !GetAtt [CalculateAmountFunction,Arn] }
      RoleArn: !GetAtt [ StatesExecutionRole, Arn ]
```

## Testing

After the stack is created go to *Step Functions*. 

You should see the *OrderProcessing* machine. 

Execute the machine with this input.

```json
{"price": 4.00, "quantity": 7}
```

## Output

What should the output be?

```json
{"price":4.0,"quantity":7,"amount":28}
```

## I/O Processing

Where did `amount` come from?

- From the `ResultPath`.

To clean up delete the CloudFormation stack.

# Choice

## Choice State Machine

Create state machine with this JSON.

```json
{
  "Comment" : "Input should look like {'tea':'green'}",
  "StartAt": "MakeTea",
  "States" : {
    "MakeTea": {
      "Type": "Choice",
      "Choices": [
        {"Variable":"$.tea","StringEquals":"green","Next":"Green"},
        {"Variable":"$.tea","StringEquals":"black","Next":"Black"}
      ],
      "Default": "Error"
    },
    "Green": { "Type": "Pass", "End": true, "Result": "Green tea" },
    "Black": { "Type": "Pass", "End": true, "Result": "Black tea" },
    "Error": { "Type": "Pass", "End": true, "Result": "Bad input" }
  }
}
```

# Activity

## Approving Orders

Bash: Create activity. 

```bash
activity_name="ApproveOrder"
aws stepfunctions create-activity --name $activity_name
aws stepfunctions list-activities
activity_arn=$(aws stepfunctions list-activities --query 'activities[].activityArn' --output text)
echo $activity_arn 
```

PowerShell: Create activity.

```bash
$activity_name = "ApproveOrder"
aws stepfunctions create-activity --name $activity_name
aws stepfunctions list-activities
$activity_arn = aws stepfunctions list-activities --query 'activities[].activityArn' --output text
echo $activity_arn 
```

Create state machine and execute it.

```json
{
  "Comment" : "Wait for order approval.",
  "StartAt": "WaitForOrderApproval",
  "States" : {
    "WaitForOrderApproval": {
      "Type": "Task",
      "Resource": "arn:aws:states:us-west-2:861469877924:activity:ApproveOrder",
      "TimeoutSeconds": 3600,
      "Next": "OrderApproved"
    },
    "OrderApproved": { "Type": "Pass", "End": true }
  }
}
```

Get activity task token.

```bash
aws stepfunctions get-activity-task --activity-arn $activity_arn 
```

Bash: Paste task token into variable below.

```bash
activity_task_token=
```

PowerShell: Paste task token into variable below.

```bash
$activity_task_token =
```

Approve order.

```bash
aws stepfunctions send-task-success --task-output "123" --task-token $activity_task_token
```

Verify that the state machine execution now shows success.

To clean up delete activity.

```bash
aws stepfunctions delete-activity --activity-arn $activity_arn
```

## Observations

- `get-activity-task` blocks until activity is available.
- Activity is not tied to specific state machine--could be from any state machine.
- Worker has to submit output of its work back to activity.
- Worker has to complete task within timeout or the task fails.
- Worker has to send heartbeats if activity requires heartbeats or task fails.

# Parallel

## State Machine 

```json
{
  "StartAt": "FindCustomerInfo",
  "States": {
    "FindCustomerInfo": {
      "Type": "Parallel",
      "Branches": [
        { 
          "StartAt": "FindAddress",
          "States": { 
            "FindAddress": { 
              "Type": "Pass", 
              "Result": "123 Main", 
              "ResultPath": "$.Address",
              "End": true 
            } 
          }
        },
        { 
          "StartAt": "FindPhone",
          "States": { 
            "FindPhone": { 
              "Type": "Pass", 
              "Result": "555-1212", 
              "ResultPath": "$.Phone",
              "End": true 
            } 
          }
        },
        {
          "StartAt": "Wait",
          "States": { 
            "Wait": { 
              "Type": "Wait", 
              "Seconds":1,
              "End": true 
            }
          }
        }
      ],
      "Next": "Done"
    },
    "Done": { "Type":"Pass", "End":true } 
  }
}
```

## Observations

- `Parallel` waits until all the branches are done.
- `Parallel` gives a copy of the input to each branch.
- Each branch injects its result in its copy of the data.


