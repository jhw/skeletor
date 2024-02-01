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

def handler(event, context=None,
            bucketname=os.environ["#{BucketKey}"],
            tablename=os.environ["#{TableKey}"]):
    for record in event["Records"]:
        message=json.loads(record["Sns"]["Message"])
        print (message)
