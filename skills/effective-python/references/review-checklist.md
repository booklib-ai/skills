# Effective Python — Code Review Checklist

Systematic checklist for reviewing Python code against the 90 best practices from
*Effective Python: 90 Specific Ways to Write Better Python* (2nd Edition) by Brett Slatkin.

---

## Chapter 1 — Pythonic Thinking (Items 1–10)

### Style and Idiom
- [ ] **Item 1 — Python version** — Is the code targeting a current, supported Python version? Are any version-specific compatibility shims present that can be removed?
- [ ] **Item 2 — PEP 8 style** — Does the code follow PEP 8? snake_case for functions/variables, PascalCase for classes, UPPER_CASE for module-level constants, 4-space indentation, 79-character lines?
- [ ] **Item 3 — bytes vs. str** — Is the code clear about whether it's operating on `bytes` or `str`? Are encoding/decoding boundaries explicit? Is `open()` called with the correct mode (`'b'` vs. `'t'`)?

### String Formatting
- [ ] **Item 4 — f-strings** — Are f-strings used instead of `%` formatting or `.format()`? Is every formatted string using the simplest, most readable form available?

### Data Unpacking
- [ ] **Item 5 — Helper functions over complex expressions** — Are complex multi-step expressions broken into helper functions with descriptive names?
- [ ] **Item 6 — Unpacking instead of indexing** — Are sequences unpacked directly (`first, second = pair`) instead of accessed by index (`pair[0]`, `pair[1]`)?
- [ ] **Item 7 — enumerate instead of range** — Is `enumerate(sequence)` used instead of `range(len(sequence))` when both the index and value are needed?
- [ ] **Item 8 — zip for parallel iteration** — Is `zip()` used to iterate over multiple sequences in parallel instead of indexing? Is `itertools.zip_longest` used when sequence lengths might differ?

### Control Flow
- [ ] **Item 9 — No else after for/while** — Are `else` blocks after `for` or `while` loops absent? This construct is confusing — use a flag variable or `break` + check instead.
- [ ] **Item 10 — Walrus operator** — Is `:=` used to reduce redundant expressions where appropriate (e.g., assigning and testing in the same expression in a `while` or `if`)? Is it avoided where it would reduce clarity?

---

## Chapter 2 — Lists and Dicts (Items 11–18)

### Sequence Operations
- [ ] **Item 11 — Slicing** — Is slicing used idiomatically? Are start/end omitted when slicing from the beginning or to the end (`a[:5]`, `a[3:]`)? Is stride-slicing (`a[::2]`) with start/end avoided in favor of clarity?
- [ ] **Item 12 — No start, stop, stride together** — Is `a[2::2]` or `a[:-1:2]` avoided in favor of two separate operations? Combining start, stop, and stride in one slice is hard to read.
- [ ] **Item 13 — Catch-all unpacking** — Is starred unpacking (`first, *rest = items`) used instead of slicing for splitting sequences? Is `*_` used to discard unwanted items cleanly?

### Sorting
- [ ] **Item 14 — Sort with key parameter** — Are `sort()` and `sorted()` called with a `key=` function rather than `cmp=` or manual tuple sorting hacks?
- [ ] **Item 15 — Sorting by multiple criteria** — When sorting by multiple fields in different directions, is `key=` with a tuple used, combined with `reverse=True` where needed, or multiple stable sorts applied in reverse priority order?

### Dicts
- [ ] **Item 16 — dict.get with default** — Is `dict.get(key, default)` used instead of checking `key in dict` before accessing? Are `setdefault` or `defaultdict` used for dict initialization patterns?
- [ ] **Item 17 — defaultdict for internal state** — Is `collections.defaultdict` used for dicts where missing keys should be initialized automatically? Is `__missing__` used for more complex initialization logic?
- [ ] **Item 18 — __missing__ for custom defaults** — When `defaultdict` is insufficient (e.g., default value depends on the key), is `__missing__` implemented on a `dict` subclass?

---

## Chapter 3 — Functions (Items 19–26)

### Return Values and Errors
- [ ] **Item 19 — Never unpack more than 3 variables** — Does any function return a tuple of more than 3 elements for unpacking? Use a `namedtuple` or small class instead.
- [ ] **Item 20 — Raise exceptions instead of returning None** — Do functions raise exceptions for failure cases instead of returning `None`? Is `None` used only to mean "no value" — not "error"?

### Closures and Scoping
- [ ] **Item 21 — Closures and variable scope** — Do closures reference variables from the enclosing scope correctly? Is `nonlocal` used when a closure must modify an enclosing variable?
- [ ] **Item 22 — Variable positional arguments with *args** — When a function accepts a variable number of positional args, is `*args` used? Is the caller passing generators directly into `*args` functions (risky — exhausts the generator)?

### Function Arguments
- [ ] **Item 23 — Keyword arguments** — Are functions that accept many arguments using keyword arguments for clarity at the call site?
- [ ] **Item 24 — None for dynamic defaults** — Are mutable objects or dynamic values (lists, dicts, `datetime.now()`) never used as default argument values? Is `None` used as the default with a `if param is None: param = []` pattern?
- [ ] **Item 25 — Keyword-only and positional-only arguments** — Are ambiguous boolean or configuration arguments declared keyword-only (after `*`)? Is the public/private boundary of an API enforced with positional-only args (before `/`)?

### Decorators
- [ ] **Item 26 — functools.wraps on all decorators** — Does every decorator use `@functools.wraps(func)` to preserve the wrapped function's `__name__`, `__doc__`, and other metadata?

---

## Chapter 4 — Comprehensions and Generators (Items 27–36)

### Comprehensions
- [ ] **Item 27 — Comprehensions over map/filter** — Are list/dict/set comprehensions used instead of `map()` and `filter()` with `lambda`? Comprehensions are more readable.
- [ ] **Item 28 — No more than two expressions** — Do all comprehensions contain at most two expressions (e.g., one loop and one condition)? Comprehensions with three or more expressions are harder to read than a plain loop.
- [ ] **Item 29 — No walrus in comprehensions for leaking** — Is `:=` in comprehensions used carefully? Walrus operator assignments in comprehensions can leak scope in unexpected ways.
- [ ] **Item 30 — Generators instead of lists** — When a function produces a sequence for a caller to iterate, does it use `yield` instead of building and returning a list? Does it avoid holding the entire sequence in memory?

### Generators and Iterators
- [ ] **Item 31 — Aware of single-iteration behavior** — Does code that iterates over an iterator do so only once? Is a container (list, tuple) used when multiple iterations are needed?
- [ ] **Item 32 — Iterator protocol** — When implementing a custom iterable, does the class implement `__iter__` returning `self` and `__next__`? Or does `__iter__` return a generator?
- [ ] **Item 33 — yield from for delegation** — Does generator code that delegates to another iterator use `yield from` instead of a manual `for` loop with `yield`?
- [ ] **Item 34 — send for generator communication** — If a generator must receive values from the caller, is `.send()` used? Is the protocol clear and documented?
- [ ] **Item 35 — throw and close on generators** — Are `generator.throw()` and `generator.close()` used for error injection and cleanup when needed?
- [ ] **Item 36 — itertools for complex iteration** — Are `itertools` functions (`chain`, `islice`, `tee`, `zip_longest`, `product`, `permutations`, `combinations`, `groupby`) used instead of hand-rolled equivalents?

---

## Chapter 5 — Classes and Interfaces (Items 37–43)

### Class Design
- [ ] **Item 37 — Compose classes instead of deep nesting** — Are deeply nested dicts/lists/tuples replaced with small helper classes or `namedtuple`/`dataclass`? Is composition preferred over inheritance?
- [ ] **Item 38 — Simple interfaces with functions** — When a simple callback interface is needed, is a plain function (or callable object) accepted instead of defining a single-method interface class?
- [ ] **Item 39 — @classmethod for polymorphic construction** — Are alternative constructors implemented as `@classmethod` methods rather than freestanding functions or `__init__` overloads?
- [ ] **Item 40 — super().__init__() always called** — Does every class that inherits from another call `super().__init__()` in its own `__init__`? Is `super()` used without arguments (Python 3 style)?

### Mix-ins and Attributes
- [ ] **Item 41 — Mix-ins for reusable behavior** — Are mix-ins used for reusable behavior that should be composed into multiple classes? Do mix-ins avoid `__init__` and instance state?
- [ ] **Item 42 — Public attributes over private** — Are attributes defined as public (`self.value`) by default? Is `__private` (name-mangled) used only when deliberate subclass protection is needed? Is `_protected` used to signal "internal use" conventionally?
- [ ] **Item 43 — Inherit from collections.abc** — When defining a custom container type (sequence, mapping, set), does the class inherit from the appropriate `collections.abc` abstract base class?

---

## Chapter 6 — Metaclasses and Attributes (Items 44–51)

### Properties and Descriptors
- [ ] **Item 44 — Plain attributes over getter/setter** — Are plain public attributes used instead of getter/setter method pairs? Java-style `get_value()`/`set_value()` methods are un-Pythonic.
- [ ] **Item 45 — @property for special behavior** — When an attribute access needs validation, lazy computation, or side effects, is `@property` used? Does the getter avoid slow computation or surprising side effects?
- [ ] **Item 46 — @property.setter validates** — Do property setters validate input before assigning? Do setters raise `ValueError` for invalid input rather than silently accepting bad values?
- [ ] **Item 47 — Descriptors for reusable @property logic** — When the same `@property` logic must apply to multiple attributes or multiple classes, is a descriptor class used instead of repeating the property code?

### Metaclasses and Dynamic Attributes
- [ ] **Item 48 — __getattr__, __getattribute__, __setattr__** — Is `__getattr__` used for lazy attribute initialization (called only when attribute is missing)? Is `__getattribute__` avoided unless interception of all attribute access is genuinely needed?
- [ ] **Item 49 — __init_subclass__ for subclass validation** — When a base class needs to validate or register all its subclasses at class definition time, is `__init_subclass__` used instead of a metaclass?
- [ ] **Item 50 — __set_name__ on descriptors** — Do descriptors use `__set_name__` to learn the attribute name they are assigned to, rather than requiring the name to be passed explicitly?
- [ ] **Item 51 — Class decorators over metaclasses** — When class-level transformation is needed, is a class decorator used rather than a metaclass? Metaclasses should be a last resort.

---

## Chapter 7 — Concurrency and Parallelism (Items 52–64)

### Processes and Threads
- [ ] **Item 52 — subprocess for child processes** — Are child processes managed through `subprocess.run()` or `Popen` rather than `os.system()` or `os.popen()`?
- [ ] **Item 53 — Threads only for I/O** — Is the `threading` module used only for blocking I/O concurrency, never for CPU parallelism? Is `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` used for CPU-bound work?
- [ ] **Item 54 — Lock for thread safety** — Is `threading.Lock` (or `RLock`) used to protect all shared mutable state accessed by multiple threads?
- [ ] **Item 55 — Queue for thread coordination** — Is `queue.Queue` used for passing work and results between producer and consumer threads instead of shared mutable lists?

### Coroutines and asyncio
- [ ] **Item 60 — Coroutines for high-concurrency I/O** — Is `asyncio` used for highly concurrent I/O instead of threads when many simultaneous connections are needed?
- [ ] **Item 61 — Blocking I/O never in async** — Does all `async` code use `await` for I/O? Are blocking calls (`requests.get`, `time.sleep`, file reads without `aiofiles`) absent from `async def` functions?
- [ ] **Item 62 — asyncio.run at the entry point** — Is `asyncio.run()` used to start the event loop rather than `loop.run_until_complete()`?
- [ ] **Item 63 — asyncio.gather for concurrent tasks** — When multiple coroutines should run concurrently, is `asyncio.gather()` or `asyncio.create_task()` used instead of awaiting them sequentially?

---

## Chapter 8 — Robustness and Performance (Items 65–79)

### Error Handling
- [ ] **Item 65 — try/except/else/finally structure** — Does error handling use the full `try/except/else/finally` structure correctly? Is `else` used for code that runs only when no exception is raised? Is `finally` used for cleanup?
- [ ] **Item 66 — Reraise with raise** — When catching and reraising exceptions, is bare `raise` used to preserve the original traceback, rather than `raise e` which replaces it?
- [ ] **Item 67 — Exception chaining** — When raising a new exception in response to a caught one, is `raise NewException(...) from original` used to preserve the chain?
- [ ] **Item 73 — datetime for timezone handling** — Is `datetime` (with `pytz` or `zoneinfo`) used for timezone-aware operations instead of the `time` module?

### Data Structures and Performance
- [ ] **Item 70 — Profile before optimizing** — Is any performance optimization justified by profiling output (`cProfile`, `timeit`) rather than intuition?
- [ ] **Item 71 — Prefer deque for FIFO** — Is `collections.deque` used for queues needing efficient append and pop from both ends, rather than a `list` (which makes `list.pop(0)` O(n))?
- [ ] **Item 72 — Consider bisect for sorted sequences** — Is `bisect.bisect_left` / `bisect.insort` used for efficient insertion and search in sorted sequences rather than a linear scan?
- [ ] **Item 73 — heapq for priority queues** — Is `heapq` used for priority queue operations rather than re-sorting a list on every insertion?
- [ ] **Item 74 — Avoid copying on each iteration** — Are large data copies inside loops avoided? Is `memoryview` used for zero-copy slicing of bytes objects?

---

## Chapter 9 — Testing and Debugging (Items 80–85)

### Testing
- [ ] **Item 78 — TestCase and subTest** — Are tests structured as `unittest.TestCase` subclasses with `setUp`/`tearDown`? Is `self.subTest()` used to run variations within a single test method?
- [ ] **Item 79 — Mocks for complex dependencies** — Are external dependencies (network, filesystem, databases, time) mocked using `unittest.mock.Mock` or `MagicMock` in tests?
- [ ] **Item 80 — Encapsulate dependencies** — Is code structured so dependencies can be injected (passed as arguments or set as attributes) rather than hardcoded? Does testability drive class design?

### Debugging
- [ ] **Item 81 — pdb for debugging** — Is `breakpoint()` (Python 3.7+) used for interactive debugging rather than scatter-gunning print statements?
- [ ] **Item 82 — tracemalloc for memory** — Is `tracemalloc` used to identify the source of unexpected memory growth rather than guessing?

---

## Chapter 10 — Collaboration (Items 86–90)

- [ ] **Item 84 — Docstrings for all public APIs** — Do all public modules, classes, and functions have docstrings? Do docstrings describe *what* the function does, its arguments, return value, and any exceptions raised?
- [ ] **Item 85 — Packages for API namespacing** — Is code organized into packages with `__init__.py` files? Does the package's `__init__.py` expose a clean public API?
- [ ] **Item 86 — Root exception for packages** — Does each package define its own root exception class that all other package exceptions inherit from? Does this let callers catch all package errors with one `except` clause?
- [ ] **Item 87 — Circular imports avoided** — Are there any circular imports between modules? Are they resolved by restructuring or by moving imports inside functions?
- [ ] **Item 88 — Virtual environments** — Is a `requirements.txt`, `Pipfile`, or `pyproject.toml` used to pin dependencies? Is the project developed in a virtual environment?

---

## Quick Review Workflow

1. **Pythonic idiom pass** — Check f-strings, unpacking, enumerate, zip, comprehensions (Items 1-10, 27-36)
2. **Function design** — Argument count, keyword-only args, return None vs. exceptions, functools.wraps (Items 19-26)
3. **Class structure** — Composition vs. inheritance, super(), @property vs. plain attributes (Items 37-51)
4. **Concurrency safety** — Thread-only for I/O, Lock, Queue, no blocking in async (Items 52-64)
5. **Error handling** — try/except/else/finally, exception chaining, reraise (Items 65-67)
6. **Test quality** — TestCase structure, mocks, one concept per test, testable design (Items 78-82)
7. **Documentation** — Docstrings, package root exceptions, dependency management (Items 84-88)

## Severity Levels

| Severity | Description | Examples |
|----------|-------------|---------|
| **Critical** | Correctness bugs or unsafe patterns | Threads for CPU parallelism (Item 53), blocking I/O in async (Item 61), mutable default arguments (Item 24), missing Lock on shared state (Item 54) |
| **High** | Maintainability violations that will cause pain | Returning None for errors (Item 20), missing super().__init__() (Item 40), no functools.wraps (Item 26), missing docstrings on public APIs (Item 84) |
| **Medium** | Un-Pythonic patterns that should be corrected | map/filter instead of comprehensions (Item 27), range(len()) instead of enumerate (Item 7), getter/setter instead of @property (Item 44) |
| **Low** | Polish and idiomatic improvements | Missing f-string (Item 4), index access instead of unpacking (Item 6), missing zip for parallel iteration (Item 8) |
