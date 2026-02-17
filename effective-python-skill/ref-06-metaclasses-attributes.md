# Chapter 6: Metaclasses and Attributes (Items 44-51)

## Item 44: Use Plain Attributes Instead of Setter and Getter Methods
```python
# BAD — Java-style getters/setters
class OldResistor:
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms

# GOOD — plain attributes
class Resistor:
    def __init__(self, ohms):
        self.ohms = ohms

# If you later need behavior, migrate to @property (Item 44)
```

- Start with simple public attributes
- If you need special behavior later, use `@property` without changing the API
- Never write explicit getter/setter methods in Python

## Item 45: Consider @property Instead of Refactoring Attributes
```python
class Bucket:
    def __init__(self, period):
        self.period = period
        self.quota = 0

    @property
    def quota(self):
        return self._quota

    @quota.setter
    def quota(self, value):
        if value < 0:
            raise ValueError('Quota must be >= 0')
        self._quota = value
```

- Use `@property` to add validation, logging, or computed behavior
- Keeps backward-compatible API (attribute access syntax)
- Don't do too much work in property getters — keep them fast
- If a property is getting complex, refactor to a normal method

## Item 46: Use Descriptors for Reusable @property Methods
```python
class Grade:
    """Reusable validation descriptor."""
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value

class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

exam = Exam()
exam.math_grade = 95  # calls Grade.__set__
print(exam.math_grade)  # calls Grade.__get__
```

- Use descriptors when you'd copy-paste `@property` logic
- Store per-instance data using `WeakKeyDictionary` to avoid memory leaks:
```python
from weakref import WeakKeyDictionary
class Grade:
    def __init__(self):
        self._values = WeakKeyDictionary()
```

## Item 47: Use __getattr__, __getattribute__, and __setattr__ for Lazy Attributes
```python
# __getattr__ — called only when attribute not found normally
class LazyRecord:
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = f'Value for {name}'
        setattr(self, name, value)  # cache it
        return value

# __getattribute__ — called for EVERY attribute access
class ValidatingRecord:
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        # validate or log every access
        return value

# __setattr__ — called for EVERY attribute assignment
class SavingRecord:
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        # save to database, etc.
```

- `__getattr__` is for lazy/dynamic attributes (called only on missing)
- `__getattribute__` intercepts ALL attribute access (use carefully)
- Always use `super()` in these methods to avoid infinite recursion
- `hasattr` and `getattr` also trigger `__getattribute__`

## Item 48: Validate Subclasses with __init_subclass__
```python
class Polygon:
    sides = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.sides is None or cls.sides < 3:
            raise ValueError('Polygons need 3+ sides')

class Triangle(Polygon):
    sides = 3  # OK

class Line(Polygon):
    sides = 2  # Raises ValueError at class definition time!
```

- `__init_subclass__` is called when a class is subclassed
- Use it for validation, registration, or class setup
- Much simpler than metaclasses for most use cases
- Works with multiple inheritance (use `**kwargs` to pass through)

## Item 49: Register Class Existence with __init_subclass__
```python
registry = {}

class Serializable:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        registry[cls.__name__] = cls

class Point(Serializable):
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Point is automatically registered
assert registry['Point'] is Point
```

- Auto-registration pattern: base class registers all subclasses
- Useful for serialization, plugin systems, ORM models
- Replaces the need for explicit registration decorators or metaclasses

## Item 50: Annotate Class Attributes with __set_name__
```python
class Field:
    def __set_name__(self, owner, name):
        self.name = name          # attribute name on the class
        self.internal_name = '_' + name  # storage name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class Customer:
    first_name = Field()  # __set_name__ called with name='first_name'
    last_name = Field()
```

- `__set_name__` is called automatically when a descriptor is assigned to a class attribute
- Eliminates the need to repeat the attribute name
- Works with descriptors to provide clean, DRY class definitions

## Item 51: Prefer Class Decorators Over Metaclasses for Composable Class Extensions
```python
# Class decorator — simple and composable
def my_class_decorator(cls):
    # modify or wrap cls
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        print(f'Creating {cls.__name__}')
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls

@my_class_decorator
class MyClass:
    def __init__(self, value):
        self.value = value
```

- Class decorators are simpler than metaclasses
- They compose easily (stack multiple decorators)
- Use metaclasses only when you need to control the class creation process itself
- Prefer: `__init_subclass__` > class decorators > metaclasses
