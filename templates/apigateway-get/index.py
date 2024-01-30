"""
infra:
  endpoint:
    api: public
    method: GET
    path: hello
    parameters:
    - foobar
  permissions:
  - dynamodb:Query
  - s3:GetObject
"""

import boto3, json, os

def handler(event, context=None,
            bucketname=os.environ["#{BucketKey}"],
            tablename=os.environ["#{TableKey}"]):
    try:
        table, s3 = (boto3.resource("dynamodb").Table(tablename),
                     boto3.client("s3"))
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

