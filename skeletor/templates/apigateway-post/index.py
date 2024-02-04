"""
infra:
  endpoint:
    api: private
    method: POST
    path: upload
    schema:
      type: object
      properties: 
        widget:
          $ref: "#/definitions/widgets"
      definitions:
        widget:
          type: object
          properties:
            id:
              type: string
            name:
              type: number
          required:
            - id
            - name
          additionalProperties: false
        widgets:
          type: array
          items:
            "$ref": "#/definitions/widget"
      required: 
      - widgets
      additionalProperties: false
  permissions:
  - dynamodb:BatchWriteItem
  - dynamodb:GetItem
  - dynamodb:PutItem
  - dynamodb:UpdateItem
  - s3:GetObject
  - s3:PutObject
"""

import boto3, json, os

def handler(event, context=None):
    try:
        tablename=os.environ["#{TableKey}"]
        table=boto3.resource("dynamodb").Table(tablename)
        bucketname=os.environ["#{BucketKey}"]
        s3=boto3.client("s3")
        body=json.loads(event["body"])
        return {"statusCode": 200,
                "headers": {"Content-Type": "text/plain"},
                "body": "ok"}
    except RuntimeError as error:
        return {"statusCode": 400,
                "headers": {"Content-Type": "text/plain"},
                "body": str(error)}

