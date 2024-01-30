from skeletor.test import SkeletorTestBase
from skeletor.test.dynamodb import SkeletorDynamodbTestMixin, TestTable
from skeletor.test.s3 import SkeletorS3TestMixin, TestBucket

from moto import mock_dynamodb, mock_s3

import json, os, unittest, yaml

import unittest.mock as mock

TableFixtures=yaml.safe_load("""
[]
""")

Username, Payload = "foo@bar.com", {"hello": "world"}

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
                     username=Username,
                     payload=Payload,
                     bucket=TestBucket,
                     table=TestTable):
        reqauth={"claims": {"email": username}}
        event={"requestContext": {"authorizer": reqauth},
               "body": json.dumps(payload)}
        with mock.patch.dict(os.environ, self.env):
            from #{IndexModulePath} import handler
            resp=handler(event)
            self.assertTrue("statusCode" in resp)
            self.assertEqual(resp["statusCode"], 200)
            self.assertTrue("body" in resp)
            self.assertEqual(resp["body"], "ok")

    def tearDown(self):
        self.teardown_dynamodb()
        self.teardown_s3()

if __name__=="__main__":
    unittest.main()

