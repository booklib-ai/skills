# Chapter 4: Comprehensions and Generators (Items 27-36)

## Item 27: Use Comprehensions Instead of map and filter
```python
# BAD
squares = map(lambda x: x**2, range(10))
even_squares = map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(10)))

# GOOD
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Also works for dicts and sets
chile_ranks = {rank: name for name, rank in names_and_ranks}
unique_lengths = {len(name) for name in names}
```

## Item 28: Avoid More Than Two Control Subexpressions in Comprehensions
```python
# OK — two levels
flat = [x for row in matrix for x in row]

# OK — two conditions
filtered = [x for x in numbers if x > 0 if x % 2 == 0]

# BAD — too complex, hard to read
result = [x for sublist1 in my_lists
          for sublist2 in sublist1
          for x in sublist2]

# GOOD — use a loop or helper
result = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        result.extend(sublist2)
```

- Rule of thumb: max two `for` subexpressions or two conditions
- Beyond that, use normal loops for readability

## Item 29: Avoid Repeated Work in Comprehensions by Using Assignment Expressions
```python
# BAD — calls get_batches twice
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}

# GOOD — walrus operator avoids repeated computation
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}

# The := expression in the condition makes 'batches' available in the value expression
```

- Use `:=` in the `if` clause to compute once and reuse in the value expression
- The walrus variable leaks into the enclosing scope (be careful with naming)

## Item 30: Consider Generators Instead of Returning Lists
```python
# BAD — builds entire list in memory
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

# GOOD — generator yields one at a time
def index_words(text):
    if text:
        yield 0
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1
```

- Generators use memory proportional to one output, not all outputs
- Use for large or infinite sequences
- Easy to convert: replace `result.append(x)` with `yield x`

## Item 31: Be Defensive When Iterating Over Arguments
```python
# BAD — generator exhausted after first iteration
def normalize(numbers):
    total = sum(numbers)    # exhausts the generator
    result = []
    for value in numbers:   # nothing left to iterate!
        result.append(value / total)
    return result

# GOOD — accept an iterable container, not iterator
def normalize(numbers):
    total = sum(numbers)    # iterates once
    result = []
    for value in numbers:   # iterates again — works with lists, not generators
        result.append(value / total)
    return result

# BETTER — use __iter__ protocol to detect single-use iterators
def normalize(numbers):
    if iter(numbers) is numbers:  # iterator, not container
        raise TypeError('Must supply a container')
    total = sum(numbers)
    return [value / total for value in numbers]
```

- Iterators are exhausted after one pass; containers are not
- Check `iter(x) is x` to detect iterators
- Or implement `__iter__` in a custom container class

## Item 32: Consider Generator Expressions for Large List Comprehensions
```python
# BAD — creates entire list in memory
values = [len(x) for x in open('my_file.txt')]

# GOOD — generator expression, lazy evaluation
values = (len(x) for x in open('my_file.txt'))

# Chain generator expressions
roots = ((x, x**0.5) for x in values)
```

- Generator expressions use `()` instead of `[]`
- Lazy — only compute values as needed
- Can be chained together without memory overhead

## Item 33: Compose Multiple Generators with yield from
```python
# BAD — manual iteration
def chain_generators(gen1, gen2):
    for item in gen1:
        yield item
    for item in gen2:
        yield item

# GOOD — yield from
def chain_generators(gen1, gen2):
    yield from gen1
    yield from gen2

# Real example: tree traversal
def traverse(tree):
    if tree is not None:
        yield from traverse(tree.left)
        yield tree.value
        yield from traverse(tree.right)
```

- `yield from` delegates to a sub-generator
- More readable and slightly faster than manual loop + yield

## Item 34: Avoid Injecting Data into Generators with send
- `generator.send(value)` is complex and hard to understand
- Prefer passing an iterator to the generator instead
- Use `send` only when absolutely necessary (coroutine patterns)

## Item 35: Avoid Causing State Transitions in Generators with throw
- `generator.throw(exception)` is confusing
- Use `__iter__` methods in a class instead for stateful iteration
- If you need exception handling in generators, prefer try/except inside the generator

## Item 36: Consider itertools for Working with Iterators and Generators
**Linking iterators:**
```python
import itertools

# Chain multiple iterators
itertools.chain(iter1, iter2)

# Repeat values
itertools.repeat('hello', 3)

# Cycle through an iterable
itertools.cycle([1, 2, 3])

# Parallel iteration with tee
it1, it2 = itertools.tee(iterator, 2)
```

**Filtering:**
```python
# takewhile — yield while predicate is True
itertools.takewhile(lambda x: x < 5, values)

# dropwhile — skip while predicate is True
itertools.dropwhile(lambda x: x < 5, values)

# filterfalse — yield items where predicate is False
itertools.filterfalse(lambda x: x < 5, values)

# islice — slice an iterator
itertools.islice(values, 2, 8, 2)  # start, stop, step
```

**Combining:**
```python
# product — cartesian product
itertools.product([1,2], ['a','b'])  # (1,'a'), (1,'b'), (2,'a'), (2,'b')

# permutations and combinations
itertools.permutations([1,2,3], 2)
itertools.combinations([1,2,3], 2)
itertools.combinations_with_replacement([1,2,3], 2)

# accumulate — running totals
itertools.accumulate([1,2,3,4])  # 1, 3, 6, 10

# zip_longest
itertools.zip_longest([1,2], [1,2,3], fillvalue=0)
```
