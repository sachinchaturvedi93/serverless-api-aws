import boto3

def lambda_handler(event, context):
    ddbClient = boto3.resource('dynamodb')
    ddbTable = ddbClient.Table('items')
    response = ddbTable.put_item(
        Item={
            'id': event['queryStringParameters']['id'],
            'name': event['queryStringParameters']['name']
        }
    )
    return {
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
        'body': 'Record ' + event['queryStringParameters']['id'] + ' Updated'
    }
