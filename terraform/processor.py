import json
import boto3
import os

# connect to DynamoDB
def handler(event, context):
    dynamodb = boto3.resource('dynamodb', endpoint_url=os.environ.get('LOCALSTACK_ENDPOINT'))
    table = dynamodb.Table('AetherFlow_Transaction')

    # process data from a file that has been uploaded to S3
    for record in event['Records']:
        bucket = record['S3']['bucket']['name']
        key = record['S3']['object']['key']

        print(f"I process file {key} from {bucket}")

        # here, the transaction validation logic would be
        transaction_data = {
            'transaction_id': key,
            'status': 'PROCESSED',
            'source': bucket
        }

        # save result to database
        table.put_item(Item=transaction_data)

    return {
        'StatusCode': 200,
        'body': json.dumps('Transaction processed successfully!')
    }
