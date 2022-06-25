# Serverless REST API with AWS Lambda (and Github Actions)

## Overview
Serverless REST API using AWS Lambda(Python), connected to API Gateway to AWS DynamoDB table. Configured CI/CD with Github Actions. We'll create a GET and PUT endpoint to retrieve and update item information in the DynamoDB table.

## Resources
1. AWS Account with appropriate IAM access_key_id and secret_access_key
2. DynamoDB table `items` with partition key as `id`
3. Default Lambda IAM Role for the GET and PUT lambdas to read and write to `items` DDB table
4. Two lambda functions `get_item_lambda` and `put_item_lambda` with Python 3.8 as runtime
5. Github account with git configured on your local workspace

## To Do
Create a Github repository, `serverless-api-aws` in my case. Create folder for each operation GET/PUT. Add the source code as added in the above folders. Sample code for reference taken from `serverless-api-aws/GET/lambda_function.py`: 
```
import boto3
import json

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('items')
    response = table.get_item(
        Key={
            'id': event['queryStringParameters']['id']
        }
    )
    if 'Item' in response:
        responseObject = {}
        responseObject['statusCode'] = 200
        responseObject['headers'] = {}
        responseObject['headers']['Content-Type'] = 'application/json'
        responseObject['body'] = json.dumps(response['Item'])
        return responseObject
    else:
        return {
            'statusCode': '404',
            'body': 'Not found'
        }
```
Above is a simple lambda function to retrieve data from `items` DDB table based on the `id` provided. The `id` would be passed to the event of the lambda_handler and will be used to retrieve the response from the `items` DDB table.

Please check `serverless-api-aws/PUT/lambda_function.py` for PUT operation.

Now go to Github Actions and create a new workflow, set up a workflow yourself and update the main.yml file with the following config : 
Thanks to the [AWS Lambda Deploy](https://github.com/marketplace/actions/aws-lambda-deploy) Github Action. We can deploy code to an existing lambda function using this action. 
```
name: deploy to lambda
on: [push]
jobs:

  deploy_source:
    name: deploy lambda from source
    runs-on: ubuntu-latest
    steps:
      - name: checkout source code
        uses: actions/checkout@v1
      - name: default deploy
        uses: appleboy/lambda-action@master
        with:
          aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws_region: ${{ secrets.AWS_REGION }}
          function_name: get_item_lambda
          source: GET/lambda_function.py
```


