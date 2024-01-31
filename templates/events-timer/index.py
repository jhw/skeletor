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

def handler(event, context=None,
            bucketname=os.environ["#{BucketKey}"],
            tablename=os.environ["#{TableKey}"]):
    print (event)
