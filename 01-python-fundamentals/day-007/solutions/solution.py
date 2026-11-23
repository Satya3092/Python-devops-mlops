"""
Day 007 — Arithmetic Operators: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
replicas = 7
remainder = replicas % 2
print("7 % 2 =", remainder)
print("Even" if remainder == 0 else "Odd")

# ===== Task 2 =====
backup_duration = 9876
hours, rest = divmod(backup_duration, 3600)
minutes, seconds = divmod(rest, 60)
print(hours, "h", minutes, "m", seconds, "s")

# ===== Task 3 =====
HOURS_PER_MONTH = 730
ec2_monthly = 0.0416 * HOURS_PER_MONTH
ebs_monthly = 100 * 0.08
transfer_monthly = 250 * 0.09
total_monthly = ec2_monthly + ebs_monthly + transfer_monthly
print("EC2:", round(ec2_monthly, 2), "EBS:", round(ebs_monthly, 2), "Transfer:", round(transfer_monthly, 2))
print("Monthly total: $", round(total_monthly, 2))
print("Yearly total: $", round(total_monthly * 12, 2))
print("Instances within $200/month:", int(200 // ec2_monthly))
