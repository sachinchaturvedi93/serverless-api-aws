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
        responseObject['body'] = json.dumps(response['Item')]
        return responeObject
    else:
        return {
            'statusCode': '404',
            'body': 'Not found'
        }
