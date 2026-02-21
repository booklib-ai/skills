# Chapter 9: Testing and Debugging (Items 77-85)

## Item 77: Isolate Tests from Each Other via setUp, tearDown, setUpModule, etc.
```python
import unittest

class DatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests in this class."""
        cls.db = create_test_database()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests in this class."""
        cls.db.close()

    def setUp(self):
        """Run before each test method."""
        self.connection = self.db.connect()
        self.transaction = self.connection.begin()

    def tearDown(self):
        """Run after each test method."""
        self.transaction.rollback()
        self.connection.close()

    def test_query(self):
        result = self.connection.execute('SELECT 1')
        self.assertEqual(result, 1)
```

- `setUp`/`tearDown` run for every test method (isolation)
- `setUpClass`/`tearDownClass` run once per class (expensive setup)
- `setUpModule`/`tearDownModule` run once per module
- Always clean up in tearDown (even if test fails)

## Item 78: Use Mocks to Test Code with Complex Dependencies
```python
from unittest.mock import patch, MagicMock, call

# Mock a function
@patch('mymodule.external_api_call')
def test_process(mock_api):
    mock_api.return_value = {'status': 'ok'}
    result = process_data()
    mock_api.assert_called_once_with(expected_arg)
    assert result == expected_result

# Mock an object's method
def test_with_mock():
    mock_db = MagicMock()
    mock_db.query.return_value = [{'id': 1}]
    service = MyService(db=mock_db)
    result = service.get_items()
    mock_db.query.assert_called_once()

# Verify call order
mock_db.query.assert_has_calls([
    call('SELECT * FROM users'),
    call('SELECT * FROM orders'),
])

# Use spec for type checking
mock = MagicMock(spec=RealClass)
mock.nonexistent_method()  # raises AttributeError
```

- Mock external dependencies (APIs, databases, file systems)
- Use `@patch` to replace modules/objects during tests
- Use `spec=RealClass` to catch API mismatches
- Verify both return values and call patterns
- Use `side_effect` for exceptions or multiple return values:
```python
mock.side_effect = ValueError('error')
mock.side_effect = [1, 2, 3]  # returns different values each call
```

## Item 79: Encapsulate Dependencies to Facilitate Mocking and Testing
```python
# BAD — hard-coded dependency
class DataProcessor:
    def process(self):
        data = requests.get('https://api.example.com/data').json()
        return transform(data)

# GOOD — inject dependency
class DataProcessor:
    def __init__(self, data_fetcher):
        self._fetcher = data_fetcher

    def process(self):
        data = self._fetcher.get_data()
        return transform(data)

# Easy to test
class FakeFetcher:
    def get_data(self):
        return {'test': 'data'}

processor = DataProcessor(FakeFetcher())
result = processor.process()
```

- Dependency injection makes code testable
- Accept dependencies as constructor or method parameters
- Use abstract base classes or protocols to define interfaces
- Fakes/stubs are often clearer than mocks for complex dependencies

## Item 80: Consider Interactive Debugging with pdb
```python
# Drop into debugger at a specific point
def complex_function(data):
    result = step_one(data)
    breakpoint()  # Python 3.7+ (same as pdb.set_trace())
    final = step_two(result)
    return final
```

**Key pdb commands:**
- `n` (next) — execute next line
- `s` (step) — step into function call
- `c` (continue) — continue execution until next breakpoint
- `p expr` — print expression
- `pp expr` — pretty-print expression
- `l` (list) — show current code context
- `w` (where) — show call stack
- `b line` — set breakpoint at line
- `r` (return) — run until current function returns
- `q` (quit) — quit debugger

- Use `breakpoint()` (Python 3.7+) instead of `import pdb; pdb.set_trace()`
- Use `PYTHONBREAKPOINT=0` environment variable to disable all breakpoints
- Use `post_mortem()` to debug after an exception

## Item 81: Use tracemalloc to Understand Memory Usage and Leaks
```python
import tracemalloc

tracemalloc.start()

# ... run code that uses memory ...

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print('Top 10 memory allocations:')
for stat in top_stats[:10]:
    print(stat)

# Compare snapshots to find leaks
snapshot1 = tracemalloc.take_snapshot()
# ... more code ...
snapshot2 = tracemalloc.take_snapshot()
top_stats = snapshot2.compare_to(snapshot1, 'lineno')
```

- `tracemalloc` tracks where memory was allocated
- Use snapshot comparison to find memory leaks
- Shows file and line number of allocations
- Much more useful than `gc` module for debugging memory issues

## Item 82: Know Where to Find Community-Built Modules
- PyPI (Python Package Index) is the main repository
- Use `pip install` to install packages
- Check package health: last update, stars, downloads, issues
- Popular packages: requests, flask, django, pandas, numpy, pytest

## Item 83: Use Virtual Environments for Isolated and Reproducible Dependencies
```bash
# Create virtual environment
python3 -m venv myenv

# Activate
source myenv/bin/activate

# Install packages
pip install flask==2.0.1

# Freeze dependencies
pip freeze > requirements.txt

# Recreate environment
pip install -r requirements.txt
```

- Always use virtual environments for projects
- Never install packages globally with `pip`
- Use `requirements.txt` for reproducible environments
- Consider `pyproject.toml` and modern tools (poetry, pipenv)

## Item 84: Write Docstrings for Every Module, Class, and Function
```python
"""Module docstring: brief description of the module's purpose."""

class MyClass:
    """One-line summary of the class.

    Extended description of the class if needed.

    Attributes:
        attr1: Description of attr1.
        attr2: Description of attr2.
    """

    def method(self, arg1: str, arg2: int = 0) -> bool:
        """One-line summary of method.

        Extended description if needed.

        Args:
            arg1: Description of arg1.
            arg2: Description of arg2. Defaults to 0.

        Returns:
            Description of return value.

        Raises:
            ValueError: When arg1 is empty.
        """
```

- First line: one-line summary ending with period
- Blank line, then extended description if needed
- Document Args, Returns, Raises sections
- Use Google style or NumPy style consistently
- Type hints complement but don't replace docstrings

## Item 85: Use Packages to Organize Modules and Provide Stable APIs
```python
# mypackage/__init__.py
from mypackage.core import (
    PublicClass,
    public_function,
)

__all__ = ['PublicClass', 'public_function']

# mypackage/core.py
class PublicClass:
    ...

def public_function():
    ...

def _private_helper():  # not exported
    ...
```

- Use `__init__.py` to define public API
- Use `__all__` to control `from package import *` behavior
- Keep internal modules private with `_` prefix
- Stable API = external code won't break when internals change
