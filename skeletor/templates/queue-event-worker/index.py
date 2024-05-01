"""
infra:
  events:
  - name: my-table-event
    pattern:
      eventName:
      - INSERT
      pk:
      - HEAD
      sk:
      - ITEM
    source:
      name: #{AppName}
      type: table
  permissions:
  - dynamodb:GetItem
  - dynamodb:PutItem
  - dynamodb:UpdateItem
  - s3:GetObject
  - s3:PutObject
"""

import boto3, json, os

def handler(event, context=None):
    tablename=os.environ["APP_TABLE"]
    table=boto3.resource("dynamodb").Table(tablename)
    bucketname=os.environ["APP_BUCKET"]
    s3=boto3.client("s3")
    body=event["detail"]
    print (body)


