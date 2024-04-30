### short

- run migrate_infra.py on index handlers
- refactor test.py env variables

### medium

- add sns fixture support
- ask which fixtures u want and have chatgpt remove unwanted ones

### done

- templates must not define handler function default args if they reference os.environ
- event templates (and anything else which refs table/bucket/website names) should define related boto3 clients/resources
- really need a website event template
- table event template references bucket event source
- XXX_TABLE is mis- defined in templates
- events timer template
- admin script to initialise template
- sns topic template
- sqs queue template
- eventbridge table event template
- eventbridge bucket event template
- apigateway post
- test script
- iterate through directory
- take path from each template replacing template prefix  with demo
- create series of variables expected to be required by the template
- extract variables from template
- asset all variables have corresponding values
- populate template with variable 
- save template to path 
- extract tests and run suite 
- api gateway get 
- replace setup/teardown_ddb
