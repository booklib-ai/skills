# Chapter 1: Pythonic Thinking (Items 1-10)

## Item 1: Know Which Version of Python You're Using
- Use `python3` explicitly, not `python`
- Check version with `python3 --version` or `sys.version_info`
- Python 2 is end-of-life; always target Python 3

## Item 2: Follow the PEP 8 Style Guide
**Whitespace:**
- Use 4 spaces for indentation (never tabs)
- Lines should be 79 characters or fewer
- Continuations should be indented by 4 extra spaces
- Put two blank lines before/after top-level functions and classes
- One blank line between methods in a class

**Naming:**
- Functions, variables, attributes: `lowercase_underscore`
- Protected instance attributes: `_leading_underscore`
- Private instance attributes: `__double_leading_underscore`
- Classes and exceptions: `CapitalizedWord`
- Module-level constants: `ALL_CAPS`
- Instance methods use `self` as first parameter; class methods use `cls`

**Expressions & Statements:**
- Use inline negation (`if a is not b`) instead of negating positive (`if not a is b`)
- Don't check for empty containers with length (`if len(list) == 0`); use `if not list`
- Use `if list` to check for non-empty
- Avoid single-line `if`, `for`, `while`, `except`
- Always use absolute imports, not relative
- Put imports at top in order: stdlib, third-party, local

**Tools:** Use `pylint` for static analysis, `black` for formatting.

## Item 3: Know the Differences Between bytes and str
- `bytes` contains raw unsigned 8-bit values; `str` contains Unicode code points
- Use helper functions to convert between them:

```python
# BAD
def to_str(data):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data

# GOOD — be explicit about encoding
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value
```

- Use `'rb'` and `'wb'` modes for binary file I/O
- Specify encoding explicitly: `open(path, 'r', encoding='utf-8')`

## Item 4: Prefer Interpolated F-Strings Over C-style Format Strings and str.format
```python
# BAD — C-style
'Hello, %s. You are %d.' % (name, age)

# BAD — str.format
'Hello, {}. You are {}.'.format(name, age)

# GOOD — f-string
f'Hello, {name}. You are {age}.'

# F-strings support expressions
f'{key!r}: {value:.2f}'
f'result: {some_func(x)}'

# Multi-line f-strings
f'{key:<10} = {value:.2f}'
```

## Item 5: Write Helper Functions Instead of Complex Expressions
- If an expression is hard to read, move it to a helper function
- Clarity over brevity: `if`/`else` is clearer than `or` for defaults

```python
# BAD
values = query_string.get('red', [''])
red = int(values[0]) if values[0] else 0

# GOOD
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default

red = get_first_int(values, 'red')
```

## Item 6: Prefer Multiple Assignment Unpacking Over Indexing
```python
# BAD
item = ('Peanut Butter', 3.50)
name = item[0]
price = item[1]

# GOOD
name, price = item

# Works with nested structures
((name1, cal1), (name2, cal2)) = snacks

# Use _ for unused values
_, price = item

# Swap without temp variable
a, b = b, a
```

## Item 7: Prefer enumerate Over range
```python
# BAD
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print(f'{i + 1}: {flavor}')

# GOOD
for i, flavor in enumerate(flavor_list):
    print(f'{i + 1}: {flavor}')

# Start from a different index
for i, flavor in enumerate(flavor_list, 1):
    print(f'{i}: {flavor}')
```

## Item 8: Use zip to Process Iterators in Parallel
```python
# BAD
for i in range(len(names)):
    print(f'{names[i]}: {counts[i]}')

# GOOD
for name, count in zip(names, counts):
    print(f'{name}: {count}')

# When lengths differ, use zip_longest
from itertools import zip_longest
for name, count in zip_longest(names, counts, fillvalue=0):
    print(f'{name}: {count}')
```

- `zip` truncates to shortest iterator (use `itertools.zip_longest` if needed)
- zip is lazy — produces one tuple at a time

## Item 9: Avoid else Blocks After for and while Loops
- `else` on loops runs when the loop completes *without* `break`
- This is counterintuitive and confuses readers
- Instead, use a helper function with early return:

```python
# BAD — confusing else on loop
for i in range(n):
    if condition(i):
        break
else:
    handle_no_break()

# GOOD — helper function
def find_match(n):
    for i in range(n):
        if condition(i):
            return i
    return None  # explicit "not found"

result = find_match(n)
if result is None:
    handle_no_match()
```

## Item 10: Prevent Repetition with Assignment Expressions (Walrus Operator)
```python
# BAD — repeated call or extra variable
count = fresh_fruit.get('lemon', 0)
if count:
    make_lemonade(count)

# GOOD — walrus operator
if count := fresh_fruit.get('lemon', 0):
    make_lemonade(count)

# Useful in while loops
while chunk := f.read(8192):
    process(chunk)

# Useful in comprehensions
result = [y for x in data if (y := f(x)) is not None]
```

- Use `:=` when you need to both assign and test a value
- Don't overuse — only when it clearly reduces repetition
