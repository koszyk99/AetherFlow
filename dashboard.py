import boto3
import pandas as pd
from tabulate import tabulate
import os
import time

def get_stats():
    # connect to LocalStack (DynamoDB)
    endpoint = "http://localhost:4566"
    dynamodb = boto3.resource(
        'dynamodb',
        endpoint_url=endpoint,
        region_name="us-east-1"
    )

    table = dynamodb.Table('FraudSentinel_Result')

    try:
        # download data from DynamoDB
        response  = table.scan()
        items     = response.get('Items', [])

        if not items:
            print("\n" + "="*65)
            print(" [!] Database is empty.")
            print(" Upload JSON files to S3 for Lambda to process.")
            print("="*65)
            return

        # processing data into a readable table
        df = pd.DataFrame(items)
        df['amount'] = pd.to_numeric(df['amount'])

        # calculating statistics
        total_tx = len(df)
        flagged  = df[df['status'] == 'FLAGGED']
        total_fraud_value = flagged['amount'].sum()

        # rendering the dashboard in the terminal
        os.system('clear')
        print("="*65)
        print("                AETHERFLOW - LIVE MONITORING")
        print("="*65)
        print(f" STATUS: OPERATIONAL | Transactions: {total_tx} | SNS alerts: {len(flagged)}")
        print(f" Total Blocked Amount: {total_fraud_value:.2f} USD")
        print("-" * 65)

        # table of the last 10 records
        cols = ['transaction_id', 'amount', 'status']
        print(tabulate(df[cols].tail(10),
                       headers=['S3 Object Key', 'Sum (USD)', 'Status'],
                       tablefmt='grid'))

        print(f"\n Last update: {time.strftime('%H:%M:%S')}")
        print("="*65)

    except Exception as e:
        print(f"\n [!] Communication error with LocalStack: {e}")
        print(" Make sure 'terraform apply' has been executed and LocalStack is running.")

if __name__ == "__main__":
    get_stats()
