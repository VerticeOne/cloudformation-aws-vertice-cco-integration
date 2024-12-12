import boto3
import pytest


def test_role():
    iam = boto3.client("iam")
    response = iam.get_role(RoleName="test-gov-template-case-2")
    role = response["Role"]
    del role["CreateDate"]
    del role["RoleId"]
    role["AssumeRolePolicyDocument"]["Statement"][0]["Principal"]["AWS"].sort()
    assert role == {
        "Path": "/vertice/",
        "RoleName": "test-gov-template-case-2",
        "Arn": "arn:aws:iam::169937232134:role/vertice/test-gov-template-case-2",
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
                            "sts:ExternalId": "868af261-713d-461d-9ba1-a76cdd9888df"
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
    ("policy_name"),
    [
        ("VerticeEc2RiAccess"),
        ("VerticeElastiCacheRiAccess"),
        ("VerticeEsRiAccess"),
        ("VerticeRdsRiAccess"),
        ("VerticeRedshiftRiAccess"),
        ("VerticeSavingPlansAccess"),
    ],
)
def test_role_policy_not_exists(policy_name):
    iam = boto3.client("iam")

    # List the policies attached to the role
    attached_policies = iam.list_attached_role_policies(
        RoleName="test-gov-template-case-2"
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
    assert billing_policy is None


def get_policy_with_sid(statements, sid):
    for statement in statements:
        if statement.get("Sid") == sid:
            return statement
    return None
