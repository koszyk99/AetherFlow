import json
import boto3
import os

# connect to DynamoDB
def lambda_handler(event, context):
    lh = os.environ.get('LOCALSTACK_HOSTNAME', 'localhost')
    endpoint = f"http://{lh}:4566"

    s3_client = boto3.client(
        's3',
        endpoint_url=endpoint,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )

    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=endpoint,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )

    table = dynamodb.Table('FraudSentinel_Result')

    # download ARN topic from Terraform
    topic_arn = "arn:aws:sns:us-east-1:000000000000:fraud-alerts-topic"

    # process data from a file that has been uploaded to S3
    for record in event['Records']:
        bucket  = record['s3']['bucket']['name']
        key     = record['s3']['object']['key']

        # downloading
        try:
            response = s3_client.get_object(Bucket=bucket, Key=key)
            file_content = response['Body'].read().decode('utf-8')

            data = json.loads(file_content)
            amount = data.get('amount', 0)
            status = 'FLAGGED' if amount > 1000 else 'APPROVED'

            # recording to the dynamodb
            table.put_item(Item={
                'transaction_id': key,
                'amount': amount,
                'status': status,
                'source': bucket
            })

            # SNS alert (only if FLAGGED)
            if status == 'FLAGGED':
                sns_client.publish(
                    TopicArn=topic_arn,
                    Subject="Alert: High Value Transaction Detected",
                    Message=f"Warning! Transaction {key} from {bucket} has a high amount: {amount}. Status: {status}"
                )
                print(f"Alert sent for {key}")

        except Exceptation as e:
            print(f"Error parsing {key}: {str(e)}")
            status = 'ERROR'


    return {'StatusCode': 200}
