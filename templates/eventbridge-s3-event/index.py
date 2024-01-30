"""
infra:
  events:
  - name: my-s3-event
    pattern:
      object:
        key:
        - prefix: hello
      reason:
      - PutObject
    source:
      name: #{AppName}
      type: bucket
  permissions: []
"""

import boto3, json, os

def handler(event, context=None,
            bucketname=os.environ["#{BucketKey}"],
            tablename=os.environ["#{TableKey}"]):
    s3key=event["detail"]["object"]["key"]
    print (s3key)

