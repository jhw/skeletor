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
- EventSource: aws:sns
  EventVersion: '1.0'
  EventSubscriptionArn: arn:aws:sns:eu-west-1:XXXXXXXXXXXX:my-topic:XXXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX
  Sns:
    Type: Notification
    MessageId: XXXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX
    TopicArn: arn:aws:sns:eu-west-1:XXXXXXXXXXXX:my-topic
    Subject: Whatevs
    Message: '{"hello": "world"}'
    Timestamp: '2024-01-01T00:00:00.000Z'
    SignatureVersion: '1'
    Signature: ABCDEFGHIJKLMNOPQRSTUVWZYZ==
    SigningCertUrl: https://sns.eu-west-1.amazonaws.com/my-topic.pem
    UnsubscribeUrl: https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-west-1:XXXXXXXXXXXX:my-topic:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    MessageAttributes: {}
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

