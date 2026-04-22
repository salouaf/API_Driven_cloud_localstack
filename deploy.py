
import boto3

# Deploy Lambda
lambda_client = boto3.client(
    'lambda',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

with open('function.zip', 'rb') as f:
    zip_content = f.read()

lambda_client.create_function(
    FunctionName='pilote-ec2',
    Runtime='python3.11',
    Role='arn:aws:iam::000000000000:role/lambda-role',
    Handler='lambda_function.lambda_handler',
    Code={'ZipFile': zip_content}
)
print("Lambda deployee !")

# Deploy API Gateway
apigw = boto3.client(
    'apigateway',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

api = apigw.create_rest_api(name='EC2-Control-API')
api_id = api['id']

resources = apigw.get_resources(restApiId=api_id)
root_id = resources['items'][0]['id']

resource = apigw.create_resource(
    restApiId=api_id,
    parentId=root_id,
    pathPart='ec2'
)
resource_id = resource['id']

apigw.put_method(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='POST',
    authorizationType='NONE'
)

apigw.put_integration(
    restApiId=api_id,
    resourceId=resource_id,
    httpMethod='POST',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri='arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:pilote-ec2/invocations'
)

apigw.create_deployment(restApiId=api_id, stageName='prod')
print(f"API Gateway deployee ! ID: {api_id}")
print(f"Endpoint: http://localhost:4566/_aws/execute-api/{api_id}/prod/ec2")
