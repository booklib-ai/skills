# Chapter 8: Robustness and Performance (Items 65-76)

## Item 65: Take Advantage of Each Block in try/except/else/finally
```python
# Full structure
try:
    # Code that might raise
    result = dangerous_operation()
except SomeError as e:
    # Handle specific error
    log_error(e)
except (TypeError, ValueError):
    # Handle multiple error types
    handle_bad_input()
else:
    # Runs ONLY if no exception was raised
    # Use for code that depends on try succeeding
    process(result)
finally:
    # ALWAYS runs, even if exception was raised
    # Use for cleanup (closing files, releasing locks)
    cleanup()
```

- `else` block: reduces code in `try`, makes it clear what you're protecting
- `finally` block: guaranteed cleanup
- Don't put too much in `try` — only the code that can raise the expected exception

## Item 66: Consider contextlib and with Statements for Reusable try/finally Behavior
```python
from contextlib import contextmanager

@contextmanager
def log_level(level, name):
    logger = logging.getLogger(name)
    old_level = logger.level
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(old_level)

with log_level(logging.DEBUG, 'my-log') as logger:
    logger.debug('Debug message')
    # Level is automatically restored after the block
```

- Use `contextlib.contextmanager` for simple context managers
- Use `with` statements instead of manual try/finally
- The `yield` in a context manager is where the `with` block executes

## Item 67: Use datetime Instead of time for Local Clocks
```python
from datetime import datetime, timezone
import pytz  # or zoneinfo (Python 3.9+)

# BAD — time module is unreliable for timezones
import time
time.localtime()  # platform-dependent behavior

# GOOD — datetime with explicit timezone
now = datetime.now(tz=timezone.utc)

# Convert between timezones
eastern = pytz.timezone('US/Eastern')
local_time = now.astimezone(eastern)

# Python 3.9+ — use zoneinfo
from zoneinfo import ZoneInfo
eastern = ZoneInfo('America/New_York')
local_time = now.astimezone(eastern)
```

- Always store/transmit times in UTC
- Convert to local time only for display
- Use `pytz` or `zoneinfo` for timezone handling
- Never use the `time` module for timezone conversions

## Item 68: Make pickle Reliable with copyreg
```python
import copyreg
import pickle

class GameState:
    def __init__(self, level=0, lives=4, points=0):
        self.level = level
        self.lives = lives
        self.points = points

def pickle_game_state(game_state):
    kwargs = game_state.__dict__
    return unpickle_game_state, (kwargs,)

def unpickle_game_state(kwargs):
    return GameState(**kwargs)

copyreg.pickle(GameState, pickle_game_state)
```

- `copyreg` makes pickle forward-compatible when classes change
- Register custom serialization functions for your classes
- Always provide default values for new attributes

## Item 69: Use decimal When Precision Matters
```python
from decimal import Decimal, ROUND_UP

# BAD — float precision issues
rate = 1.45
seconds = 222
cost = rate * seconds / 60  # 5.364999999999999

# GOOD — Decimal for exact arithmetic
rate = Decimal('1.45')
seconds = Decimal('222')
cost = rate * seconds / Decimal('60')
rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
```

- Use `Decimal` for financial calculations, exact fractions
- Always construct from strings (`Decimal('1.45')`) not floats (`Decimal(1.45)`)
- Use `quantize` for rounding control

## Item 70: Profile Before Optimizing
```python
from cProfile import Profile
from pstats import Stats

profiler = Profile()
profiler.runcall(my_function, arg1, arg2)

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()
```

- Never guess where bottlenecks are — profile first
- Use `cProfile` for C-extension speed profiling
- `cumulative` time shows total time including sub-calls
- `tottime` shows time in the function itself (excluding sub-calls)
- Focus optimization on the top functions by cumulative time

## Item 71: Prefer deque for Producer-Consumer Queues
```python
from collections import deque

# FIFO queue operations
queue = deque()
queue.append('item')      # O(1) add to right
item = queue.popleft()    # O(1) remove from left

# BAD — list as queue
queue = []
queue.append('item')      # O(1)
item = queue.pop(0)       # O(n)! shifts all elements
```

- `list.pop(0)` is O(n); `deque.popleft()` is O(1)
- `deque` also supports `maxlen` for bounded buffers
- Use `deque` for any FIFO pattern

## Item 72: Consider Searching Sorted Sequences with bisect
```python
import bisect

sorted_list = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

# Find insertion point
index = bisect.bisect_left(sorted_list, 12)  # 3
index = bisect.bisect_right(sorted_list, 12) # 4

# Insert while maintaining sort order
bisect.insort(sorted_list, 15)  # inserts 15 in correct position
```

- Binary search is O(log n) vs O(n) for linear search
- Use `bisect_left` for leftmost position, `bisect_right` for rightmost
- `insort` keeps list sorted after insertion
- Requires the sequence to already be sorted

## Item 73: Know How to Use heapq for Priority Queues
```python
import heapq

# Create a min-heap
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)

# Pop smallest
smallest = heapq.heappop(heap)  # 1

# Get n smallest/largest
heapq.nsmallest(3, data)
heapq.nlargest(3, data)

# Priority queue with tuples
heapq.heappush(heap, (priority, item))
```

- heapq provides O(log n) push and pop operations
- Always a min-heap (smallest first)
- For max-heap, negate the values
- Use for priority queues, top-K problems, merge sorted streams

## Item 74: Consider memoryview and bytearray for Zero-Copy Interactions with bytes
```python
# BAD — copying bytes on every slice
data = b'large data...'
chunk = data[10:20]  # creates a new bytes object

# GOOD — zero-copy with memoryview
data = bytearray(b'large data...')
view = memoryview(data)
chunk = view[10:20]  # no copy, just a view
chunk[:5] = b'hello'  # writes directly to original data
```

- `memoryview` provides zero-copy slicing of bytes-like objects
- Essential for high-performance I/O and data processing
- Works with `bytearray`, `array.array`, NumPy arrays
- Use for socket I/O, file I/O, binary protocol parsing

## Item 75: Use repr Strings for Debugging Output
```python
class MyClass:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value!r})'

    def __str__(self):
        return f'MyClass with value {self.value}'
```

- `repr()` gives an unambiguous string for debugging
- `str()` gives a human-readable string
- Always implement `__repr__` on your classes
- Use `!r` in f-strings for repr formatting: `f'{obj!r}'`

## Item 76: Verify Related Behaviors in TestCase Subclasses
(Cross-reference with Chapter 9 Testing)
- Group related tests in TestCase subclasses
- Use descriptive test method names
- Test both success and failure cases
