
.PHONY: all install setup deploy test clean

all: install setup deploy

install:
	pip install awscli awscli-local boto3 --break-system-packages
	aws configure set aws_access_key_id test
	aws configure set aws_secret_access_key test
	aws configure set region us-east-1
	aws configure set output json

setup:
	python3 setup_ec2.py

deploy:
	zip function.zip lambda_function.py
	python3 deploy.py

test:
	curl -X POST "http://localhost:4566/_aws/execute-api/otwmmt3szx/prod/ec2" -H "Content-Type: application/json" -d '{"instance_id": "i-f5a5df153f11d2641", "action": "stop"}'

clean:
	rm -f function.zip
