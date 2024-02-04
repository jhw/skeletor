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

def handler(event, context=None,
            bucketname=os.environ["#{WebsiteKey}"],
            tablename=os.environ["#{TableKey}"]):
    s3key=event["detail"]["object"]["key"]
    print (s3key)
