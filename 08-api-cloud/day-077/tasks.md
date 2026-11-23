# Day 077 — Practice Tasks: REST API Concepts

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Map CRUD to HTTP

**Problem statement:** Print a table mapping these operations on a Kubernetes `deployments` resource to method + path: list, get `api`, create, update `api`, delete `api` (namespace `prod`, base `/apis/apps/v1/namespaces/prod/deployments`).

**Input requirements:** No user input required.

**Expected behavior:** Five rows like `GET /apis/apps/v1/namespaces/prod/deployments/api`.

**Expected output:**

```text
list   GET    /apis/apps/v1/namespaces/prod/deployments
get    GET    /apis/apps/v1/namespaces/prod/deployments/api
create POST   /apis/apps/v1/namespaces/prod/deployments
update PUT    /apis/apps/v1/namespaces/prod/deployments/api
delete DELETE /apis/apps/v1/namespaces/prod/deployments/api
```

## Task 2 — Medium: Filter via query params

**Problem statement:** Using the mock API and `urllib`, list servers with `env=prod` and then `env=dev`, printing names and the `total` field.

**Input requirements:** No user input required.

**Expected behavior:** prod: web-01, web-02; dev: batch-01.

**Expected output:**

```text
prod ['web-01', 'web-02'] total: 2
dev ['batch-01'] total: 1
```

## Task 3 — Practical Challenge: Paginate everything

**Problem statement:** Create 5 extra servers via POST, then write `get_all(per_page=2)` that keeps requesting pages until all items (according to `total`) are collected. Print how many requests were needed and all names.

**Input requirements:** No user input required.

**Expected behavior:** 8 servers collected in 4 requests.

**Expected output:**

```text
8 servers collected in 4 requests
['web-01', 'web-02', 'batch-01', 'extra-0', 'extra-1', 'extra-2', 'extra-3', 'extra-4']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
