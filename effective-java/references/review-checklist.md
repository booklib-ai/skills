# Effective Java Code Review Checklist

Use this checklist when reviewing Java code. Work through each section and flag any
violations. Not every section applies to every review — skip sections that aren't
relevant to the code under review.

---

## 1. Object Creation

- [ ] Static factory methods used where beneficial (named construction, caching, return subtypes)
- [ ] Builder pattern used for classes with many optional parameters
- [ ] Singleton enforcement is correct (enum type or private constructor with static field)
- [ ] Utility classes have private constructor to prevent instantiation
- [ ] Dependencies are injected, not hardwired to concrete implementations
- [ ] No unnecessary object creation (cached patterns, primitive vs boxed in loops)
- [ ] Obsolete object references are nulled out (custom collections, caches, listeners)
- [ ] try-with-resources used for all AutoCloseable objects
- [ ] No finalizers or cleaners (except as safety nets for native resources)

**Red flags**: Telescoping constructors with 4+ parameters. `new String("literal")`.
`Long sum = 0L` in a loop. Resources closed in finally blocks instead of
try-with-resources. Finalizer or cleaner used for non-native resource cleanup.

---

## 2. Methods Common to All Objects

- [ ] `equals` override obeys the contract (reflexive, symmetric, transitive, consistent)
- [ ] `hashCode` is overridden whenever `equals` is overridden
- [ ] `toString` provides useful diagnostic information
- [ ] `clone` is avoided in favor of copy constructors or copy factories
- [ ] `Comparable` is implemented where natural ordering exists
- [ ] Comparators don't use subtraction (overflow risk)

**Red flags**: `equals` that breaks symmetry (subclass vs superclass). Missing `hashCode`
override causing HashMap failures. `Cloneable` implemented on new classes. Comparator
using `return o1.val - o2.val` (integer overflow).

---

## 3. Class Design

- [ ] Classes and members have minimal accessibility (private > package-private > protected > public)
- [ ] Instance fields are never public (use accessors)
- [ ] Classes are immutable where possible (final fields, no setters, final class or private constructor)
- [ ] Composition is used instead of inheritance across package boundaries
- [ ] Classes designed for inheritance document self-use of overridable methods
- [ ] Classes not designed for inheritance are final or have private constructors
- [ ] Interfaces are used to define types, not for constants
- [ ] Tagged classes are refactored into class hierarchies
- [ ] Inner classes are static unless they need an enclosing instance reference
- [ ] One top-level class per source file

**Red flags**: Public mutable fields. Concrete class extended across package boundary
without documentation of overridable method self-use. Non-static inner class in a
long-lived object (hidden reference causes memory leak). Constant interface
(`interface Constants { int FOO = 1; }`).

---

## 4. Generics

- [ ] No raw types anywhere in the codebase
- [ ] All unchecked warnings are eliminated or suppressed with justification
- [ ] Lists preferred over arrays for generic collections
- [ ] Types and methods are generic where appropriate
- [ ] Bounded wildcards used per PECS (Producer-Extends, Consumer-Super)
- [ ] `@SafeVarargs` used correctly on generic varargs methods
- [ ] No wildcards on return types

**Red flags**: `List` instead of `List<String>`. `@SuppressWarnings("unchecked")` on a
large scope without comment. `E[]` used where `List<E>` would be safer. Missing
wildcards on API parameters that accept subtypes.

---

## 5. Enums and Annotations

- [ ] Enums used instead of `int` or `String` constants
- [ ] Enum values don't derive from `ordinal()` — instance fields used instead
- [ ] `EnumSet` used instead of bit fields
- [ ] `EnumMap` used instead of ordinal-indexed arrays
- [ ] `@Override` annotation present on all overriding methods
- [ ] Annotations used instead of naming patterns

**Red flags**: `public static final int SEASON_WINTER = 0`. Calling `ordinal()` to
derive a value. `int` flags combined with bitwise OR instead of `EnumSet`. Array
indexed by `enum.ordinal()`.

---

## 6. Lambdas and Streams

- [ ] Lambdas used instead of anonymous classes for functional interfaces
- [ ] Method references used where clearer than lambdas
- [ ] Standard functional interfaces from `java.util.function` used before custom ones
- [ ] Streams used judiciously (not forced where loops are clearer)
- [ ] Stream operations are side-effect-free (no mutation in `forEach` used for computation)
- [ ] `Collection` returned from APIs instead of `Stream`
- [ ] Parallel streams used only with appropriate data structures and verified speedup

**Red flags**: Long, complex lambdas (should be extracted to methods). `forEach` used
for computation instead of collect/reduce. `Stream.parallel()` on `LinkedList` or
`Stream.iterate`. Stream pipeline with side effects on shared mutable state.

---

## 7. Method Design

- [ ] Parameters validated at method entry (`Objects.requireNonNull`, bounds checks)
- [ ] Defensive copies made of mutable input parameters (copy before validation)
- [ ] Method signatures have ≤4 parameters (or use helper classes / Builder)
- [ ] No confusing overloads (same number of parameters with different behavior)
- [ ] Varargs methods require at least one argument where needed
- [ ] Empty collections/arrays returned instead of null
- [ ] `Optional` used appropriately for absent return values (not for fields/parameters/collections)
- [ ] All exported API elements have doc comments

**Red flags**: Missing null check that leads to NPE deep in call stack. Mutable
`Date`/`Calendar` parameter stored directly without copy. Method returning `null`
instead of `Collections.emptyList()`. `Optional.get()` without presence check.
Overloaded methods with same arity causing dispatch surprises.

---

## 8. General Programming

- [ ] Local variables declared at point of first use with minimal scope
- [ ] For-each loops used wherever applicable
- [ ] Standard library methods used instead of hand-rolled equivalents
- [ ] `BigDecimal` or `int`/`long` used for monetary calculations (not `float`/`double`)
- [ ] Primitive types preferred over boxed primitives
- [ ] Strings not used as substitutes for other types (enums, aggregates, capabilities)
- [ ] `StringBuilder` used for string concatenation in loops
- [ ] Objects referred to by interface types where appropriate
- [ ] Reflection avoided except for class instantiation via interfaces
- [ ] Naming conventions followed (camelCase methods, UPPER_SNAKE constants, etc.)

**Red flags**: `double` used for currency. `String` concatenation with `+` inside a loop
building large output. `==` applied to boxed primitives. Hand-rolled sorting or data
structure instead of using `java.util` classes. Variable declared far from use with
wide scope.

---

## 9. Exceptions

- [ ] Exceptions used only for exceptional conditions (not control flow)
- [ ] Checked exceptions for recoverable conditions, runtime for programming errors
- [ ] Unnecessary checked exceptions eliminated (consider Optional or method splitting)
- [ ] Standard exceptions reused (`IllegalArgumentException`, `NullPointerException`, etc.)
- [ ] Exceptions translated at abstraction boundaries (with chaining)
- [ ] All exceptions documented with `@throws`
- [ ] Exception detail messages include failure-capture information
- [ ] Methods are failure-atomic (object state unchanged on failure)
- [ ] No empty catch blocks (if intentionally ignored, document why and use `ignored` variable name)

**Red flags**: `try { ... } catch (Exception e) { }` (swallowed exception). Exception
used for flow control (`try { array[i++] } catch (AIOOBE)`). Method declares
`throws Exception`. Low-level `SQLException` propagated through business logic instead
of translated.

---

## 10. Concurrency

- [ ] Shared mutable data is properly synchronized or volatile
- [ ] Minimal work done inside synchronized regions
- [ ] No alien method calls within synchronized blocks
- [ ] `ExecutorService` used instead of raw `Thread` management
- [ ] `java.util.concurrent` utilities preferred over `wait`/`notify`
- [ ] Thread safety level documented on every class
- [ ] Lazy initialization used only when necessary, with correct idiom
- [ ] No dependence on thread scheduler behavior (`Thread.yield`, priorities)

**Red flags**: Non-volatile field used as stop flag across threads. Long computation
inside synchronized block. `wait()` without loop. `new Thread(runnable).start()` instead
of executor. Missing thread safety documentation. Single-check idiom used where
double-check is required.

---

## 11. Serialization

- [ ] Java serialization avoided (JSON, protobuf, or other formats preferred)
- [ ] If Serializable: considered impact on flexibility and security
- [ ] If Serializable: custom serialized form used where default is inappropriate
- [ ] If Serializable: `readObject` validates defensively like a constructor
- [ ] If Serializable: enum types preferred for instance-controlled classes
- [ ] If Serializable: serialization proxy pattern considered
- [ ] No deserialization of untrusted data

**Red flags**: `ObjectInputStream.readObject()` on untrusted input. Default serialized
form exposing internal representation. `readObject` that doesn't validate or make
defensive copies. Non-enum singleton implementing `Serializable` without `readResolve`
or serialization proxy.

---

## Severity Classification

When reporting issues, classify them:

- **Critical**: Bug, security vulnerability, or data corruption risk
  (e.g., missing synchronization on shared mutable data, deserializing untrusted data,
  broken equals/hashCode contract, empty catch block hiding failures)
- **Major**: Significant design debt or maintenance burden
  (e.g., concrete class inheritance, raw types, mutable class that should be immutable,
  telescoping constructors, checked exceptions that should be unchecked)
- **Minor**: Best practice deviation with limited immediate impact
  (e.g., missing @Override, toString not implemented, unnecessary object creation,
  for-loop instead of for-each)
- **Suggestion**: Improvement that would be nice but isn't urgent
  (e.g., consider Builder for future extensibility, evaluate switching to Optional
  return type, document thread safety level)
