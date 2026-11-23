# Day 082 — Boto3 Introduction and AWS SDK

[⬅ Day 081](../../08-api-cloud/day-081/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 083 ➡](../../09-data-analysis/day-083/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 8 — API, Cloud and DevOps Integration | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Install boto3 and understand clients, resources, sessions and the credential chain
- Authenticate safely (IAM roles, profiles, environment) — never hard-coded keys
- Read S3 and EC2 information with paginators and handle `ClientError`; use `DryRun`

## 2. Topic Explanation

**boto3** is the official AWS SDK for Python — the same engine behind many AWS automation tools.

```bash
pip install boto3
aws configure            # or: aws configure sso   (creates a profile in ~/.aws)
```

**Core concepts**
- **Client** — low-level, 1:1 with AWS API calls: `boto3.client("s3").list_buckets()`. Returns dicts.
- **Resource** — higher-level objects for some services (`boto3.resource("s3").Bucket("x")`). AWS has frozen new resource features, so prefer clients for new code.
- **Session** — holds credentials + region: `boto3.Session(profile_name="dev", region_name="ap-south-1")`.
- **Paginators** — many APIs return results in pages; `client.get_paginator("describe_instances")` loops for you.
- **Errors** — `botocore.exceptions.ClientError` (AccessDenied, NoSuchBucket...), `NoCredentialsError`, `NoRegionError`.

**How boto3 finds credentials (the credential chain, in order):**
1. Parameters passed in code (**don't**).
2. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_PROFILE`).
3. Shared files `~/.aws/credentials` and `~/.aws/config` (profiles, **SSO**).
4. Container credentials (ECS task roles), then **EC2 instance profile** (IAM role).
5. On EKS: IRSA / Pod Identity. In GitHub Actions: OIDC role assumption.

✅ Best practice: **IAM roles** on AWS compute, **SSO profiles** on laptops, **OIDC** in CI. Short-lived credentials, least privilege.
❌ Never put access keys in code, Git, Docker images or notebooks.

**Using the Free Tier responsibly**
- Prefer **read-only** calls while learning (`list_*`, `describe_*`, `get_caller_identity`) — they are free.
- Use `DryRun=True` on EC2 actions to test permissions without doing anything.
- If you create resources: tag them (`Owner`, `Purpose=learning`), stick to free-tier types (e.g. `t2.micro`/`t3.micro` where eligible), and **delete them the same day**.
- Set an **AWS Budget** alert (e.g. $5) and enable **Cost Explorer**. Check the Billing console regularly.
- Watch for hidden costs: NAT gateways, Elastic IPs not attached, EBS snapshots, data transfer, CloudWatch Logs retention.

## 3. Syntax

```python
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

session = boto3.Session(profile_name="dev", region_name="ap-south-1")   # or rely on env/role
s3 = session.client("s3")
ec2 = session.client("ec2")

paginator = ec2.get_paginator("describe_instances")
for page in paginator.paginate(Filters=[{"Name": "instance-state-name", "Values": ["running"]}]):
    ...
try:
    ec2.stop_instances(InstanceIds=["i-123"], DryRun=True)
except ClientError as e:
    e.response["Error"]["Code"]      # "DryRunOperation" means you WOULD be allowed
```

| Part | Meaning |
|---|---|
| `boto3.Session` | Credentials + region container; uses the credential chain if nothing is passed. |
| `session.client("svc")` | Low-level API client. |
| `get_paginator` | Iterate through all pages of results. |
| `ClientError` | AWS returned an error; details in `e.response["Error"]`. |
| `DryRun=True` | Checks permissions for EC2 actions without performing them. |

## 4. Example 1 — Basic Example: Who am I? Sessions, regions and safe error handling

```python
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
```

## 5. Example 2 — Practical Example: Read-only S3 and EC2 inventory with paginators and DryRun

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- No keys in code: `boto3.Session()` uses the credential chain (env vars, `~/.aws`, SSO, IAM role).
- `sts.get_caller_identity()` is the AWS "whoami" — free and the best first test of your setup.
- `get_credentials().method` tells you **where** the credentials came from — useful for debugging "why is it using the wrong account?".
- Specific exceptions give actionable messages instead of tracebacks.

**Example 2**
- `list_buckets` + `get_bucket_location` give an S3 inventory.
- A **paginator** walks every page of `describe_instances` (accounts with hundreds of instances return results in pages).
- Tags arrive as a list of `{"Key", "Value"}` dicts; a dict comprehension turns them into a normal dict. Missing `Owner` tags are highlighted (tag compliance!).
- `stop_instances(..., DryRun=True)` checks permissions: the error code `DryRunOperation` means "you would be allowed", and nothing is stopped.

## 7. Expected Output

**Example 1:**

```text
Account : 123456789012
Caller  : assumed-role/AWSReservedSSO_DevOpsLearner_abc123/satya
Region  : ap-south-1
Credential source: sso
```

**Example 2:**

```text
S3 buckets: 3
  learning-artifacts-123456789012  ap-south-1   created 2026-09-14
  ml-datasets-demo-123456789012    ap-south-1   created 2026-10-02
  tf-state-learning-123456789012   us-east-1    created 2026-08-21
EC2 instances in ap-south-1: 2
  i-0a1b2c3d4e5f60718  t3.micro   running   Name=web-learn    Owner=satya
  i-0f9e8d7c6b5a40312  t3.micro   stopped   Name=scratch      Owner=MISSING
DryRun stop: allowed (nothing was stopped)
```

> ℹ️ boto3 talks to your real AWS account, so the output shown is a sample. Every example is read-only or uses `DryRun=True`; nothing here creates billable resources unless you change it. boto3 must be installed (`pip install boto3`) and credentials configured; otherwise the examples print a friendly 'No AWS credentials found' message.

## 8. Common Mistakes

**1. Hard-coded access keys**

`boto3.client('s3', aws_access_key_id='AKIA...')` leaks keys through Git and images. Use roles/profiles/env vars.

**2. Forgetting pagination**

`describe_instances()` and `list_objects_v2()` return only the first page (e.g. 1000 objects). Use paginators.

**3. Wrong region surprises**

Resources are regional: an empty list may just mean the wrong region. Print `session.region_name` and set `AWS_REGION`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Safe identity check:** Write `whoami()` that returns `Account <id> in <region>` or a friendly message when credentials are missing (catch `NoCredentialsError`) or invalid (`ClientError`).
- **Task 2 (Medium) — S3 bucket sizes:** For each bucket, use the `list_objects_v2` paginator to count objects and total size in MB. Print one line per bucket. (Read-only; free for small buckets.)
- **Task 3 (Practical Challenge) — Tag compliance and dev shutdown (dry-run):** List instances missing an `Owner` tag, then find running instances tagged `Env=dev` and call `stop_instances` with `DryRun=True` unless a variable `APPLY = True` is set. Print what would happen. This is the core of [Project 5](../../projects/05-aws-automation-script/).

## 10. DevOps/MLOps Connection

- **DevOps / Cloud:** cost-saving schedulers (stop dev at night), tag-compliance reports, snapshot/AMI cleanup, S3 lifecycle audits, security checks (public buckets, open security groups) — all boto3.
- **Serverless:** the same code runs inside AWS Lambda with an IAM role — no credentials needed in code.
- **MLOps:** upload datasets and models to S3, start SageMaker training jobs, read model artefacts in serving containers, and register models — boto3 is the glue of ML on AWS.

## 11. Interview Questions

**Q1. What is the difference between a boto3 client and a resource?**

<details><summary>Show answer</summary>

Clients are low-level 1:1 API wrappers returning dicts; resources are higher-level object-oriented abstractions (feature-frozen, available for some services).

</details>

**Q2. How does boto3 find credentials?**

<details><summary>Show answer</summary>

Through the credential provider chain: explicit params, environment variables, shared config/credentials files (profiles/SSO), container credentials, then the EC2 instance metadata role.

</details>

**Q3. How can you test whether you have permission to stop an instance without stopping it?**

<details><summary>Show answer</summary>

Call `stop_instances(..., DryRun=True)`; a `DryRunOperation` error means the call would succeed, `UnauthorizedOperation` means it would not.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 82 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 081](../../08-api-cloud/day-081/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 083 ➡](../../09-data-analysis/day-083/README.md)
