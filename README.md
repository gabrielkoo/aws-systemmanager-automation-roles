# aws-systemmanager-automation-roles

This repo contains a python script that generates a CloudFormation template defines roles that could be used by AWS System Manager's automation documents. Custom roles are sometimes required when the steps of an automation document contains the type `aws:executeAwsApi`, which could not be run by the default SSM service role.

These special roles correspond to some SSM Automation Documents, which could in fact be used in AWS Config automatic remedations.

```bash
# install dependencies
pip install -r requirements.txt

# configure your credentials here.
# permission for the user / role needed:
# - ssm:ListDocuments
# - ssm:GetDocument
aws configure

# save the CloudFormation template into file
python generate_roles.py > automation-roles.yml
```
