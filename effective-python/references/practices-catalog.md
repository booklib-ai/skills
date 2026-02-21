# Effective Python — Practices Catalog

The 20 most impactful items from Brett Slatkin's *Effective Python* (2nd Edition),
each with the problem it solves, the Pythonic solution, and a before/after code example.

---

## Item 4 — Prefer Interpolated F-Strings Over C-style Format Strings and str.format

**Problem:** `%` format strings are verbose and error-prone with multiple values. `.format()` is better but still cluttered with braces and positional indices. Both separate the format template from the values being formatted.

**Solution:** Use f-strings — they embed expressions directly in string literals, are more readable, and support the full power of format specifiers inline.

```python
# Before
name, age = "Alice", 30
msg = "User %s is %d years old" % (name, age)
msg = "User {} is {} years old".format(name, age)

# After
msg = f"User {name} is {age} years old"
msg = f"Pi to 4 places: {3.14159:.4f}"
```

---

## Item 6 — Prefer Multiple Assignment Unpacking Over Indexing

**Problem:** Accessing sequence elements by index (`pair[0]`, `pair[1]`) is opaque — the reader must know what position 0 or 1 represents. It is verbose and error-prone when indices change.

**Solution:** Unpack sequences into named variables in a single assignment. The names document meaning; the structure enforces the expected shape.

```python
# Before
item = ("Alice", 25, "engineer")
name = item[0]
age = item[1]
role = item[2]

# After
name, age, role = item
first, *rest = items          # catch-all unpacking
head, *middle, tail = items   # discard the middle
```

---

## Item 7 — Prefer enumerate Over range for Indexed Iteration

**Problem:** `for i in range(len(sequence))` is verbose and indirect. It requires manually indexing the sequence on each iteration, which is error-prone and harder to read.

**Solution:** Use `enumerate(sequence)` to get both the index and value together. Pass a `start` argument to control the counter's starting value.

```python
# Before
flavors = ["vanilla", "chocolate", "strawberry"]
for i in range(len(flavors)):
    print(f"{i}: {flavors[i]}")

# After
for i, flavor in enumerate(flavors, start=1):
    print(f"{i}: {flavor}")
```

---

## Item 8 — Use zip to Process Iterators in Parallel

**Problem:** Iterating over two related sequences using a shared index is verbose and fragile. If the sequences have different lengths, off-by-one bugs or IndexError occur silently.

**Solution:** Use `zip()` to pair up items from multiple sequences. Use `itertools.zip_longest()` when sequences may have different lengths and you want to handle all items.

```python
# Before
for i in range(len(names)):
    print(f"{names[i]}: {scores[i]}")

# After
from itertools import zip_longest
for name, score in zip(names, scores):
    print(f"{name}: {score}")
for name, score in zip_longest(names, scores, fillvalue=0):
    print(f"{name}: {score}")
```

---

## Item 20 — Prefer Raising Exceptions to Returning None

**Problem:** Functions that return `None` to signal failure require callers to check the return value — and if they forget, the `None` silently propagates until it crashes somewhere unrelated. `None` and `0`, `""`, `[]` all evaluate as falsy, making the check ambiguous.

**Solution:** Raise an exception for failure cases. Callers that want to handle the failure use `try/except`; callers that don't care let the exception propagate. The failure is never silently ignored.

```python
# Before
def parse_ratio(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None  # caller may forget to check

result = parse_ratio(5, 0)
if result:  # BUG: 0.0 is also falsy!
    print(result)

# After
def parse_ratio(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError(f"parse_ratio({a}, {b}): b must be non-zero")
```

---

## Item 24 — Use None and Docstrings to Specify Dynamic Default Arguments

**Problem:** Using a mutable object (list, dict) or dynamic expression (`datetime.now()`) as a default argument value is evaluated once at function definition time, not at call time. All callers share the same default object, leading to subtle, hard-to-find bugs.

**Solution:** Use `None` as the default and initialize the mutable/dynamic value inside the function body. Document the actual default in the docstring.

```python
# Before — BUG: all calls share the same list
def log(message, when=datetime.now(), tags=[]):
    tags.append("debug")  # mutates the shared default!
    print(f"{when}: {message} {tags}")

# After
def log(message, when=None, tags=None):
    """Log a message with a timestamp.
    
    Args:
        when: Timestamp for the log entry. Defaults to now.
        tags: List of tags. Defaults to an empty list.
    """
    if when is None:
        when = datetime.now()
    if tags is None:
        tags = []
    tags.append("debug")
    print(f"{when}: {message} {tags}")
```

---

## Item 25 — Enforce Clarity with Keyword-Only and Positional-Only Arguments

**Problem:** Functions with multiple boolean or configuration parameters are ambiguous at the call site. `safe_divide(1.0, 5.0, True, False)` — what do `True` and `False` mean? Callers can pass args in the wrong order and get no error.

**Solution:** Use keyword-only arguments (after `*` or `*args`) to force callers to name certain parameters. Use positional-only arguments (before `/`) to prevent callers from naming implementation details.

```python
# Before — ambiguous call
def safe_divide(number, divisor, ignore_overflow, ignore_zero):
    ...
safe_divide(1.0, 5.0, True, False)  # what does True mean?

# After — keyword-only enforces clarity
def safe_divide(number, divisor, *, ignore_overflow=False, ignore_zero=False):
    ...
safe_divide(1.0, 5.0, ignore_zero=True)  # clear at the call site
```

---

## Item 26 — Define Function Decorators with functools.wraps

**Problem:** A decorator replaces the wrapped function with a new wrapper function. Without `functools.wraps`, the wrapped function loses its `__name__`, `__doc__`, `__module__`, and other metadata. This breaks debugging, documentation tools, and introspection.

**Solution:** Apply `@functools.wraps(func)` to the inner wrapper function in every decorator.

```python
# Before — metadata lost
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper  # wrapper.__name__ is "wrapper", not "fibonacci"

# After — metadata preserved
import functools
def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper  # wrapper.__name__ is "fibonacci"
```

---

## Item 27 — Use Comprehensions Instead of map and filter

**Problem:** `map()` and `filter()` with `lambda` are verbose and require the reader to mentally parse the lambda, the outer function, and the argument order. They return iterators that must be explicitly materialized.

**Solution:** Use list, dict, and set comprehensions. They are more readable, support conditions inline, and work naturally for all collection types.

```python
# Before
squares_of_evens = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(10))))

# After
squares_of_evens = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
square_map = {x: x**2 for x in range(10)}

# Set comprehension
unique_lengths = {len(name) for name in names}
```

---

## Item 30 — Consider Generators Instead of Returning Lists

**Problem:** A function that builds and returns a list must hold the entire result in memory before the first item is available to the caller. For large sequences, this wastes memory and delays the first result.

**Solution:** Use `yield` to make the function a generator. The caller receives items one at a time; no full list is ever built in memory. The generator is lazy — it computes only what the caller consumes.

```python
# Before — entire list built in memory
def index_words(text):
    result = []
    for i, char in enumerate(text):
        if i == 0 or char == " ":
            result.append(i)
    return result

# After — generator, one item at a time
def index_words(text):
    for i, char in enumerate(text):
        if i == 0 or char == " ":
            yield i
```

---

## Item 37 — Compose Classes Instead of Nesting Many Levels of Built-in Types

**Problem:** Deeply nested dicts, lists, and tuples (e.g., a dict of dicts of lists of tuples) are hard to read, document, and extend. Adding a new field requires updating every place that constructs or unpacks the data.

**Solution:** When a structure exceeds two levels of nesting, define small helper classes or use `collections.namedtuple` / `dataclasses.dataclass`. This provides named access, documentation, and the ability to add methods later.

```python
# Before — opaque nested dict
grades = {"Alice": {"Math": [90, 88], "English": [75, 82]}}

# After — self-documenting classes
from dataclasses import dataclass, field
@dataclass
class Subject:
    name: str
    scores: list = field(default_factory=list)
    def average(self): return sum(self.scores) / len(self.scores)

@dataclass
class Student:
    name: str
    subjects: dict = field(default_factory=dict)
```

---

## Item 40 — Initialize Parent Classes with super()

**Problem:** Calling `ParentClass.__init__(self)` directly breaks with multiple inheritance and the Method Resolution Order (MRO). It can call a parent's `__init__` twice or miss it entirely when the class hierarchy is diamond-shaped.

**Solution:** Always use `super().__init__()` without arguments. Python resolves the correct class to call based on the MRO, making multiple inheritance predictable.

```python
# Before — fragile with multiple inheritance
class MyChild(ParentA, ParentB):
    def __init__(self):
        ParentA.__init__(self)  # may call Base twice in diamond inheritance
        ParentB.__init__(self)

# After — MRO-correct
class MyChild(ParentA, ParentB):
    def __init__(self):
        super().__init__()  # follows MRO, each parent called exactly once
```

---

## Item 44 — Use Plain Attributes Instead of Get and Set Methods

**Problem:** Java-style getter/setter method pairs (`get_voltage()`, `set_voltage()`) are verbose and un-Pythonic. They add noise without benefit when no special behavior is needed.

**Solution:** Use plain public attributes by default. If you later need validation, caching, or computed values, migrate to `@property` without changing the external interface.

```python
# Before — Java-style
class OldResistor:
    def __init__(self, ohms):
        self._ohms = ohms
    def get_ohms(self): return self._ohms
    def set_ohms(self, ohms): self._ohms = ohms

# After — plain attribute first
class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms  # plain attribute; add @property later if needed
        self.voltage = 0
        self.current = 0
```

---

## Item 45 — Consider @property Instead of Refactoring Attributes

**Problem:** Once a class is published with a plain attribute, changing it to a method breaks all callers. If behavior (validation, computation, side effects) is needed on attribute access, the API must change.

**Solution:** Use `@property` to add behavior to attribute access while keeping the same attribute-style interface. The caller never knows whether it's a stored value or a computed one.

```python
# Before — breaks callers if changed to a method
class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):  # caller must use circle.area()
        return 3.14 * self.radius ** 2

# After — area looks like an attribute
class Circle:
    def __init__(self, radius):
        self.radius = radius
    @property
    def area(self):     # caller uses circle.area (no parentheses)
        return 3.14 * self.radius ** 2
```

---

## Item 53 — Use Threads for Blocking I/O, Avoid for Parallelism

**Problem:** Python's Global Interpreter Lock (GIL) prevents multiple threads from executing Python bytecode simultaneously. Using threads to parallelize CPU-bound work achieves no speedup and adds complexity.

**Solution:** Use threads only for blocking I/O (network calls, disk reads) where threads wait idle most of the time. Use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` for CPU-bound parallelism.

```python
# CPU-bound — threads give no benefit (GIL)
from concurrent.futures import ProcessPoolExecutor
def factorize(number): ...  # CPU work
with ProcessPoolExecutor() as pool:
    results = list(pool.map(factorize, numbers))

# I/O-bound — threads work well
from concurrent.futures import ThreadPoolExecutor
def fetch_url(url): ...  # blocking network I/O
with ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(fetch_url, urls))
```

---

## Item 54 — Use Lock to Prevent Data Races in Threads

**Problem:** When multiple threads read and write shared mutable state without synchronization, the operations interleave unpredictably. The GIL does not protect against data races at the level of compound operations like `counter += 1`.

**Solution:** Use `threading.Lock` to protect all accesses to shared mutable state. Acquire the lock before reading or writing, release it after. Use `with lock:` for automatic release even on exceptions.

```python
# Before — data race: final count is unpredictable
counter = 0
def increment():
    global counter
    counter += 1  # not atomic: read, add, write — can interleave

# After — Lock prevents interleaving
import threading
lock = threading.Lock()
counter = 0
def increment():
    global counter
    with lock:
        counter += 1
```

---

## Item 65 — Take Advantage of Each Block in try/except/else/finally

**Problem:** Developers often use `try/except` with all code inside `try`, catching exceptions that were not intended to be caught. The `else` and `finally` clauses are underused.

**Solution:** Use the full four-part structure: `try` for only the risky operation, `except` for specific exceptions, `else` for code that runs only on success, `finally` for cleanup that always runs.

```python
# Before — too broad, may catch unexpected exceptions
try:
    data = json.loads(text)
    process(data)         # this exception is caught too!
    save(data)
except ValueError:
    log("Invalid JSON")

# After — precise structure
try:
    data = json.loads(text)  # only the risky part
except ValueError as e:
    log(f"Invalid JSON: {e}")
else:
    process(data)            # runs only if no exception
    save(data)
finally:
    cleanup()                # always runs
```

---

## Item 78 — Use TestCase Subclasses for Tests

**Problem:** Writing tests as standalone functions without a `TestCase` class misses built-in helpers: `setUp`/`tearDown` for fixtures, `subTest` for variations, and assertion methods like `assertRaises`, `assertEqual`, `assertAlmostEqual` that produce clear failure messages.

**Solution:** Subclass `unittest.TestCase`. Use `setUp` for common setup and `tearDown` for cleanup. Use `subTest` to run the same test with multiple inputs.

```python
# After — structured TestCase
import unittest
class TestMyFunction(unittest.TestCase):
    def setUp(self):
        self.db = FakeDatabase()
    def tearDown(self):
        self.db.close()
    def test_normal_case(self):
        self.assertEqual(my_function(self.db, 1), "expected")
    def test_multiple_inputs(self):
        cases = [(1, "a"), (2, "b"), (3, "c")]
        for inp, expected in cases:
            with self.subTest(inp=inp):
                self.assertEqual(my_function(self.db, inp), expected)
```

---

## Item 80 — Consider Interactive Debugging with pdb

**Problem:** Adding `print()` statements to debug code produces cluttered output, requires multiple edit-run cycles, and must be cleaned up afterward. It provides no way to interactively explore state.

**Solution:** Use `breakpoint()` (Python 3.7+) to drop into the interactive pdb debugger at a specific line. Step through code, inspect variables, call functions, and modify state interactively. Remove the breakpoint when done.

```python
# Before — print debugging
def complex_function(data):
    print(f"DEBUG: data={data}")  # must be cleaned up
    result = transform(data)
    print(f"DEBUG: result={result}")
    return result

# After — interactive debugger
def complex_function(data):
    breakpoint()  # drops into pdb; type 'n' (next), 's' (step), 'p var' (print)
    result = transform(data)
    return result
```

---

## Item 84 — Write Docstrings for Every Function, Class, and Module

**Problem:** Functions and classes without docstrings force readers to read the implementation to understand the contract. Automated documentation tools (`pydoc`, Sphinx) produce empty or useless output.

**Solution:** Write a docstring for every public module, class, and function. Describe what it does, its arguments, return value, and any exceptions it raises. Use the first line as a one-sentence summary.

```python
# Before — no documentation
def find_anagrams(word, candidates):
    word_letters = Counter(word.lower())
    return [c for c in candidates if Counter(c.lower()) == word_letters]

# After — documented contract
def find_anagrams(word, candidates):
    """Find all anagrams of word in the candidates list.
    
    Args:
        word: The word to find anagrams for. Case-insensitive.
        candidates: Sequence of words to search.
    
    Returns:
        List of strings from candidates that are anagrams of word.
    """
    word_letters = Counter(word.lower())
    return [c for c in candidates if Counter(c.lower()) == word_letters]
```
