# Vertice Cloud Cost Optimization CloudFormation templates

This repository provides CloudFormation templates helping to configure
[Vertice Cloud Cost Optimization](https://www.vertice.one/product/cloud-cost-optimization)
infrastructure in your account, including:

* an IAM role allowing Vertice platform to access your resources,
* an S3 bucket to store Cost and Usage Reports (CUR), and
* a Cost and Usage Report definition.

We also offer Terraform configuration of the same at
[VerticeOne/terraform-aws-vertice-integration](https://github.com/VerticeOne/terraform-aws-vertice-integration).

## Using the template

The [Vertice governance CloudFormation template](templates/governance.yaml) is published
to the following S3 address:

```text
https://vertice-cco-cloudformation-templates.s3.eu-west-1.amazonaws.com/vertice-governance.yaml
```

To deploy it, [create a new CloudFormation Stack](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-cli-creating-stack.html),
providing the URL above as the `--template-url` parameter (or `Amazon S3 URL`
in the AWS console).

### :warning: Region selection

As documented [in this upstream issue](https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/1825),
the AWS CUR functionality is limited to the `us-east-1` region. Therefore,
we recommend deploying this template to that region to ensure smooth operation.

### Parameters

Only the **AccountType** parameter is strictly required by the template,
supporting the following values:

* `billing` (CUR with S3 bucket should be configured in the account);
* `member` (IAM role should be allowed to monitor your AWS services); or
* `combined` (both `billing` and `member` resources should be set up).

The creation of specific resources is further controlled by the
**BillingReportCreate**, **BillingBucketCreate** and **VerticeIAMRoleCreate**
parameters. The **BillingBucketName** will usually also need to be provided.
Please see the `Parameters` section of the template for further details.
