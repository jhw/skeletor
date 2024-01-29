from skeletor.test import SkeletorTestBase

from skeletor.test.dynamodb import SkeletorDynamodbTestMixin, TestTable

from skeletor.test.s3 import SkeletorS3TestMixin, TestBucket

from moto import mock_dynamodb, mock_s3

import unittest.mock as mock

import json, os, unittest, yaml

Fixtures=yaml.safe_load("""
[]
""")

@mock_dynamodb
@mock_s3
class #{TestClassName}(Pareto2TestBase,                    
                       Pareto2DDBTestMixin,
                       Pareto2S3TestMixin):
    
    def setUp(self,
              fixtures=Fixtures,
              bucket=TestBucket,
              table=TestTable):
        self.env={}
        self.setup_ddb()
        self.env["#{TableKey}"]=table["name"]
        self.setup_s3()
        self.env["#{BucketKey}"]=bucket["name"]
        with self.tables[0].batch_writer() as batch:
            for fixture in fixtures:
                batch.put_item(Item=fixture)

    def test_handler(self,
                     bucket=TestBucket
                     table=TestTable):
        params={"foo": "bar"}
        event={"queryStringParameters": params}
        with mock.patch.dict(os.environ, self.env):
            from ImportPath import handler
            resp=handler(event)
            self.assertTrue("statusCode" in resp)
            self.assertEqual(resp["statusCode"], 200)
            self.assertTrue("body" in resp)
            struct=json.loads(resp["body"])            
            self.assertTrue(struct!=[])

    def tearDown(self):
        self.teardown_ddb()
        self.teardown_s3()

if __name__=="__main__":
    unittest.main()

