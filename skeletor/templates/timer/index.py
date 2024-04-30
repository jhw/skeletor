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
    tablename=os.environ["APP_TABLE"]
    table=boto3.resource("dynamodb").Table(tablename)
    bucketname=os.environ["APP_BUCKET"]
    s3=boto3.client("s3")
    print (event)
