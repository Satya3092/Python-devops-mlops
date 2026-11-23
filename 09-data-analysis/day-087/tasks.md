# Day 087 — Practice Tasks: Pandas Series and DataFrames

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Build a DataFrame

**Problem statement:** Create a DataFrame of 4 employees (name, team, salary) from a dict, print it, then print only the names of the `devops` team using `loc`.

**Input requirements:** No user input required.

**Expected behavior:** The table and the devops names.

**Expected output:**

```text
    name    team  salary
0   Asha  devops   95000
1   Ravi    data   88000
2  Meera  devops   99000
3   John      ml  105000
['Asha', 'Meera']
```

## Task 2 — Medium: Derived columns

**Problem statement:** Load `house_prices.csv`, add `price_per_sqft` (rounded to 2) and `age_group` (`new` < 10 years, `mid` < 25, `old`), then print the first 5 rows and the average price per sqft per age group.

**Input requirements:** No user input required.

**Expected behavior:** Five rows and three group averages.

**Expected output:**

```text
   size_sqft  bedrooms  age_years  ...   price  price_per_sqft  age_group
0       3241         6          4  ...  566400          174.76        new
1       1922         4         22  ...  324000          168.57        mid
2        888         1          7  ...  125000          140.77        new
3        857         1         39  ...  156700          182.85        old
4       3420         5         34  ...  517800          151.40        old

[5 rows x 7 columns]
new 168.31
mid 158.56
old 146.94
```

## Task 3 — Practical Challenge: Fleet scorecard

**Problem statement:** Load `servers.csv`, add `risk_score = 0.5*cpu + 0.3*memory + 0.2*disk`, rank servers by it (`rank(ascending=False)`), and print the top 5 with host, environment, risk_score (1 decimal) and rank. Then print the mean risk per environment.

**Input requirements:** No user input required.

**Expected behavior:** Top-5 risky servers and environment averages.

**Expected output:**

```text
      hostname environment  risk_score  rank
staging-web-10     staging        81.0     1
staging-web-13     staging        76.5     2
   prod-web-03        prod        69.4     3
    dev-web-17         dev        67.2     4
    dev-web-02         dev        64.2     5
dev 53.3
prod 53.1
staging 58.4
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
