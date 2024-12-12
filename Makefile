init:
	pip install -r requirements.txt

test:
	pytest tests/

deploy-case-1:
	aws cloudformation deploy \
		--template-file templates/governance.yaml \
		--stack-name mencner-gov-test-case-1 \
		--parameter-overrides file://tests/parameters/case_1.json \
		--capabilities CAPABILITY_NAMED_IAM

deploy-case-2:
	aws cloudformation deploy \
		--template-file templates/governance.yaml \
		--stack-name mencner-gov-test-case-2 \
		--parameter-overrides file://tests/parameters/case_2.json \
		--capabilities CAPABILITY_NAMED_IAM

destroy-case-1:
	aws cloudformation delete-stack --stack-name mencner-gov-test-case-1

destroy-case-2:
	aws cloudformation delete-stack --stack-name mencner-gov-test-case-2