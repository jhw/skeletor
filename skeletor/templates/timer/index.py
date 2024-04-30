"""
infra:
  permissions:
  - sqs:SendMessage
  timer:
    rate: "1 hour"
    body:
      hello: world
"""

import boto3, json, os

def handler(event, context=None):
    tablename=os.environ["#{TableKey}"]
    table=boto3.resource("dynamodb").Table(tablename)
    bucketname=os.environ["#{BucketKey}"]
    s3=boto3.client("s3")
    print (event)
