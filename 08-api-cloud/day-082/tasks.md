# Day 082 — Practice Tasks: Boto3 Introduction and AWS SDK

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Safe identity check

**Problem statement:** Write `whoami()` that returns `Account <id> in <region>` or a friendly message when credentials are missing (catch `NoCredentialsError`) or invalid (`ClientError`).

**Input requirements:** No user input required.

**Expected behavior:** Either the account line or the friendly message.

**Expected output:**

```text
Without credentials -> No AWS credentials found. Run 'aws configure sso' or attach an IAM role.
With credentials    -> Account 123456789012 in ap-south-1
```

## Task 2 — Medium: S3 bucket sizes

**Problem statement:** For each bucket, use the `list_objects_v2` paginator to count objects and total size in MB. Print one line per bucket. (Read-only; free for small buckets.)

**Input requirements:** No user input required.

**Expected behavior:** Object count and size per bucket.

**Expected output:**

```text
learning-artifacts-123456789012: 14 objects, 2.37 MB
ml-datasets-demo-123456789012: 3 objects, 41.80 MB
tf-state-learning-123456789012: 1 objects, 0.01 MB
```

## Task 3 — Practical Challenge: Tag compliance and dev shutdown (dry-run)

**Problem statement:** List instances missing an `Owner` tag, then find running instances tagged `Env=dev` and call `stop_instances` with `DryRun=True` unless a variable `APPLY = True` is set. Print what would happen. This is the core of [Project 5](../../projects/05-aws-automation-script/).

**Input requirements:** No user input required.

**Expected behavior:** Untagged instances and a dry-run stop message.

**Expected output:**

```text
Instances missing the Owner tag:
  i-0f9e8d7c6b5a40312 (stopped) Name=scratch
Dev instances to stop: ['i-0a1b2c3d4e5f60719']
DryRun for i-0a1b2c3d4e5f60719: allowed - re-run with --apply to really stop it
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
