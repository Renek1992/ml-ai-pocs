bucket_name=${BUCKET_NAME}

# Include .env file
include .env
export $(shell sed 's/=.*//' .env)

core-infra:
	@echo "[$$(date +'%Y-%m-%d %H:%M:%S')] || Deploying changes to stack..."
	@aws cloudformation deploy \
	--stack-name rekogn-celeb-comparsion-core \
	--template-file ./deploy/core_infra.yml \
	--capabilities CAPABILITY_NAMED_IAM \
	--parameter-overrides BucketName=$(bucket_name) \
	--region us-east-1
	@echo "[$$(date +'%Y-%m-%d %H:%M:%S')] || Changes to stack deployed."