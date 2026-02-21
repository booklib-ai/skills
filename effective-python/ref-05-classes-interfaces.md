# Chapter 5: Classes and Interfaces (Items 37-43)

## Item 37: Compose Classes Instead of Nesting Many Levels of Built-in Types
```python
# BAD — deeply nested built-in types
grades = {}  # dict of dict of list of tuples
grades['Math'] = {}
grades['Math']['test'] = [(95, 0.4), (87, 0.6)]

# GOOD — compose with named classes
from dataclasses import dataclass
from collections import namedtuple

Grade = namedtuple('Grade', ('score', 'weight'))

@dataclass
class Subject:
    grades: list

    def average_grade(self):
        total = sum(g.score * g.weight for g in self.grades)
        total_weight = sum(g.weight for g in self.grades)
        return total / total_weight

@dataclass
class Student:
    subjects: dict  # name -> Subject

class Gradebook:
    def __init__(self):
        self._students = {}
```

- When nesting goes beyond dict of dict, refactor into classes
- Use `namedtuple` for lightweight immutable data containers
- Use `dataclass` for mutable data containers with behavior
- Bottom-up refactoring: start with the innermost type

## Item 38: Accept Functions Instead of Classes for Simple Interfaces
```python
# Python's hooks can accept any callable
names = ['Socrates', 'Archimedes', 'Plato']
names.sort(key=len)  # function as interface

# Use __call__ for stateful callables
class CountMissing:
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = CountMissing()
result = defaultdict(counter, current_data)  # uses __call__
print(counter.added)
```

- Functions are first-class in Python — use them as interfaces
- For stateful behavior, define `__call__` on a class
- Simpler than defining full interface classes

## Item 39: Use @classmethod Polymorphism to Construct Objects Generically
```python
class InputData:
    def read(self):
        raise NotImplementedError

class PathInputData(InputData):
    def __init__(self, path):
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        """Factory that creates instances from config."""
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))
```

- Use `@classmethod` as a polymorphic constructor
- Enables subclasses to provide their own construction logic
- Avoids hardcoding class names in factory functions

## Item 40: Initialize Parent Classes with super()
```python
# BAD — direct call to parent
class Child(Parent):
    def __init__(self):
        Parent.__init__(self)  # breaks with multiple inheritance

# GOOD — always use super()
class Child(Parent):
    def __init__(self):
        super().__init__()
```

- `super()` follows the MRO (Method Resolution Order) correctly
- Essential for multiple inheritance (diamond problem)
- Always call `super().__init__()` in `__init__` methods
- The MRO is deterministic: use `ClassName.__mro__` or `ClassName.mro()` to inspect

## Item 41: Consider Composing Functionality with Mix-in Classes
```python
# Mix-in: a class that provides extra functionality without its own state
class JsonMixin:
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.__dict__)

class DatacenterRack(JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = switch
        self.machines = machines

# Usage
rack = DatacenterRack.from_json(json_data)
json_str = rack.to_json()
```

- Mix-ins provide reusable behavior without instance state
- Classes can use multiple mix-ins via multiple inheritance
- Prefer mix-ins over deep inheritance hierarchies
- Name them with `Mixin` suffix for clarity

## Item 42: Prefer Public Attributes Over Private Ones
```python
# BAD — private attributes (__name mangling)
class MyObject:
    def __init__(self):
        self.__private_field = 10  # name-mangled to _MyObject__private_field

# GOOD — protected with convention
class MyObject:
    def __init__(self):
        self._protected_field = 10  # convention: internal use

# Access is still possible but signals "internal"
obj = MyObject()
obj._protected_field  # works, but callers know it's internal
```

- `__double_underscore` causes name mangling — don't use it
- Use `_single_underscore` for protected/internal attributes
- Python philosophy: "We're all consenting adults"
- Name mangling breaks subclass access and makes debugging harder
- Only use `__` to avoid naming conflicts with subclasses (rare)

## Item 43: Inherit from collections.abc for Custom Container Types
```python
from collections.abc import Sequence

class FrequencyList(list):
    def frequency(self):
        counts = {}
        for item in self:
            counts[item] = counts.get(item, 0) + 1
        return counts

# For custom containers, inherit from collections.abc
class BinaryNode(Sequence):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __getitem__(self, index):
        # Required by Sequence
        ...

    def __len__(self):
        # Required by Sequence
        ...

    # count() and index() provided automatically by Sequence
```

- `collections.abc` provides abstract base classes for containers
- Inheriting ensures you implement required methods
- You get mixin methods for free (e.g., `count`, `index` from `Sequence`)
- Available ABCs: `Sequence`, `MutableSequence`, `Set`, `MutableSet`, `Mapping`, `MutableMapping`, etc.
