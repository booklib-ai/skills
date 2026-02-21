# Effective Python — All 90 Items Quick Reference

Complete reference table for all 90 items from *Effective Python: 90 Specific Ways
to Write Better Python* (2nd Edition) by Brett Slatkin.

---

## Chapter 1 — Pythonic Thinking (Items 1–10)

| Item | Name | Chapter | Summary |
|------|------|---------|---------|
| 1 | Know Which Version of Python You're Using | Pythonic Thinking | Verify the runtime version; write code for Python 3; avoid Python 2 patterns |
| 2 | Follow the PEP 8 Style Guide | Pythonic Thinking | snake_case functions/variables, PascalCase classes, 4-space indent, 79-char lines |
| 3 | Know the Differences Between bytes and str | Pythonic Thinking | Be explicit about encoding boundaries; never mix bytes and str operations |
| 4 | Prefer Interpolated F-Strings Over C-style Format Strings and str.format | Pythonic Thinking | Use f-strings for all string formatting; they're more readable and expressive |
| 5 | Write Helper Functions Instead of Complex Expressions | Pythonic Thinking | When an expression needs a comment, extract it into a descriptively named helper function |
| 6 | Prefer Multiple Assignment Unpacking Over Indexing | Pythonic Thinking | Unpack sequences into named variables instead of accessing by index |
| 7 | Prefer enumerate Over range | Pythonic Thinking | Use `enumerate(seq)` instead of `range(len(seq))` when index and value are both needed |
| 8 | Use zip to Process Iterators in Parallel | Pythonic Thinking | Use `zip()` for parallel iteration; `itertools.zip_longest` when lengths may differ |
| 9 | Avoid else Blocks After for and while Loops | Pythonic Thinking | Loop else blocks are counterintuitive; use a flag variable or restructure instead |
| 10 | Prevent Repetition with Assignment Expressions | Pythonic Thinking | Use `:=` (walrus) to assign and test in one expression; avoid in places that hurt clarity |

---

## Chapter 2 — Lists and Dicts (Items 11–18)

| Item | Name | Chapter | Summary |
|------|------|---------|---------|
| 11 | Know How to Slice Sequences | Lists and Dicts | Omit start/end in slices at boundaries; prefer `a[:5]` over `a[0:5]` |
| 12 | Avoid Striding and Slicing in a Single Expression | Lists and Dicts | Never combine start, stop, and stride in one slice; use two operations for clarity |
| 13 | Prefer Catch-All Unpacking Over Slicing | Lists and Dicts | Use starred expressions `first, *rest = items` to split sequences without slicing |
| 14 | Sort by Complex Criteria Using the key Parameter | Lists and Dicts | Use `key=` function with `sort()` and `sorted()`; never use the removed `cmp=` parameter |
| 15 | Be Cautious When Relying on dict Insertion Ordering | Lists and Dicts | In Python 3.7+ dicts preserve insertion order; don't write code that requires a specific order from arbitrary kwargs |
| 16 | Prefer get Over in and KeyError to Handle Missing Dict Keys | Lists and Dicts | Use `dict.get(key, default)` for simple cases; use `setdefault` for initialization |
| 17 | Prefer defaultdict Over setdefault to Handle Missing Items in Internal State | Lists and Dicts | Use `collections.defaultdict` for dicts where missing keys need automatic initialization |
| 18 | Know How to Construct Key-Dependent Default Values with __missing__ | Lists and Dicts | Subclass `dict` and implement `__missing__` when the default value depends on the key |

---

## Chapter 3 — Functions (Items 19–26)

| Item | Name | Chapter | Summary |
|------|------|---------|---------|
| 19 | Never Unpack More Than Three Variables When Functions Return Multiple Values | Functions | Tuples of 4+ are unreadable; use `namedtuple` or a small class instead |
| 20 | Prefer Raising Exceptions to Returning None | Functions | `None` is silently ignored; exceptions are explicit and force callers to handle failure |
| 21 | Know How Closures Interact with Variable Scope | Functions | Closures can read enclosing scope; use `nonlocal` to write to it; prefer class state for complex cases |
| 22 | Reduce Visual Noise with Variable Positional Arguments | Functions | Use `*args` to accept variable positional arguments; watch out for generator exhaustion |
| 23 | Provide Optional Behavior with Keyword Arguments | Functions | Use keyword arguments for optional parameters; provide sensible defaults |
| 24 | Use None and Docstrings to Specify Dynamic Default Arguments | Functions | Never use mutable or dynamic values as defaults; use `None` and initialize inside the body |
| 25 | Enforce Clarity with Keyword-Only and Positional-Only Arguments | Functions | Use `*` to force keyword-only args; use `/` to enforce positional-only args |
| 26 | Define Function Decorators with functools.wraps | Functions | Always use `@functools.wraps(func)` in decorators to preserve metadata |

---

## Chapter 4 — Comprehensions and Generators (Items 27–36)

| Item | Name | Chapter | Summary |
|------|------|---------|---------|
| 27 | Use Comprehensions Instead of map and filter | Comprehensions & Generators | List/dict/set comprehensions are clearer than `map(lambda...)` and `filter(lambda...)` |
| 28 | Avoid More Than Two Control Subexpressions in Comprehensions | Comprehensions & Generators | At most one loop and one condition in a comprehension; use a regular loop for anything more |
| 29 | Avoid Repeated Work in Comprehensions by Using the Walrus Operator | Comprehensions & Generators | Use `:=` in comprehensions to avoid calling the same function twice in loop and condition |
| 30 | Consider Generators Instead of Returning Lists | Comprehensions & Generators | Use `yield` to produce sequences lazily; avoids building the full list in memory |
| 31 | Be Defensive When Iterating Over Arguments | Comprehensions & Generators | Iterators are exhausted after one pass; containers can be iterated multiple times |
| 32 | Consider Generator Expressions for Large List Comprehensions | Comprehensions & Generators | Use `(x for x in ...)` instead of `[x for x in ...]` for large sequences to avoid memory overhead |
| 33 | Compose Multiple Generators with yield from | Comprehensions & Generators | Use `yield from` to delegate to a sub-generator instead of a manual `for/yield` loop |
| 34 | Avoid Injecting Data into Generators with send | Comprehensions & Generators | `generator.send()` is confusing; prefer passing parameters to generator functions |
| 35 | Avoid Causing State Transitions in Generators with throw | Comprehensions & Generators | `generator.throw()` complicates flow; prefer class-based stateful iteration |
| 36 | Consider itertools for Working with Iterators and Generators | Comprehensions & Generators | Use `itertools.chain`, `islice`, `tee`, `zip_longest`, `product`, `groupby` instead of hand-rolling |

---

## Chapter 5 — Classes and Interfaces (Items 37–43)

| Item | Name | Chapter | Summary |
|------|------|---------|---------|
| 37 | Compose Classes Instead of Nesting Many Levels of Built-in Types | Classes & Interfaces | When data has more than two nesting levels, define helper classes or use dataclass |
| 38 | Accept Functions Instead of Classes for Simple Interfaces | Classes & Interfaces | Pass functions (or callables) rather than defining single-method interfaces |
| 39 | Use @classmethod Polymorphism to Construct Objects Generically | Classes & Interfaces | Use `@classmethod` for alternative constructors; enables polymorphic creation |
| 40 | Initialize Parent Classes with super() | Classes & Interfaces | Always call `super().__init__()` to handle MRO correctly in multiple inheritance |
| 41 | Consider Composing Functionality with Mix-in Classes | Classes & Interfaces | Mix-ins provide reusable behavior via inheritance without state or `__init__` |
| 42 | Prefer Public Attributes Over Private Ones | Classes & Interfaces | Use `self.value` by default; use `_protected` by convention; use `__private` only for subclass collision prevention |
| 43 | Inherit from collections.abc for Custom Container Types | Classes & Interfaces | Inherit from `Sequence`, `Mapping`, `Set` etc. to get correct interface enforcement |

---

## Chapter 6 — Metaclasses and Attributes (Items 44–51)

| Item | Name | Chapter | Summary |
|------|------|---------|---------|
| 44 | Use Plain Attributes Instead of Setter and Getter Methods | Metaclasses & Attributes | Public attributes are Pythonic; getter/setter pairs are Java idiom and should be avoided |
| 45 | Consider @property Instead of Refactoring Attributes | Metaclasses & Attributes | Use `@property` to add behavior to attribute access without changing the caller's interface |
| 46 | Use Descriptive Attributes for Lazy Attributes | Metaclasses & Attributes | Use `@property` for lazy computation; avoid surprising side effects in getters |
| 47 | Use __set_name__ to Annotate Class Attributes | Metaclasses & Attributes | Descriptors with `__set_name__` learn their attribute name automatically at class creation |
| 48 | Know How to Use __getattr__, __getattribute__, and __setattr__ for On-demand Attribute Access | Metaclasses & Attributes | Use `__getattr__` for missing attributes (lazy init); avoid `__getattribute__` unless truly needed |
| 49 | Register Class Existence with __init_subclass__ | Metaclasses & Attributes | Use `__init_subclass__` to validate or register subclasses without a metaclass |
| 50 | Annotate Class Attributes with __set_name__ | Metaclasses & Attributes | Descriptors use `__set_name__` to capture the name they're assigned to, eliminating boilerplate |
| 51 | Prefer Class Decorators Over Metaclasses for Composable Class Extensions | Metaclasses & Attributes | Class decorators are simpler than metaclasses for most class-level transformations |

---

## Chapter 7 — Concurrency and Parallelism (Items 52–64)

| Item | Name | Chapter | Summary |
|------|------|---------|---------|
| 52 | Use subprocess to Manage Child Processes | Concurrency & Parallelism | Manage child processes with `subprocess.run()` or `Popen`; avoid `os.system()` |
| 53 | Use Threads for Blocking I/O, Avoid for Parallelism | Concurrency & Parallelism | GIL prevents thread-based CPU parallelism; threads are for I/O only |
| 54 | Use Lock to Prevent Data Races in Threads | Concurrency & Parallelism | Protect all shared mutable state with `threading.Lock` using `with lock:` |
| 55 | Use Queue to Coordinate Work Between Threads | Concurrency & Parallelism | Use `queue.Queue` for thread-safe producer-consumer coordination |
| 56 | Know How to Recognize When Concurrency Is Necessary | Concurrency & Parallelism | Identify fan-out (spawning work) and fan-in (collecting results) patterns |
| 57 | Avoid Creating New Thread Instances for On-demand Fan-out | Concurrency & Parallelism | Creating threads on demand is costly; use a thread pool instead |
| 58 | Understand How Using Queue for Concurrency Requires Refactoring | Concurrency & Parallelism | Queue-based concurrency requires rethinking data flow across thread boundaries |
| 59 | Consider ThreadPoolExecutor When Threads Are Necessary for Concurrency | Concurrency & Parallelism | Use `concurrent.futures.ThreadPoolExecutor` for managed thread pools with futures |
| 60 | Achieve Highly Concurrent I/O with Coroutines | Concurrency & Parallelism | Use `asyncio` coroutines for large numbers of concurrent I/O operations |
| 61 | Know How to Port Threaded I/O to asyncio | Concurrency & Parallelism | Replace blocking calls with `await`; restructure sync code to async incrementally |
| 62 | Mix Threads and Coroutines to Ease the Transition to asyncio | Concurrency & Parallelism | Use `asyncio.run_in_executor` to call blocking code from async context during migration |
| 63 | Avoid Blocking the asyncio Event Loop to Maximize Responsiveness | Concurrency & Parallelism | Never call blocking I/O, `time.sleep`, or CPU-heavy code directly in `async def` functions |
| 64 | Consider concurrent.futures for True Parallelism | Concurrency & Parallelism | Use `ProcessPoolExecutor` for CPU-bound parallelism that bypasses the GIL |

---

## Chapter 8 — Robustness and Performance (Items 65–79)

| Item | Name | Chapter | Summary |
|------|------|---------|---------|
| 65 | Take Advantage of Each Block in try/except/else/finally | Robustness & Performance | Use `else` for success code and `finally` for cleanup; keep `try` narrow |
| 66 | Consider contextlib and with Statements for Reusable try/finally Behavior | Robustness & Performance | Use `@contextlib.contextmanager` to package setup/teardown as a context manager |
| 67 | Use datetime Instead of time for Local Clocks | Robustness & Performance | Use `datetime` with `pytz` or `zoneinfo` for timezone-aware time; avoid the `time` module |
| 68 | Make pickle Reliable with copyreg | Robustness & Performance | Use `copyreg` to version pickle data and handle class evolution over time |
| 69 | Use decimal When Precision Is Paramount | Robustness & Performance | Use `decimal.Decimal` for monetary or exact decimal arithmetic; never float for money |
| 70 | Profile Before Optimizing | Robustness & Performance | Use `cProfile` to find real bottlenecks before optimizing; intuition is often wrong |
| 71 | Prefer deque for Producer-Consumer Queues | Robustness & Performance | `collections.deque` appends/pops from both ends in O(1); `list.pop(0)` is O(n) |
| 72 | Consider Searching Sorted Lists with bisect | Robustness & Performance | Use `bisect.bisect_left` and `insort` for O(log n) search and insertion in sorted lists |
| 73 | Know How to Use heapq for Priority Queues | Robustness & Performance | Use `heapq.heappush`/`heappop` for O(log n) priority queue; avoid re-sorting a list |
| 74 | Consider memoryview and bytearray for Zero-Copy Interactions with bytes | Robustness & Performance | Use `memoryview` for zero-copy slicing of bytes; use `bytearray` for mutable bytes |
| 75 | Use repr Strings for Debugging Output | Robustness & Performance | Use `repr()` in debug output to get unambiguous string representations |
| 76 | Verify Related Behaviors in TestCase Subclasses | Robustness & Performance | Group related test cases into a single `TestCase` subclass for shared setup |
| 77 | Isolate Tests from Each Other with setUp, tearDown, setUpModule, and tearDownModule | Robustness & Performance | Use `setUp`/`tearDown` for per-test isolation and module-level equivalents for expensive setup |
| 78 | Use Mocks to Test Code with Complex Dependencies | Robustness & Performance | Use `unittest.mock.Mock`/`patch` to isolate tests from filesystem, network, and time |
| 79 | Encapsulate Dependencies to Facilitate Mocking and Testing | Robustness & Performance | Inject dependencies (pass them as args or set as attributes) to make code testable |

---

## Chapter 9 — Testing and Debugging (Items 80–85)

| Item | Name | Chapter | Summary |
|------|------|---------|---------|
| 80 | Consider Interactive Debugging with pdb | Testing & Debugging | Use `breakpoint()` to drop into pdb; step through code interactively |
| 81 | Use tracemalloc to Understand Memory Usage and Leaks | Testing & Debugging | Use `tracemalloc` to capture memory snapshots and trace allocation sources |
| 82 | Consider warnings to Refactor and Migrate Usage | Testing & Debugging | Use `warnings.warn` to communicate deprecations without breaking existing callers |
| 83 | Consider Static Analysis via typing to Obviate Testing | Testing & Debugging | Add type annotations and use `mypy` to catch type errors before runtime |
| 84 | Write Docstrings for Every Function, Class, and Module | Testing & Debugging | Docstrings define the contract; every public symbol should have one |
| 85 | Use Packages to Organize Modules and Provide Stable APIs | Testing & Debugging | Use packages with `__init__.py` to namespace and expose a clean public API |

---

## Chapter 10 — Collaboration (Items 86–90)

| Item | Name | Chapter | Summary |
|------|------|---------|---------|
| 86 | Consider Module-Scoped Code to Configure Deployment Environments | Collaboration | Use module-level code and environment variables to configure behavior per deployment |
| 87 | Define a Root Exception to Insulate Callers from APIs | Collaboration | Define a package-specific root exception so callers can catch all package errors in one clause |
| 88 | Know How to Break Circular Dependencies | Collaboration | Resolve circular imports by restructuring, using `TYPE_CHECKING`, or importing inside functions |
| 89 | Consider warnings to Refactor and Migrate Usage | Collaboration | Use the `warnings` module for deprecation notices; filter warnings in tests |
| 90 | Consider Static Analysis via typing to Obviate Testing | Collaboration | Add type hints (`str`, `int`, `list[str]`, `Optional[T]`) and run `mypy` in CI |

---

## Chapter Coverage Summary

| Chapter | Items | Core Theme |
|---------|-------|-----------|
| 1 — Pythonic Thinking | 1–10 | Follow PEP 8, use f-strings, unpacking, enumerate, zip, walrus |
| 2 — Lists and Dicts | 11–18 | Slicing, sorting with key=, defaultdict, __missing__ |
| 3 — Functions | 19–26 | Exceptions over None, closures, *args, keyword-only args, functools.wraps |
| 4 — Comprehensions & Generators | 27–36 | Comprehensions over map/filter, generators with yield, itertools |
| 5 — Classes & Interfaces | 37–43 | Compose classes, @classmethod, super(), mix-ins, collections.abc |
| 6 — Metaclasses & Attributes | 44–51 | Plain attributes, @property, descriptors, __init_subclass__, class decorators |
| 7 — Concurrency & Parallelism | 52–64 | subprocess, threads for I/O only, Lock, Queue, asyncio coroutines |
| 8 — Robustness & Performance | 65–79 | try/except/else/finally, datetime, Decimal, profiling, deque, heapq |
| 9 — Testing & Debugging | 80–85 | pdb, tracemalloc, type annotations, docstrings, packages |
| 10 — Collaboration | 86–90 | Root exceptions, circular imports, warnings, static analysis |

---

## Highest-Impact Items by Priority

### Critical — Correctness and Safety

| Item | Name | Why Critical |
|------|------|-------------|
| 20 | Raise exceptions instead of returning None | Silent failures cause debugging nightmares |
| 24 | Use None for dynamic defaults | Mutable defaults cause shared-state bugs |
| 40 | Initialize parent classes with super() | Direct parent call breaks multiple inheritance |
| 53 | Threads for I/O only | Threads for CPU give no speedup due to GIL |
| 54 | Use Lock for thread safety | Compound operations are not atomic without a Lock |
| 65 | Use try/except/else/finally correctly | Overly broad try blocks catch unintended exceptions |

### Important — Maintainability

| Item | Name | Why Important |
|------|------|--------------|
| 2 | Follow PEP 8 | Consistent style makes code readable by the whole team |
| 4 | Prefer f-strings | Most readable string formatting; avoids format string bugs |
| 25 | Keyword-only and positional-only arguments | Prevents argument confusion at call sites |
| 26 | functools.wraps on decorators | Missing this breaks introspection and debugging |
| 44 | Plain attributes over getters/setters | Pythonic API that can migrate to @property transparently |
| 84 | Docstrings for all public APIs | Enables tooling, onboarding, and API stability |

### Suggestions — Polish and Optimization

| Item | Name | Why Useful |
|------|------|-----------|
| 7 | enumerate over range | Cleaner index+value iteration |
| 8 | zip for parallel iteration | Removes index arithmetic and prevents IndexError |
| 27 | Comprehensions over map/filter | More readable and Pythonic |
| 30 | Generators instead of lists | Reduces memory for large sequences |
| 70 | Profile before optimizing | Prevents wasted effort on non-bottlenecks |
| 71 | deque for queues | O(1) appends/pops vs O(n) for list.pop(0) |
