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
      type: bucket
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
    for record in event["detail"]["records"]:
        item={k: list(v.values())[0]
              for k, v in record["dynamodb"]["NewImage"].items()}
        print (item)


