# Day 091 — Practice Tasks: AI vs ML vs Deep Learning

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Classify the technique

**Problem statement:** For each scenario print AI-rule / ML / DL: (1) alert when disk > 90 %, (2) predict next week's traffic from history, (3) detect defects in product photos, (4) chatbot answering runbook questions, (5) cluster similar log messages.

**Input requirements:** No user input required.

**Expected behavior:** Five labelled scenarios with a reason.

**Expected output:**

```text
Alert when disk > 90%          AI-rule  explicit threshold written by a human
Predict next week's traffic    ML       learn trends from historical numbers
Detect defects in photos       DL       images need deep neural networks
Runbook chatbot                DL       generative large language model
Cluster similar log messages   ML       unsupervised learning groups similar text
```

## Task 2 — Medium: Rule vs model

**Problem statement:** Using the Example 1 data, write your own better rule (using both cpu and errors) and compare its correctness with the learned tree.

**Input requirements:** No user input required.

**Expected behavior:** Your rule and the model both get 10/10 (or close).

**Expected output:**

```text
My rule: 10 / 10
Tree   : 10 / 10
```

## Task 3 — Practical Challenge: Where does ML help my pipeline?

**Problem statement:** Create a list of dicts describing 4 DevOps problems (name, has_labels, data_volume, rules_known). Write `recommend(problem)` returning `simple rules`, `supervised ML`, `unsupervised ML` or `collect data first`, and print a recommendation table.

**Input requirements:** No user input required.

**Expected behavior:** A recommendation per problem.

**Expected output:**

```text
Disk full alerts             -> simple rules
Predict deployment failures  -> supervised ML
Group noisy alerts           -> unsupervised ML
Forecast cloud cost          -> collect data first
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
