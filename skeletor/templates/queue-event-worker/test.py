from skeletor.test import SkeletorTestBase
from skeletor.test.dynamodb import SkeletorDynamodbTestMixin, TestTable
from skeletor.test.s3 import SkeletorS3TestMixin, TestBucket

from moto import mock_dynamodb, mock_s3

import json, os, unittest, yaml

import unittest.mock as mock

TableFixtures=yaml.safe_load("""
[]
""")

"""
Remember pareto2 task-queue inline code passes `record["body"]` as `detail` field in EventBridge message; specifiying `type` as `queue` will bind `source` field to APP_QUEUE url within rule definition
"""

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
  hello: world
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
        self.env["APP_TABLE"]=table["name"]
        self.setup_s3()
        self.env["APP_BUCKET"]=bucket["name"]
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

