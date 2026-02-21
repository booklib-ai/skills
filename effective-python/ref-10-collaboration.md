# Chapter 10: Collaboration (Items 86-90)

## Item 86: Consider Module-Scoped Code to Configure Deployment Environments
```python
# config.py
import sys

# Module-scoped code runs at import time
if sys.platform == 'win32':
    DB_PATH = r'C:\data\mydb.sqlite'
else:
    DB_PATH = '/data/mydb.sqlite'

# Use environment variables for deployment config
import os
ENVIRONMENT = os.environ.get('APP_ENV', 'development')

if ENVIRONMENT == 'production':
    DEBUG = False
    DATABASE_URL = os.environ['DATABASE_URL']
else:
    DEBUG = True
    DATABASE_URL = 'sqlite:///dev.db'
```

- Module-level code executes once at import time
- Use it for deployment configuration, feature flags
- Keep it minimal — complex logic at import time slows startup
- Prefer environment variables over hardcoded conditions

## Item 87: Define a Root Exception to Insulate Callers from APIs
```python
# mypackage/exceptions.py
class Error(Exception):
    """Base class for all exceptions in this package."""

class InvalidInputError(Error):
    """Raised when input validation fails."""

class AuthenticationError(Error):
    """Raised when authentication fails."""

class InternalError(Error):
    """Raised for unexpected internal errors."""

# Callers can catch all package errors
try:
    result = mypackage.do_something()
except mypackage.Error:
    # Catches any error from this package
    logging.exception('Error from mypackage')
except Exception:
    # Catches unexpected errors (bugs)
    logging.exception('Unexpected error')
    raise
```

- Define a root `Error` class for your package/module
- All custom exceptions inherit from it
- Callers can catch the root to handle all your errors
- Three levels: root error (known API errors), specific errors, Exception (bugs)
- This insulates callers from internal changes to your exception hierarchy

## Item 88: Know How to Break Circular Dependencies
```python
# BAD — circular import
# module_a.py
from module_b import B
class A:
    def use_b(self):
        return B()

# module_b.py
from module_a import A  # ImportError: circular!
class B:
    def use_a(self):
        return A()

# FIX 1 — import at function call time
# module_a.py
class A:
    def use_b(self):
        from module_b import B  # lazy import
        return B()

# FIX 2 — restructure to remove the cycle
# Move shared code to a third module

# FIX 3 — use import module, not from module import
import module_b
class A:
    def use_b(self):
        return module_b.B()
```

**Strategies (in order of preference):**
1. **Restructure** — move shared code to a common module
2. **Import at use time** — put import inside the function
3. **Import the module** — use `import module` instead of `from module import name`

## Item 89: Consider warnings to Refactor and Migrate Usage
```python
import warnings

def old_function():
    """Deprecated: use new_function instead."""
    warnings.warn(
        'old_function is deprecated, use new_function',
        DeprecationWarning,
        stacklevel=2  # point to caller, not this function
    )
    return new_function()

# Callers see:
# DeprecationWarning: old_function is deprecated, use new_function
#   result = old_function()  # <-- points to their code
```

- Use `DeprecationWarning` for API migrations
- `stacklevel=2` makes the warning point to the caller's code
- Use `warnings.filterwarnings` to control warning behavior
- In tests, use `warnings.catch_warnings` to verify warnings are raised:
```python
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    old_function()
    assert len(w) == 1
    assert issubclass(w[0].category, DeprecationWarning)
```

## Item 90: Consider Static Analysis via typing to Obviate Bugs
```python
from typing import List, Dict, Optional, Tuple, Union
from typing import Protocol  # Python 3.8+

# Basic type annotations
def greet(name: str) -> str:
    return f'Hello, {name}'

# Collections
def process(items: List[int]) -> Dict[str, int]:
    return {'total': sum(items)}

# Optional (can be None)
def find(name: str) -> Optional[str]:
    ...

# Protocol for structural typing (duck typing)
class Readable(Protocol):
    def read(self) -> str:
        ...

def process_input(source: Readable) -> str:
    return source.read()

# Generic classes
from typing import Generic, TypeVar
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()
```

- Use type annotations for documentation and static analysis
- Run `mypy` for type checking: `mypy --strict mymodule.py`
- Use `Protocol` for structural typing (no inheritance needed)
- Type hints are not enforced at runtime (use `mypy` to check)
- Modern syntax (Python 3.10+): `list[int]` instead of `List[int]`, `X | Y` instead of `Union[X, Y]`
