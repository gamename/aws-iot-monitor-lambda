import boto3
from datetime import datetime, timedelta
import time
import json
import os

arn = os.environ.get('SNS_ARN')

if not arn:
    raise Exception('SNS_ARN not provided')

client = boto3.client('logs')

query = "fields @timestamp, @message, @logStream | filter @message like /MSG00[34]/ | sort @timestamp desc | limit 20"

log_group = 'AWSIotLogsV2'

start_query_response = client.start_query(
    logGroupName=log_group,
    startTime=int((datetime.today() - timedelta(hours=12)).timestamp()),
    endTime=int(datetime.now().timestamp()),
    queryString=query,
)

query_id = start_query_response['queryId']

response = None

while response is None or response['status'] == 'Running':
    print('Waiting for query to complete ...')
    time.sleep(1)
    response = client.get_query_results(
        queryId=query_id
    )

if not response['results']:
    print("No results found. Sending SMS")
    message = {"MSG005": "Monitor offline"}
    client = boto3.client('sns')
    response = client.publish(
        TargetArn=arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
else:
    for result in response['results']:
        print(result)