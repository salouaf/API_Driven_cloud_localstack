import boto3
import json

def lambda_handler(event, context):
    ec2 = boto3.client(
        'ec2',
        endpoint_url='http://172.17.0.1:4566',
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )
    
    body = json.loads(event.get('body', '{}'))
    instance_id = body.get('instance_id')
    action = body.get('action')

    if action == "start":
        ec2.start_instances(InstanceIds=[instance_id])
        message = f"Instance {instance_id} démarrée"
    elif action == "stop":
        ec2.stop_instances(InstanceIds=[instance_id])
        message = f"Instance {instance_id} arrêtée"
    else:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Action inconnue. Utilise 'start' ou 'stop'"})
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": message})
    }
