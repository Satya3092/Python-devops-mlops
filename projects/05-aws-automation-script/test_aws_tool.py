"""Offline tests using botocore's Stubber (no AWS account needed).
Run: pip install boto3 pytest && pytest -q
"""
import boto3
from botocore.stub import Stubber

import aws_tool


def test_tags_to_dict():
    assert aws_tool.tags_to_dict([{"Key": "Env", "Value": "dev"}]) == {"Env": "dev"}
    assert aws_tool.tags_to_dict(None) == {}


def test_all_instances_flattens_reservations():
    ec2 = boto3.client("ec2", region_name="ap-south-1", aws_access_key_id="test", aws_secret_access_key="test")
    response = {"Reservations": [
        {"Instances": [{"InstanceId": "i-1"}, {"InstanceId": "i-2"}]},
        {"Instances": [{"InstanceId": "i-3"}]},
    ]}
    with Stubber(ec2) as stub:
        stub.add_response("describe_instances", response, {"Filters": []})
        ids = [i["InstanceId"] for i in aws_tool.all_instances(ec2)]
    assert ids == ["i-1", "i-2", "i-3"]


def test_parser_defaults_to_dry_run():
    args = aws_tool.build_parser().parse_args(["ec2-stop", "--env", "dev"])
    assert args.apply is False
