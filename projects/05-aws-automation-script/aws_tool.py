"""
Project 5 - AWS Automation Script (safe by default).

Credentials come ONLY from the standard boto3 chain (SSO profile, IAM role, env vars).
Usage: python aws_tool.py {whoami,s3-list,s3-upload,ec2-list,tag-audit,ec2-stop} [options]
"""
import argparse
import csv
import logging
import os
import sys
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

LOG = logging.getLogger("aws_tool")
RETRY_CONFIG = Config(retries={"max_attempts": 5, "mode": "standard"})


def session_from_args(args):
    return boto3.Session(profile_name=args.profile, region_name=args.region or os.getenv("AWS_REGION"))


def tags_to_dict(tags):
    return {t["Key"]: t["Value"] for t in tags or []}


def all_instances(ec2, filters=None):
    instances = []
    for page in ec2.get_paginator("describe_instances").paginate(Filters=filters or []):
        for reservation in page["Reservations"]:
            instances.extend(reservation["Instances"])
    return instances


# ----------------------------------------------------------------------------- commands
def cmd_whoami(session, args):
    identity = session.client("sts", config=RETRY_CONFIG).get_caller_identity()
    print(f"Account : {identity['Account']}")
    print(f"Caller  : {identity['Arn']}")
    print(f"Region  : {session.region_name}")
    print(f"Source  : {session.get_credentials().method}")
    return 0


def cmd_s3_list(session, args):
    s3 = session.client("s3", config=RETRY_CONFIG)
    buckets = s3.list_buckets()["Buckets"]
    print(f"{'BUCKET':<40}{'REGION':<15}{'OBJECTS':>9}{'SIZE MB':>10}")
    for bucket in buckets:
        name = bucket["Name"]
        try:
            region = s3.get_bucket_location(Bucket=name)["LocationConstraint"] or "us-east-1"
            regional = session.client("s3", region_name=region, config=RETRY_CONFIG)
            count = size = 0
            for page in regional.get_paginator("list_objects_v2").paginate(Bucket=name):
                for obj in page.get("Contents", []):
                    count += 1
                    size += obj["Size"]
            print(f"{name:<40}{region:<15}{count:>9}{size / 1024 ** 2:>10.2f}")
        except ClientError as error:
            print(f"{name:<40}{'?':<15}  {error.response['Error']['Code']}")
    return 0


def cmd_s3_upload(session, args):
    path = Path(args.file)
    if not path.is_file():
        print(f"File not found: {path}")
        return 2
    key = f"{args.prefix}{path.name}"
    s3 = session.client("s3", config=RETRY_CONFIG)
    s3.upload_file(str(path), args.bucket, key, ExtraArgs={"ServerSideEncryption": "AES256"})
    print(f"Uploaded {path} -> s3://{args.bucket}/{key} (SSE-S3 encrypted)")
    return 0


def cmd_ec2_list(session, args):
    filters = [{"Name": "instance-state-name", "Values": [args.state]}] if args.state else []
    instances = all_instances(session.client("ec2", config=RETRY_CONFIG), filters)
    print(f"{'INSTANCE':<21}{'TYPE':<12}{'STATE':<10}{'NAME':<16}{'ENV':<9}OWNER")
    for inst in instances:
        tags = tags_to_dict(inst.get("Tags"))
        print(f"{inst['InstanceId']:<21}{inst['InstanceType']:<12}{inst['State']['Name']:<10}"
              f"{tags.get('Name', '-'):<16}{tags.get('Env', '-'):<9}{tags.get('Owner', '-')}")
    print(f"{len(instances)} instance(s) in {session.region_name}")
    return 0


def cmd_tag_audit(session, args):
    instances = all_instances(session.client("ec2", config=RETRY_CONFIG))
    rows = []
    for inst in instances:
        tags = tags_to_dict(inst.get("Tags"))
        missing = [t for t in args.required if t not in tags]
        if missing:
            rows.append({"instance_id": inst["InstanceId"], "name": tags.get("Name", "-"),
                         "state": inst["State"]["Name"], "missing_tags": " ".join(missing)})
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["instance_id", "name", "state", "missing_tags"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} of {len(instances)} instance(s) missing tags {args.required} -> {args.output}")
    return 1 if rows else 0


def cmd_ec2_stop(session, args):
    ec2 = session.client("ec2", config=RETRY_CONFIG)
    targets = all_instances(ec2, [{"Name": "tag:Env", "Values": [args.env]},
                                  {"Name": "instance-state-name", "Values": ["running"]}])
    if args.env == "prod":
        print("Refusing to stop prod instances with this tool.")
        return 2
    for inst in targets:
        name = tags_to_dict(inst.get("Tags")).get("Name", "-")
        label = f"{inst['InstanceId']} ({name}, {inst['InstanceType']})"
        try:
            ec2.stop_instances(InstanceIds=[inst["InstanceId"]], DryRun=not args.apply)
            print(f"Stopping {label}")
            LOG.info("stopped %s", inst["InstanceId"])
        except ClientError as error:
            code = error.response["Error"]["Code"]
            if code == "DryRunOperation":
                print(f"[DRY RUN] would stop {label} - permission check: allowed")
            else:
                print(f"[ERROR] {label}: {code}")
    print(f"{len(targets)} instance(s) matched." + ("" if args.apply else " Re-run with --apply to stop them."))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Safe AWS automation helper")
    parser.add_argument("--profile", default=os.getenv("AWS_PROFILE"), help="AWS profile (SSO recommended)")
    parser.add_argument("--region", help="AWS region (default: AWS_REGION / profile)")
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("whoami").set_defaults(func=cmd_whoami)
    sub.add_parser("s3-list").set_defaults(func=cmd_s3_list)
    p = sub.add_parser("s3-upload")
    p.add_argument("file")
    p.add_argument("--bucket", required=True)
    p.add_argument("--prefix", default="")
    p.set_defaults(func=cmd_s3_upload)
    p = sub.add_parser("ec2-list")
    p.add_argument("--state", choices=["pending", "running", "stopped", "stopping", "terminated"])
    p.set_defaults(func=cmd_ec2_list)
    p = sub.add_parser("tag-audit")
    p.add_argument("--required", nargs="+", default=["Owner", "Env"])
    p.add_argument("--output", default="tag-audit.csv")
    p.set_defaults(func=cmd_tag_audit)
    p = sub.add_parser("ec2-stop")
    p.add_argument("--env", required=True)
    p.add_argument("--apply", action="store_true", help="really stop (default is a dry run)")
    p.set_defaults(func=cmd_ec2_stop)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING,
                        format="%(asctime)s %(levelname)s %(message)s")
    try:
        return args.func(session_from_args(args), args)
    except NoCredentialsError:
        print("No AWS credentials found. Use 'aws configure sso', an IAM role, or AWS_PROFILE.")
    except ClientError as error:
        err = error.response["Error"]
        print(f"AWS error {err['Code']}: {err['Message']}")
    except BotoCoreError as error:
        print(f"AWS SDK error: {error}")
    return 3


if __name__ == "__main__":
    sys.exit(main())
