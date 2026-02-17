# Chapter 3: Functions (Items 19-26)

## Item 19: Never Unpack More Than Three Variables When Functions Return Multiple Values
```python
# BAD — too many unpacked values, confusing
minimum, maximum, average, median, count = get_stats(data)

# GOOD — return a lightweight class or namedtuple
from collections import namedtuple

Stats = namedtuple('Stats', ['minimum', 'maximum', 'average', 'median', 'count'])

def get_stats(data):
    return Stats(
        minimum=min(data),
        maximum=max(data),
        average=sum(data)/len(data),
        median=find_median(data),
        count=len(data)
    )

result = get_stats(data)
print(result.average)
```

- Three or fewer values is fine to unpack
- More than three: use a namedtuple, dataclass, or custom class

## Item 20: Prefer Raising Exceptions to Returning None
```python
# BAD — None is ambiguous
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

# Caller can't distinguish None from 0
result = careful_divide(0, 5)  # returns 0.0
if not result:  # BUG: treats 0.0 as failure

# GOOD — raise an exception
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e

# ALSO GOOD — type hints with Never-None return
def careful_divide(a: float, b: float) -> float:
    """Raises ValueError on invalid inputs."""
    if b == 0:
        raise ValueError('Invalid inputs')
    return a / b
```

## Item 21: Know How Closures Interact with Variable Scope
```python
# Closures capture variables from enclosing scope
def sort_priority(values, group):
    found = False
    def helper(x):
        nonlocal found  # REQUIRED to modify enclosing variable
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)
    return found
```

- Without `nonlocal`, assignment creates a new local variable
- Prefer returning state over using `nonlocal` for complex cases
- For complex state, use a helper class instead

## Item 22: Reduce Visual Noise with Variable Positional Arguments (*args)
```python
# Accept variable args
def log(message, *values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('My numbers', 1, 2)
log('Hi')

# Pass a sequence as *args
favorites = [7, 33, 99]
log('Favorites', *favorites)
```

**Caveats:**
- `*args` are converted to a tuple (memory issue with generators)
- Adding positional args before *args breaks callers if not careful
- Use keyword-only args after *args for new parameters

## Item 23: Provide Optional Behavior with Keyword Arguments
```python
def flow_rate(weight_diff, time_diff, *, period=1):  # period is keyword-only
    return (weight_diff / time_diff) * period

# Callers must use keyword
flow_rate(1, 2, period=3600)
flow_rate(1, 2, 3600)  # TypeError!
```

- Keyword args make function calls more readable
- They provide default values for optional behavior
- Can be added to existing functions without breaking callers

## Item 24: Use None and Docstrings to Specify Dynamic Default Arguments
```python
# BAD — mutable default is shared across calls!
def log(message, when=datetime.now()):  # BUG: evaluated once at import
    print(f'{when}: {message}')

# GOOD — use None sentinel
def log(message, when=None):
    """Log a message with a timestamp.

    Args:
        message: Message to print.
        when: datetime of when the message occurred.
            Defaults to the present time.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')
```

- **Never use mutable objects** as default argument values (lists, dicts, sets, datetime.now())
- Use `None` and document the actual default in the docstring
- This also applies to type hints: `when: Optional[datetime] = None`

## Item 25: Enforce Clarity with Keyword-Only and Positional-Only Arguments
```python
# Keyword-only: after * in signature
def safe_division(number, divisor, *,
                  ignore_overflow=False,
                  ignore_zero_division=False):
    pass

# Positional-only: before / in signature (Python 3.8+)
def safe_division(numerator, denominator, /,
                  *, ignore_overflow=False):
    pass

# Combined: positional-only / regular / keyword-only
def safe_division(numerator, denominator, /,
                  ndigits=10, *,
                  ignore_overflow=False):
    pass
```

- `/` separates positional-only from regular params
- `*` separates regular from keyword-only params
- Use positional-only for params where the name is an implementation detail
- Use keyword-only for boolean flags and optional configuration

## Item 26: Define Function Decorators with functools.wraps
```python
from functools import wraps

# BAD — decorator hides original function metadata
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args}, {kwargs}) -> {result}')
        return result
    return wrapper

# GOOD — preserves function metadata
def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args}, {kwargs}) -> {result}')
        return result
    return wrapper
```

- `@wraps` copies the inner function's metadata (__name__, __module__, __doc__)
- Without it, debugging tools, serializers, and `help()` break
- **Always** use `@wraps` on decorator wrapper functions
