"""
infra:
  events:
  - name: my-website-event
    pattern:
      object:
        key:
        - prefix: hello
      reason:
      - PutObject
    source:
      name: #{AppName}
      type: website
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
    bucketname=os.environ["#{WebsiteKey}"]
    s3=boto3.client("s3")
    s3key=event["detail"]["object"]["key"]
    print (s3key)

