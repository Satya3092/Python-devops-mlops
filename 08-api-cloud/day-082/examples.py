"""
Day 082 — Boto3 Introduction and AWS SDK
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Who am I? Sessions, regions and safe error handling
# ======================================================================
import os

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound

# Nothing secret here: the region and profile come from the environment / ~/.aws/config
region = os.getenv("AWS_REGION", "ap-south-1")
profile = os.getenv("AWS_PROFILE")                 # e.g. "learning" (optional)

try:
    session = boto3.Session(profile_name=profile, region_name=region)
    sts = session.client("sts")
    identity = sts.get_caller_identity()           # free, read-only, works with any valid credentials
    print("Account :", identity["Account"])
    print("Caller  :", identity["Arn"].split(":")[-1])
    print("Region  :", session.region_name)
    creds = session.get_credentials()
    print("Credential source:", creds.method)       # env, shared-credentials-file, sso, iam-role...
except ProfileNotFound as error:
    print("Profile problem:", error)
except NoCredentialsError:
    print("No AWS credentials found. Run 'aws configure sso' or attach an IAM role.")
except ClientError as error:
    print("AWS error:", error.response["Error"]["Code"], "-", error.response["Error"]["Message"])

# ======================================================================
# Example 2 — Read-only S3 and EC2 inventory with paginators and DryRun
# ======================================================================
import os

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

session = boto3.Session(region_name=os.getenv("AWS_REGION", "ap-south-1"))
s3 = session.client("s3")
ec2 = session.client("ec2")

try:
    # --- S3: list buckets and their regions (read-only) ---
    buckets = s3.list_buckets()["Buckets"]
    print(f"S3 buckets: {len(buckets)}")
    for bucket in buckets[:5]:
        location = s3.get_bucket_location(Bucket=bucket["Name"])["LocationConstraint"] or "us-east-1"
        print(f"  {bucket['Name']:<32} {location:<12} created {bucket['CreationDate']:%Y-%m-%d}")

    # --- EC2: every instance in the region, page by page ---
    paginator = ec2.get_paginator("describe_instances")
    instances = []
    for page in paginator.paginate():
        for reservation in page["Reservations"]:
            instances.extend(reservation["Instances"])
    print(f"EC2 instances in {session.region_name}: {len(instances)}")
    for inst in instances:
        tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
        print(f"  {inst['InstanceId']}  {inst['InstanceType']:<10} {inst['State']['Name']:<9} "
              f"Name={tags.get('Name', '-'):<12} Owner={tags.get('Owner', 'MISSING')}")

    # --- Permission check without side effects ---
    running = [i["InstanceId"] for i in instances if i["State"]["Name"] == "running"]
    if running:
        try:
            ec2.stop_instances(InstanceIds=running[:1], DryRun=True)
        except ClientError as error:
            code = error.response["Error"]["Code"]
            print("DryRun stop:", "allowed (nothing was stopped)" if code == "DryRunOperation" else code)
except NoCredentialsError:
    print("No AWS credentials found - see the setup notes above.")
except ClientError as error:
    print("AWS error:", error.response["Error"]["Code"])
