# Chapter 2: Lists and Dictionaries (Items 11-18)

## Item 11: Know How to Slice Sequences
```python
a = [1, 2, 3, 4, 5, 6, 7, 8]

# Basic slicing
a[:4]   # [1, 2, 3, 4] — first 4
a[-3:]  # [6, 7, 8] — last 3
a[3:5]  # [4, 5]

# Don't use 0 for start or len for end
a[:5]   # GOOD
a[0:5]  # BAD — redundant 0

# Slicing makes a new list (shallow copy)
b = a[:]  # copy of a

# Slice assignment replaces in place
a[2:4] = [10, 11]  # can be different length
```

## Item 12: Avoid Striding and Slicing in a Single Expression
```python
# BAD — confusing stride + slice
x = a[2::2]    # skip start, stride by 2
x = a[-2::-2]  # reverse with stride

# GOOD — separate steps
y = a[::2]     # stride first
z = y[1:3]     # then slice

# Reverse a sequence
x = a[::-1]    # OK for simple reversal, but avoid combining with slicing
```

## Item 13: Prefer Catch-All Unpacking Over Slicing
```python
# BAD — manual slicing
oldest = ages[0]
rest = ages[1:]

# GOOD — starred expression
oldest, *rest = ages
oldest, second, *rest = ages
first, *middle, last = ages

# Works with any iterable
it = iter(range(10))
first, second, *rest = it
```

- Starred expressions always produce a list (may be empty)
- Cannot have more than one starred expression in a single assignment

## Item 14: Sort by Complex Criteria Using the key Parameter
```python
# Sort with key function
tools = [Tool('drill', 4), Tool('saw', 2)]
tools.sort(key=lambda x: x.weight)

# Multiple criteria — use tuple
tools.sort(key=lambda x: (x.name, x.weight))

# Reverse one criterion using negation (numeric)
tools.sort(key=lambda x: (-x.weight, x.name))

# For non-numeric reverse, use multiple sort passes (stable sort)
tools.sort(key=lambda x: x.name)             # secondary first
tools.sort(key=lambda x: x.weight, reverse=True)  # primary last
```

- Python sort is stable — equal elements maintain relative order
- Use `operator.attrgetter` for attribute access as key

## Item 15: Be Cautious When Relying on dict Insertion Order
- Since Python 3.7, dicts maintain insertion order
- But don't assume all dict-like objects do (e.g., custom classes)
- Use explicit ordering when you need it:

```python
# If order matters and you're creating a protocol
class MyDB:
    def __init__(self):
        self._data = {}

    # Be explicit that order is part of the contract
```

- For **kwargs, insertion order is preserved
- Standard dict methods (keys, values, items) follow insertion order

## Item 16: Prefer get Over in and KeyError to Handle Missing Dictionary Keys
```python
# BAD — check then access
if key in counters:
    count = counters[key]
else:
    count = 0
counters[key] = count + 1

# BAD — try/except
try:
    count = counters[key]
except KeyError:
    count = 0
counters[key] = count + 1

# GOOD — use get
count = counters.get(key, 0)
counters[key] = count + 1

# For complex default values, consider setdefault or defaultdict
```

## Item 17: Prefer defaultdict Over setdefault to Handle Missing Items in Internal State
```python
from collections import defaultdict

# BAD — setdefault (confusing API)
visits = {}
visits.setdefault('France', []).append('Paris')

# GOOD — defaultdict
visits = defaultdict(list)
visits['France'].append('Paris')
```

- `defaultdict` is clearer when you control the dict creation
- `setdefault` is better when you don't control the dict (external data)

## Item 18: Know How to Construct Key-Dependent Default Values with __missing__
```python
# When the default value depends on the key, use __missing__
class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)  # default depends on key
        self[key] = value
        return value

pictures = Pictures()
handle = pictures[path]  # calls __missing__ if path not present
```

- Use when `defaultdict` isn't sufficient (default factory doesn't receive the key)
- `__missing__` is called by `__getitem__` when key is not found
