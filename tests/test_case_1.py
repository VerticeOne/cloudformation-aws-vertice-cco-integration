import boto3
import pytest


def test_role():
    iam = boto3.client("iam")
    response = iam.get_role(RoleName="test-gov-template-case-1")
    role = response["Role"]
    del role["CreateDate"]
    del role["RoleId"]
    role["AssumeRolePolicyDocument"]["Statement"][0]["Principal"]["AWS"].sort()
    assert role == {
        "Path": "/vertice/",
        "RoleName": "test-gov-template-case-1",
        "Arn": "arn:aws:iam::169937232134:role/vertice/test-gov-template-case-1",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            "arn:aws:iam::642184526628:root",
                            "arn:aws:iam::762729743961:root",
                        ]
                    },
                    "Action": "sts:AssumeRole",
                    "Condition": {
                        "StringLike": {
                            "sts:ExternalId": "24b28687-dfd3-471a-8bb3-2f2b4530380b"
                        }
                    },
                }
            ],
        },
        "Description": "Role assumed by Vertice to monitor your spending",
        "MaxSessionDuration": 43200,
        "RoleLastUsed": {},
    }


@pytest.mark.parametrize(
    ("policy_name", "effect", "resource", "action"),
    [
        (
            "VerticeBillingAccess",
            "Allow",
            "*",
            [
                "bcm-data-exports:GetExport",
                "bcm-data-exports:GetExecution",
                "bcm-data-exports:ListExports",
                "bcm-data-exports:ListExecutions",
                "budgets:Describe*",
                "budgets:View*",
                "ce:Describe*",
                "ce:Get*",
                "ce:List*",
                "cur:Describe*",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeInstanceTypeOfferings",
                "ec2:DescribeInstanceTypes",
                "ec2:DescribeInstances",
                "ec2:DescribeReservedInstances",
                "ec2:DescribeReservedInstancesOfferings",
                "elasticache:DescribeReservedCacheNodes",
                "elasticache:DescribeReservedCacheNodesOfferings",
                "es:DescribeReservedInstanceOfferings",
                "es:DescribeReservedInstances",
                "organizations:Describe*",
                "organizations:List*",
                "rds:DescribeDBInstances",
                "rds:DescribeReservedDBInstances",
                "rds:DescribeReservedDBInstancesOfferings",
                "redshift:DescribeReservedNodeOfferings",
                "redshift:DescribeReservedNodes",
                "savingsplans:Describe*",
                "savingsplans:List*",
            ],
        ),
        (
            "VerticeBillingBucketAccess",
            "Allow",
            [
                "arn:aws:s3:::test-gov-template-case-1",
                "arn:aws:s3:::test-gov-template-case-1/*",
            ],
            [
                "s3:GetBucketLocation",
                "s3:ListBucket",
                "s3:GetObject",
            ],
        ),
        (
            "VerticeEc2RiAccess",
            "Allow",
            "*",
            [
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeInstanceTypeOfferings",
                "ec2:DescribeInstanceTypes",
                "ec2:DescribeInstances",
                "ec2:DescribeReservedInstances",
                "ec2:DescribeReservedInstancesOfferings",
                "ec2:PurchaseReservedInstancesOffering",
                "ec2:ModifyReservedInstances",
                "ec2:DeleteQueuedReservedInstances",
            ],
        ),
        (
            "VerticeElastiCacheRiAccess",
            "Allow",
            "*",
            [
                "elasticache:DescribeReservedCacheNodes",
                "elasticache:DescribeReservedCacheNodesOfferings",
                "elasticache:PurchaseReservedCacheNodesOffering",
            ],
        ),
        (
            "VerticeEsRiAccess",
            "Allow",
            "*",
            [
                "es:DescribeReservedInstanceOfferings",
                "es:DescribeReservedInstances",
                "es:PurchaseReservedInstanceOffering",
            ],
        ),
        (
            "VerticeRdsRiAccess",
            "Allow",
            "*",
            [
                "rds:DescribeDBInstances",
                "rds:DescribeReservedDBInstances",
                "rds:DescribeReservedDBInstancesOfferings",
                "rds:PurchaseReservedDBInstancesOffering",
            ],
        ),
        (
            "VerticeRedshiftRiAccess",
            "Allow",
            "*",
            [
                "redshift:DescribeReservedNodeOfferings",
                "redshift:DescribeReservedNodes",
                "redshift:PurchaseReservedNodeOffering",
            ],
        ),
        (
            "VerticeSavingPlansAccess",
            "Allow",
            "*",
            [
                "savingsplans:Describe*",
                "savingsplans:List*",
                "savingsplans:CreateSavingsPlan",
                "savingsplans:DeleteQueuedSavingsPlan",
            ],
        ),
    ],
)
def test_role_permissions(policy_name, effect, resource, action):
    iam = boto3.client("iam")

    # List the policies attached to the role
    attached_policies = iam.list_attached_role_policies(
        RoleName="test-gov-template-case-1"
    )
    statements = []
    for policy in attached_policies["AttachedPolicies"]:
        policy_arn = policy["PolicyArn"]

        # Get the policy document
        policy_version = iam.get_policy(PolicyArn=policy_arn)["Policy"][
            "DefaultVersionId"
        ]
        policy_document = iam.get_policy_version(
            PolicyArn=policy_arn, VersionId=policy_version
        )["PolicyVersion"]["Document"]

        statements.extend(policy_document["Statement"])

    billing_policy = get_policy_with_sid(statements, policy_name)
    assert billing_policy is not None
    assert billing_policy["Resource"] == resource
    assert billing_policy["Effect"] == effect
    assert billing_policy["Action"] == action


def get_policy_with_sid(statements, sid):
    for statement in statements:
        if statement.get("Sid") == sid:
            return statement
    return None
