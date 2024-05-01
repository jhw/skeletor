"""
infra:
  event:
    rate: 1 hour
  layers: []
  permissions:
  - sqs:SendMessage # because most likely action is to push series of smaller granular timer messages onto a queue
  size: 512
  timeout: 5
  type: timer
"""

import boto3, json, os

def handler(event, context=None):
    tablename=os.environ["APP_TABLE"]
    table=boto3.resource("dynamodb").Table(tablename)
    bucketname=os.environ["APP_BUCKET"]
    s3=boto3.client("s3")
    print (event)
