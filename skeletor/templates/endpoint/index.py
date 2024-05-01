"""
infra:
  auth: public
  layers: []
  method: GET
  parameters:
  - foobar
  path: hello
  permissions:
  - dynamodb:GetObject
  - dynamodb:Query
  - s3:GetObject
  size: 512
  timeout: 5
  type: endpoint
"""

import boto3, json, os

def handler(event, context=None):
    try:
        tablename=os.environ["APP_TABLE"]
        table=boto3.resource("dynamodb").Table(tablename)
        bucketname=os.environ["APP_BUCKET"]
        s3=boto3.client("s3")
        foobar=event["queryStringParameters"]["foobar"]
        struct=[{"hello": "world"}]
        return {"statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(struct,
                                   indent=2)}
    except RuntimeError as error:
        return {"statusCode": 400,
                "headers": {"Content-Type": "text/plain"},
                "body": str(error)}

