# Day 065 — Practice Tasks: Inheritance, Encapsulation, and Polymorphism

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Shapes

**Problem statement:** Create a base `Shape` with `area()` returning 0 and `describe()`. Create `Circle(r)` and `Square(side)` overriding `area()`. Print the description of a list of shapes and the total area.

**Input requirements:** No user input required.

**Expected behavior:** Two descriptions and the total area.

**Expected output:**

```text
Circle with area 3.14
Square with area 9.00
Total area: 12.14
```

## Task 2 — Medium: Encapsulated thermostat

**Problem statement:** Create `Thermostat` with a `temperature` property whose setter only accepts 10–30 °C (raise ValueError otherwise) and a read-only `history` property returning a copy of all accepted values.

**Input requirements:** No user input required.

**Expected behavior:** Valid changes recorded; invalid one rejected.

**Expected output:**

```text
Rejected: 45 C is outside 10-30 C
Current: 18 History: [20, 23, 18]
```

## Task 3 — Practical Challenge: Deployment strategies

**Problem statement:** Create an abstract `DeploymentStrategy` with `deploy(version, hosts)`. Implement `RollingDeployment(batch_size)`, `BlueGreenDeployment()` and `CanaryDeployment(percent)` that return a list of step strings. Run all three polymorphically for 6 hosts and print the steps.

**Input requirements:** No user input required.

**Expected behavior:** Three different step lists from the same call.

**Expected output:**

```text
== RollingDeployment ==
   deploy v2.0 to ['web-01', 'web-02']
   deploy v2.0 to ['web-03', 'web-04']
   deploy v2.0 to ['web-05', 'web-06']
== BlueGreenDeployment ==
   start green env with v2.0 on 6 new hosts
   run smoke tests on green
   switch load balancer blue -> green
   keep blue for rollback
== CanaryDeployment ==
   deploy v2.0 to canary ['web-01']
   watch error rate for 15 min
   deploy v2.0 to remaining 5 hosts
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
