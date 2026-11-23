# Project 5 — AWS Automation Script

**Phase:** after Day 82 · **Difficulty:** 🟠 Intermediate+ · **Concepts:** boto3, safe AWS authentication, S3, EC2, argparse, logging, error handling

`aws_tool.py` is a small, **safe-by-default** AWS automation CLI:

| Command | What it does | Changes anything? |
|---|---|---|
| `whoami` | shows account, caller and credential source | no |
| `s3-list` | lists buckets with region, object count and size | no |
| `s3-upload FILE --bucket B [--prefix P]` | uploads a file with SSE-S3 encryption | yes (explicit) |
| `ec2-list [--state running]` | lists instances with Name/Env/Owner tags | no |
| `tag-audit --required Owner Env` | reports instances missing required tags (CSV report) | no |
| `ec2-stop --env dev [--apply]` | stops instances tagged `Env=dev`; **dry-run unless `--apply`** | only with `--apply` |

## 🔐 Authentication — never put keys in code
The script **never** accepts access keys. boto3 finds credentials through the standard chain:

1. **Laptop:** AWS IAM Identity Center (SSO): `aws configure sso --profile learning` → `export AWS_PROFILE=learning` → `aws sso login`.
2. **EC2 / ECS / EKS / Lambda:** attach an **IAM role** (instance profile, task role, IRSA/Pod Identity).
3. **GitHub Actions:** use **OIDC** with `aws-actions/configure-aws-credentials` to assume a role (no stored secrets).
4. Environment variables (`AWS_ACCESS_KEY_ID`...) only for short-lived credentials.

Select the region with `--region` or `AWS_REGION`.

### Least-privilege IAM policy for this tool
See [`iam-policy.json`](iam-policy.json). It allows read-only listing, uploads to **one** bucket, and stopping only instances tagged `Env=dev`.

## 💰 Free Tier & cost safety
- `whoami`, `s3-list`, `ec2-list`, `tag-audit` are **read-only** API calls (free).
- `ec2-stop` defaults to `DryRun=True` — it only checks permissions.
- If you create practice resources: use free-tier eligible types (`t2.micro`/`t3.micro` where eligible), tag them `Purpose=learning`, and delete them the same day.
- Create an **AWS Budget** alert (e.g. $5/month) before experimenting and check **Billing → Bills** weekly.
- Beware of NAT Gateways, unattached Elastic IPs, old EBS snapshots and large S3 transfers.

## Usage
```bash
pip install boto3
export AWS_PROFILE=learning AWS_REGION=ap-south-1
python aws_tool.py whoami
python aws_tool.py s3-list
python aws_tool.py ec2-list --state running
python aws_tool.py tag-audit --required Owner Env --output tag-report.csv
python aws_tool.py ec2-stop --env dev             # dry run: shows what WOULD be stopped
python aws_tool.py ec2-stop --env dev --apply     # really stops them
python aws_tool.py s3-upload report.csv --bucket my-learning-bucket --prefix reports/
```

Sample output:
```text
$ python aws_tool.py ec2-stop --env dev
[DRY RUN] would stop i-0a1b2c3d4e5f60719 (dev-api, t3.micro) - permission check: allowed
1 instance(s) matched. Re-run with --apply to stop them.
```

## Automate it
Run `ec2-stop --env dev --apply` every evening with an EventBridge schedule + Lambda (same code, IAM role) or a cron job on a management host — a classic FinOps saving.

## Testing without AWS
The logic is separated from the AWS calls so you can unit-test it with `botocore.stub.Stubber` or the [moto](https://github.com/getmoto/moto) library (`pip install moto`), which fakes AWS locally. See `test_aws_tool.py`.
