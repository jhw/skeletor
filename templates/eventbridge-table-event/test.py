from skeletor.test import SkeletorTestBase
from skeletor.test.dynamodb import SkeletorDynamodbTestMixin, TestTable
from skeletor.test.s3 import SkeletorS3TestMixin, TestBucket

from moto import mock_dynamodb, mock_s3

import json, os, unittest, yaml

import unittest.mock as mock

TableFixtures=yaml.safe_load("""
[]
""")

Event=yaml.safe_load("""
---
version: '0'
id: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
detail-type: INSERT
source: my-table-0123456789
account: '0123456789'
time: '2024-01-01T00:00:00Z'
region: eu-west-1
resources: []
detail:
  pk: HEAD
  sk: ITEM
  eventName: INSERT
  diffKeys: []
  records:
  - eventID: a1b2c3d4e5f6g7h8
    eventName: INSERT
    eventVersion: '1.1'
    eventSource: aws:dynamodb
    awsRegion: eu-west-1
    dynamodb:
      ApproximateCreationDateTime: 12345678
      Keys:
        pk:
          S: HEAD
        sk:
          S: ITEM#hello/1970-01-01-00-00-00-0000
      NewImage:
        pk:
          S: HEAD
        sk: 
          S: ITEM#hello/1970-01-01-00-00-00-0000
      SequenceNumber: '1234567890'
      SizeBytes: 1234
      StreamViewType: NEW_AND_OLD_IMAGES
    eventSourceARN: arn:aws:dynamodb:eu-west-1:123456789:table/my-table-0123456789/stream/2024-01-01T00:00:00.000
""")

@mock_dynamodb
@mock_s3
class #{TestClassName}(SkeletorTestBase,                    
                       SkeletorDynamodbTestMixin,
                       SkeletorS3TestMixin):
    
    def setUp(self,
              table=TestTable,
              tablefixtures=TableFixtures,
              bucket=TestBucket):
        self.env={}
        self.setup_dynamodb()
        self.env["#{TableKey}"]=table["name"]
        self.setup_s3()
        self.env["#{BucketKey}"]=bucket["name"]
        with self.tables[0].batch_writer() as batch:
            for fixture in tablefixtures:
                batch.put_item(Item=fixture)

    def test_handler(self,
                     event=Event,
                     bucket=TestBucket,
                     table=TestTable):
        with mock.patch.dict(os.environ, self.env):
            from #{IndexModulePath} import handler
            handler(event)

    def tearDown(self):
        self.teardown_dynamodb()
        self.teardown_s3()

if __name__=="__main__":
    unittest.main()

