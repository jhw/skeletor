"""
infra:
  alarm:
    period: 60
    threshold: 10
  event:
    pattern:
      detail:
        eventName:
        - INSERT
        pk:
        - HEAD
        sk:
        - ITEM
    type: table
  layers: []
  permissions:
  - dynamodb:GetItem
  - dynamodb:PutItem
  - dynamodb:UpdateItem
  - s3:GetObject
  - s3:PutObject
  size: 512
  timeout: 5
  type: worker
"""

import boto3, json, os

def handler(event, context=None):
    tablename=os.environ["APP_TABLE"]
    table=boto3.resource("dynamodb").Table(tablename)
    bucketname=os.environ["APP_BUCKET"]
    s3=boto3.client("s3")
    for record in event["detail"]["records"]:
        item={k: list(v.values())[0]
              for k, v in record["dynamodb"]["NewImage"].items()}
        print (item)


