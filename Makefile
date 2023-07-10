image      := generator
region     := $(shell aws configure get region)
account_id := $(shell aws sts get-caller-identity --query Account --output text)
uri        := ${account_id}.dkr.ecr.${region}.amazonaws.com
target     := .

format:
	@isort ${target} \
	&& black ${target} \
	&& ruff ${target}

deploy: format
	@docker build --platform=linux/amd64 -t ${image} . \
	&& aws ecr get-login-password --region ${region} \
	| docker login \
	--username AWS \
	--password-stdin ${uri} \
	&& aws ecr create-repository \
	--repository-name ${image} \
	--image-scanning-configuration scanOnPush=true \
	--image-tag-mutability MUTABLE \
	&& docker tag ${image}:latest ${uri}/${image}:latest \
	&& docker push ${uri}/${image}:latest \
	&& aws lambda create-function \
	--function-name ${image} \
	--package-type Image \
	--code ImageUri=${uri}/${image}:latest \
	--role arn:aws:iam::${account_id}:role/lambda-ex

role:
	@aws iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
