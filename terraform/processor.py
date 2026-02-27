import json
import boto3
import os

# connect to DynamoDB
def lambda_handler(event, context):
    lh = os.environ.get('LOCALSTACK_HOSTNAME', 'localhost')
    endpoint = f"http://{lh}:4566"

    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=endpoint,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )

    table = dynamodb.Table('FraudSentinel_Result')

    # process data from a file that has been uploaded to S3
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"Processing: {key} from {bucket}")


        # here, the transaction validation logic would be
        transaction_data = {
            'transaction_id': key,
            'status': 'PROCESSED',
            'source': bucket
        }

        # save result to database
        table.put_item(Item=transaction_data)

    return {'StatusCode': 200}
