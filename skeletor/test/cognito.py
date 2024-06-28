import boto3 

PoolName = "my-test-pool"

class CognitoMixin:

    def setup_cognito(self,
                      username,
                      userattrs, 
                      pool_name = PoolName):
        self.cognito = boto3.client("cognito-idp")
        schema = [{'Name': 'email',
                   'AttributeDataType': 'String',
                   'Mutable': True,
                   'Required': True}]
        schema += [{'Name': key,
                    'AttributeDataType': 'String',
                    'Mutable': True} for key in userattrs]                 
        response = self.cognito.create_user_pool(PoolName = pool_name,
                                                 Schema = schema)
        self.user_pool_id = response['UserPool']['Id']
        self.cognito.admin_create_user(
            UserPoolId = self.user_pool_id,
            Username = username,
            UserAttributes=[{'Name': 'email',
                             'Value': username}],
            MessageAction='SUPPRESS'
        )
        self.cognito.admin_update_user_attributes(
            UserPoolId = self.user_pool_id,
            Username = username,
            UserAttributes = [{'Name': key if key.startswith("custom:") else "custom:%s" % key,
                               'Value': value}
                              for key, value in userattrs.items()]
        )
        
    def teardown_cognito(self, username = Username):
        self.cognito.admin_delete_user(
            UserPoolId = self.user_pool_id,
            Username = username
        )
        self.cognito.delete_user_pool(
            UserPoolId = self.user_pool_id
        )

if __name__ == "__main__":
    pass
