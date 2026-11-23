"""
Day 082 — Boto3 Introduction and AWS SDK: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import os

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

REGION = os.getenv("AWS_REGION", "ap-south-1")

# ===== Task 1 =====
def whoami():
    try:
        identity = boto3.client("sts", region_name=REGION).get_caller_identity()
        return f"Account {identity['Account']} in {REGION}"
    except NoCredentialsError:
        return "No AWS credentials found. Run 'aws configure sso' or attach an IAM role."
    except ClientError as error:
        return f"Credentials rejected: {error.response['Error']['Code']}"


print(whoami())

# ===== Task 2 =====
s3 = boto3.client("s3", region_name=REGION)
try:
    for bucket in s3.list_buckets()["Buckets"]:
        count = size = 0
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket["Name"]):
            for obj in page.get("Contents", []):
                count += 1
                size += obj["Size"]
        print(f"{bucket['Name']}: {count} objects, {size / 1024 ** 2:.2f} MB")
except (NoCredentialsError, ClientError) as error:
    print("Cannot list buckets:", error)

# ===== Task 3 =====
APPLY = False
ec2 = boto3.client("ec2", region_name=REGION)
try:
    instances = [i for page in ec2.get_paginator("describe_instances").paginate()
                 for r in page["Reservations"] for i in r["Instances"]]
    print("Instances missing the Owner tag:")
    for inst in instances:
        tags = {t["Key"]: t["Value"] for t in inst.get("Tags", [])}
        if "Owner" not in tags:
            print(f"  {inst['InstanceId']} ({inst['State']['Name']}) Name={tags.get('Name', '-')}")
    dev_running = [i["InstanceId"] for i in instances
                   if i["State"]["Name"] == "running"
                   and {t["Key"]: t["Value"] for t in i.get("Tags", [])}.get("Env") == "dev"]
    print("Dev instances to stop:", dev_running)
    for instance_id in dev_running:
        try:
            ec2.stop_instances(InstanceIds=[instance_id], DryRun=not APPLY)
            print("Stopped", instance_id)
        except ClientError as error:
            if error.response["Error"]["Code"] == "DryRunOperation":
                print(f"DryRun for {instance_id}: allowed - re-run with --apply to really stop it")
            else:
                print(f"{instance_id}: {error.response['Error']['Code']}")
except (NoCredentialsError, ClientError) as error:
    print("Cannot describe instances:", error)
