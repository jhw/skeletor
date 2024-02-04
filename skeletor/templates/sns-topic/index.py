"""
infra:
  topic: {}
  permissions:
  - dynamodb:GetItem
  - dynamodb:PutItem
  - dynamodb:UpdateItem
  - s3:GetObject
  - s3:PutObject
"""

import boto3, json, os

def handler(event, context=None):
    tablename=os.environ["#{TableKey}"]
    table=boto3.resource("dynamodb").Table(tablename)
    bucketname=os.environ["#{BucketKey}"]
    s3=boto3.client("s3")
    for record in event["Records"]:
        message=json.loads(record["Sns"]["Message"])
        print (message)
