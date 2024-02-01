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
Records:
- messageId: 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXX'
  receiptHandle: ABCDEFGHIJKLM
  body: '{"hello": "world"}'
  attributes:
    ApproximateReceiveCount: '1'
    SentTimestamp: '1500000000000'
    SenderId: NOPQRSTUVWZYZ
    ApproximateFirstReceiveTimestamp: '1500000000000'
  messageAttributes: {}
  md5OfBody: a1b2c3d4e5f6g7h8
  eventSource: aws:sqs
  eventSourceARN: arn:aws:sqs:eu-west-1:XXXXXXXXXXXX:my-queue
  awsRegion: eu-west-1
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

