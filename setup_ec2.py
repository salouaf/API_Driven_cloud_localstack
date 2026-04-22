
import boto3

ec2 = boto3.client(
    'ec2',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

response = ec2.run_instances(
    ImageId='ami-07b643b5e45e',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1
)

instance_id = response['Instances'][0]['InstanceId']
print(f"Instance EC2 creee ! InstanceId: {instance_id}")
