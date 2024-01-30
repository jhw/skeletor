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
id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx
detail-type: Object Created
source: aws.s3
account: '0123456789'
time: '2024-01-01T00:00:00Z'
region: eu-west-1
resources:
- arn:aws:s3:::my-bucket
detail:
  version: '0'
  bucket:
    name: my-bucket
  object:
    key: hello/world.zip
    size: 1234
    etag: ABCDEFGHIJKLMNOPQRSTUVWXYZ
    sequencer: 0A1B2C3D4E5F6G7H
  request-id: 0N1O2P3Q4R5S6T7U8V
  requester: '0123456789'
  source-ip-address: 00.00.00.00
  reason: PutObject
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

