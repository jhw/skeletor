"""
infra:
  queue: {}
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
        body=json.loads(record["body"])
        print (body)
