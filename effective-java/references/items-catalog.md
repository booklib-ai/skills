# Effective Java Items Catalog

Complete reference for all 90 items from Joshua Bloch's *Effective Java* (3rd Edition),
organized by chapter. Use this catalog when generating or reviewing Java code to identify
which items apply.

---

## Chapter 2: Creating and Destroying Objects

### Item 1: Consider static factory methods instead of constructors

Static factory methods have advantages over constructors: they have names, don't require
creating a new object on each invocation, can return subtypes, and the returned type can
vary based on input parameters.

**Naming conventions**: `from`, `of`, `valueOf`, `instance`/`getInstance`, `create`/`newInstance`, `getType`, `newType`, `type`

**Anti-pattern**:
```java
// Direct constructor — no name, always creates new instance
BigInteger prime = new BigInteger("7");
```

**Correct**:
```java
// Named, can cache, can return subtype
BigInteger prime = BigInteger.valueOf(7);
List<String> empty = List.of();
Optional<String> opt = Optional.empty();
```

---

### Item 2: Consider a builder when faced with many constructor parameters

The Builder pattern simulates named optional parameters. Use it when constructors would
need 4+ parameters, especially if many are optional or of the same type.

**Anti-pattern** (telescoping constructors):
```java
NutritionFacts nf = new NutritionFacts(240, 8, 100, 0, 35, 27);
```

**Correct** (Builder):
```java
NutritionFacts nf = new NutritionFacts.Builder(240, 8)
    .calories(100)
    .sodium(35)
    .carbohydrate(27)
    .build();
```

**Key points**: Builder can enforce invariants in `build()`. Builder works well with class hierarchies using recursive type parameters (covariant return typing).

---

### Item 3: Enforce the singleton property with a private constructor or an enum type

For singletons, prefer a single-element enum which provides serialization for free and
guarantees against multiple instantiation even in the face of reflection attacks.

**Preferred**:
```java
public enum Elvis {
    INSTANCE;
    public void leaveTheBuilding() { ... }
}
```

**Alternative** (when you need to extend a superclass):
```java
public class Elvis {
    private static final Elvis INSTANCE = new Elvis();
    private Elvis() { }
    public static Elvis getInstance() { return INSTANCE; }
}
```

---

### Item 4: Enforce noninstantiability with a private constructor

Utility classes (collections of static methods) should not be instantiable.

```java
public class UtilityClass {
    private UtilityClass() {
        throw new AssertionError(); // Prevents internal instantiation
    }
}
```

---

### Item 5: Prefer dependency injection to hardwiring resources

Don't use a singleton or static utility class to implement a class that depends on
underlying resources. Pass the resource (or a factory) into the constructor.

**Anti-pattern**:
```java
public class SpellChecker {
    private static final Lexicon dictionary = new EnglishLexicon(); // Hardwired
}
```

**Correct**:
```java
public class SpellChecker {
    private final Lexicon dictionary;
    public SpellChecker(Lexicon dictionary) {
        this.dictionary = Objects.requireNonNull(dictionary);
    }
}
```

---

### Item 6: Avoid creating unnecessary objects

Reuse immutable objects. Prefer primitives to boxed primitives. Watch out for unintentional autoboxing in loops.

**Anti-pattern**:
```java
Long sum = 0L;
for (long i = 0; i <= Integer.MAX_VALUE; i++) {
    sum += i; // Creates ~2^31 unnecessary Long instances
}
```

**Correct**:
```java
long sum = 0L; // primitive
for (long i = 0; i <= Integer.MAX_VALUE; i++) {
    sum += i;
}
```

Also: prefer `String s = "literal"` over `new String("literal")`. Cache expensive objects like `Pattern`.

---

### Item 7: Eliminate obsolete object references

Null out references when they become obsolete, especially in classes that manage their own
memory (stacks, caches, pools). Use `WeakHashMap` for caches, `LinkedHashMap.removeEldestEntry` for bounded caches.

**Key situations**: stack pop (null out popped element), cache entries, listener/callback registrations.

---

### Item 8: Avoid finalizers and cleaners

Finalizers are unpredictable, dangerous, and generally unnecessary. Cleaners (Java 9) are
less dangerous but still unpredictable. Use `try-with-resources` and `AutoCloseable` instead.

**Exception**: Safety net for native resources, and `Cleaner` as backup only.

---

### Item 9: Prefer try-with-resources to try-finally

Always use try-with-resources for any object that implements `AutoCloseable`.

**Anti-pattern**:
```java
InputStream in = new FileInputStream(src);
try {
    // use in
} finally {
    in.close(); // Can mask original exception
}
```

**Correct**:
```java
try (InputStream in = new FileInputStream(src);
     OutputStream out = new FileOutputStream(dst)) {
    // use in and out
}
```

---

## Chapter 3: Methods Common to All Objects

### Item 10: Obey the general contract when overriding equals

The `equals` contract: reflexive, symmetric, transitive, consistent, non-null.
Don't override `equals` unless you need logical equality. Use `instanceof` (not `getClass`) for type checking when the class is not designed for subclassing.

**Key recipe**: Check `this == obj`, check `instanceof`, cast, compare significant fields.

---

### Item 11: Always override hashCode when you override equals

If two objects are equal according to `equals`, they must have the same `hashCode`.
Use `Objects.hash(field1, field2, ...)` for simple cases; compute manually for performance-critical code.

---

### Item 12: Always override toString

Provide a useful `toString` for debugging. Include all interesting information.
Document the format (or state that it's unspecified).

---

### Item 13: Override clone judiciously

Prefer copy constructors or copy factory methods to `Cloneable`. The `Cloneable` interface
is deeply flawed — it modifies `Object.clone()` behavior via an extralinguistic mechanism.

**Prefer**:
```java
public Yum(Yum yum) { ... } // Copy constructor
public static Yum newInstance(Yum yum) { ... } // Copy factory
```

---

### Item 14: Consider implementing Comparable

Implement `Comparable` for value classes with natural ordering. Use `Comparator.comparing`
with chained `thenComparing` for clean, type-safe comparisons.

```java
private static final Comparator<PhoneNumber> COMPARATOR =
    Comparator.comparingInt((PhoneNumber pn) -> pn.areaCode)
              .thenComparingInt(pn -> pn.prefix)
              .thenComparingInt(pn -> pn.lineNum);
```

**Never** use difference-based comparators (e.g., `return o1.x - o2.x`) — they can overflow.

---

## Chapter 4: Classes and Interfaces

### Item 15: Minimize the accessibility of classes and members

Make each class or member as inaccessible as possible. Top-level classes: package-private or public.
Members: private → package-private → protected → public (use the most restrictive that works).
Instance fields should never be public. Public static final fields are OK only for immutable objects.

---

### Item 16: In public classes, use accessor methods, not public fields

Don't expose fields directly — use getters (and setters only if mutable).
Exception: package-private or private nested classes can expose fields.

---

### Item 17: Minimize mutability

Immutable classes are simpler, thread-safe, and can be shared freely. Rules:
1. Don't provide mutators
2. Ensure class can't be extended (make it final or use static factories with private constructor)
3. Make all fields final
4. Make all fields private
5. Ensure exclusive access to mutable components (defensive copies)

---

### Item 18: Favor composition over inheritance

Inheritance across package boundaries is fragile. Use the decorator pattern:
a forwarding class that wraps the existing class and delegates all method calls.

**Anti-pattern**: `class InstrumentedHashSet<E> extends HashSet<E>` — breaks if `HashSet.addAll` calls `add`.

**Correct**: `class InstrumentedSet<E> extends ForwardingSet<E>` wrapping any `Set<E>`.

---

### Item 19: Design and document for inheritance or else prohibit it

Classes designed for subclassing must document self-use of overridable methods.
If you don't design for inheritance, make the class final or make constructors private with static factories.

---

### Item 20: Prefer interfaces to abstract classes

Interfaces enable mixins, non-hierarchical type frameworks, and default methods.
Use skeletal implementation classes (e.g., `AbstractList`) as optional companions.

---

### Item 21: Design interfaces for posterity

Default methods can break existing implementations. Think carefully before adding
default methods to existing interfaces — they may violate invariants of existing implementations.

---

### Item 22: Use interfaces only to define types

Don't use constant interfaces (interfaces with only `static final` fields).
Use enum types or utility classes for constants instead.

---

### Item 23: Prefer class hierarchies to tagged classes

Tagged classes (a class with a `type` field and switch statements) are verbose, error-prone,
and inefficient. Refactor into a class hierarchy with an abstract root class.

---

### Item 24: Favor static member classes over nonstatic

Four kinds of nested classes: static member, nonstatic member, anonymous, local.
If a member class doesn't need a reference to the enclosing instance, make it static.
Non-static member classes retain a hidden reference to the enclosing instance (memory leak risk).

---

### Item 25: Limit source files to a single top-level class

Never put multiple top-level classes in a single source file. Use static member classes
if the classes are closely related.

---

## Chapter 5: Generics

### Item 26: Don't use raw types

Raw types lose type safety. Use `List<Object>` if you want a list that can hold any object,
`List<?>` if you want a list of some unknown type.

**Anti-pattern**: `List list = new ArrayList();`
**Correct**: `List<String> list = new ArrayList<>();`

---

### Item 27: Eliminate unchecked warnings

Every unchecked warning represents a potential `ClassCastException` at runtime.
Eliminate every warning you can. If you can prove the code is typesafe but can't
eliminate the warning, suppress it with `@SuppressWarnings("unchecked")` on the
smallest possible scope, and add a comment explaining why it's safe.

---

### Item 28: Prefer lists to arrays

Arrays are covariant and reified; generics are invariant and erased. These differences
make arrays and generics poor mixmates. Prefer `List<E>` to `E[]`.

---

### Item 29: Favor generic types

Generify your classes. It's not much harder than using raw types and provides compile-time safety.

---

### Item 30: Favor generic methods

Generic methods are especially useful for static utility methods.
Use type inference: `Set<String> union = union(s1, s2);`

**Recursive type bounds** for mutual comparability:
```java
public static <E extends Comparable<E>> E max(Collection<E> c)
```

---

### Item 31: Use bounded wildcards to increase API flexibility

PECS: Producer-Extends, Consumer-Super.
- If a parameter is a **producer** of `T`, use `<? extends T>`
- If a parameter is a **consumer** of `T`, use `<? super T>`
- Do not use wildcards on return types

```java
public void pushAll(Iterable<? extends E> src) { ... }    // src produces E
public void popAll(Collection<? super E> dst) { ... }      // dst consumes E
```

---

### Item 32: Combine generics and varargs judiciously

Heap pollution can occur with generic varargs parameters. Use `@SafeVarargs`
on every method with a varargs parameter of a generic or parameterized type,
provided the method is truly safe (doesn't store into the varargs array or
expose it to untrusted code).

---

### Item 33: Consider typesafe heterogeneous containers

Use `Class<T>` as a key to store and retrieve values of different types safely.
Pattern: `Map<Class<?>, Object>` with runtime type checking on put/get.

```java
public <T> void putFavorite(Class<T> type, T instance);
public <T> T getFavorite(Class<T> type);
```

---

## Chapter 6: Enums and Annotations

### Item 34: Use enums instead of int constants

Enums provide compile-time type safety, namespaces, and can have behavior.
Use constant-specific method implementations for behavior that varies by constant.
Use the strategy enum pattern for shared behaviors.

---

### Item 35: Use instance fields instead of ordinals

Never derive a value from `ordinal()`. Store the value in an instance field.

**Anti-pattern**: `public int numberOfMusicians() { return ordinal() + 1; }`
**Correct**: Store the count as a constructor parameter.

---

### Item 36: Use EnumSet instead of bit fields

`EnumSet` provides the performance of bit fields with the readability and type safety of enums.

```java
text.applyStyles(EnumSet.of(Style.BOLD, Style.ITALIC));
```

---

### Item 37: Use EnumMap instead of ordinal indexing

Use `EnumMap` instead of `array[enum.ordinal()]` for enum-keyed maps. Also applicable
for multi-dimensional mappings: use nested `EnumMap<..., EnumMap<..., V>>`.

---

### Item 38: Emulate extensible enums with interfaces

Enums can't extend other enums, but they can implement interfaces.
Use this for extensible operation codes (opcode pattern).

---

### Item 39: Prefer annotations to naming patterns

Annotations (like `@Test`) are superior to naming conventions (like `testXxx`).
Use meta-annotations to create custom annotations.

---

### Item 40: Consistently use the Override annotation

Use `@Override` on every method declaration intended to override a superclass or
interface method. The compiler will catch errors if the method doesn't actually override.

---

### Item 41: Use marker interfaces to define types

Marker interfaces (like `Serializable`) define a type that instances of marked classes
have. Use them when you need compile-time type checking. Use marker annotations when
you don't need the type.

---

## Chapter 7: Lambdas and Streams

### Item 42: Prefer lambdas to anonymous classes

Lambdas are more concise than anonymous classes for functional interface implementations.
Keep lambdas short (1-3 lines). If a lambda is long, extract it to a method.
Lambdas lack names and documentation — if a computation isn't self-explanatory, don't use one.

---

### Item 43: Prefer method references to lambdas

Method references are more concise and clearer when they don't need parameter renaming.

| Method Ref Type | Example | Lambda Equivalent |
|----------------|---------|-------------------|
| Static | `Integer::parseInt` | `str -> Integer.parseInt(str)` |
| Bound | `Instant.now()::isAfter` | `t -> Instant.now().isAfter(t)` |
| Unbound | `String::toLowerCase` | `str -> str.toLowerCase()` |
| Constructor | `TreeMap<K,V>::new` | `() -> new TreeMap<K,V>()` |

---

### Item 44: Favor the use of standard functional interfaces

Use the 43 interfaces in `java.util.function` before creating your own.
Six basic ones: `UnaryOperator<T>`, `BinaryOperator<T>`, `Predicate<T>`,
`Function<T,R>`, `Supplier<T>`, `Consumer<T>`.

---

### Item 45: Use streams judiciously

Don't overuse streams. Overusing streams makes code hard to read and maintain.
Good for: transforming sequences, filtering, combining, accumulating into collections,
searching. Bad for: accessing corresponding elements from multiple stages simultaneously,
modifying local variables from enclosing scope.

---

### Item 46: Prefer side-effect-free functions in streams

The most important part of the streams paradigm is to structure your computation as
a sequence of transformations where each stage's result is as close as possible to a
pure function. The `forEach` operation should only be used to report the result of a
stream computation, not to perform computation.

**Key collectors**: `toList()`, `toSet()`, `toMap()`, `groupingBy()`, `joining()`.

---

### Item 47: Prefer Collection to Stream as a return type

`Collection` is a subtype of both `Iterable` and `Stream`, making it the best return
type for public APIs. If the values aren't stored in memory, consider returning a custom
collection backed by computation.

---

### Item 48: Use caution when making streams parallel

Parallelizing a stream is easy to do but can cause incorrect results or poor performance.
Performance gains are best with `ArrayList`, `HashMap`, `HashSet`, `ConcurrentHashMap`,
arrays, `int` ranges, and `long` ranges — data structures that can be cheaply split.
Avoid parallelizing pipelines backed by `Stream.iterate` or `limit`.

---

## Chapter 8: Methods

### Item 49: Check parameters for validity

Validate parameters at the start of methods. Use `Objects.requireNonNull` for null checks.
Use `assert` for non-public methods. Document restrictions with `@throws` Javadoc.

---

### Item 50: Make defensive copies when needed

When receiving mutable objects from clients, make defensive copies in the constructor
(before validation). When returning mutable internal state, return copies.

**Critical**: Copy first, validate the copy — prevents TOCTOU attacks.

```java
public Period(Date start, Date end) {
    this.start = new Date(start.getTime()); // Defensive copy
    this.end = new Date(end.getTime());
    if (this.start.compareTo(this.end) > 0) // Validate copy
        throw new IllegalArgumentException();
}
```

---

### Item 51: Design method signatures carefully

- Choose method names carefully (consistent, understandable)
- Don't go overboard with convenience methods
- Avoid long parameter lists (max 4) — use helper classes, Builder, or break into multiple methods
- Prefer interfaces over classes for parameter types
- Prefer two-element enum types to boolean parameters

---

### Item 52: Use overloading judiciously

Overloading selection is static (compile-time), not dynamic (runtime). Avoid overloading
methods with the same number of parameters. Use different method names instead.

**Dangerous**: `List.remove(int)` vs `List.remove(Object)` — autoboxing creates confusion.

---

### Item 53: Use varargs judiciously

Require at least one argument pattern:
```java
static int min(int firstArg, int... remainingArgs) { ... }
```

Performance concern: varargs allocates an array. For performance-critical methods,
provide overloads for 0-3 args plus varargs fallback.

---

### Item 54: Return empty collections or arrays, not nulls

Never return null from a collection-returning method. Use `Collections.emptyList()`,
`Collections.emptySet()`, `Collections.emptyMap()`, or empty arrays.

---

### Item 55: Return optionals judiciously

Use `Optional<T>` for methods that might not return a result. Never return `null`
from an Optional-returning method. Never use Optional for collection return types
(return empty collection instead). Don't use Optional in fields, parameters, or map keys/values.

---

### Item 56: Write doc comments for all exposed API elements

Document every exported class, interface, method, constructor, and field.
The doc comment should describe the contract: what the method does (not how),
preconditions, postconditions, side effects, and thread safety.

Use `@param`, `@return`, `@throws`, `{@code}`, `{@literal}`, `{@index}`, `@implSpec`.

---

## Chapter 9: General Programming

### Item 57: Minimize the scope of local variables

Declare variables where they are first used. Prefer for-loop to while-loop when
the loop variable isn't needed afterward. Keep methods small and focused.

---

### Item 58: Prefer for-each loops to traditional for loops

Use enhanced for-each wherever possible. Three situations where you can't:
destructive filtering, transforming, and parallel iteration.

---

### Item 59: Know and use the libraries

Don't reinvent the wheel. Use `java.util`, `java.util.concurrent`, `java.util.stream`,
`java.time`, etc. Example: `ThreadLocalRandom.current().nextInt(bound)` instead of
hand-rolled random number generation.

---

### Item 60: Avoid float and double if exact answers are required

Use `BigDecimal`, `int`, or `long` for monetary calculations. `float` and `double`
are designed for scientific computation, not exact decimal values.

---

### Item 61: Prefer primitive types to boxed primitives

Prefer `int` over `Integer`, `long` over `Long`. Unintentional autoboxing causes
performance issues. Applying `==` to boxed primitives is almost always wrong.

---

### Item 62: Avoid strings where other types are more appropriate

Don't use strings as substitutes for enums, aggregates, or capabilities.
Use proper types: enums for enumerated values, classes for aggregates, keys for capabilities.

---

### Item 63: Beware the performance of string concatenation

Use `StringBuilder` when concatenating many strings in a loop.
The `+` operator is fine for a fixed number of strings.

---

### Item 64: Refer to objects by their interfaces

If appropriate interface types exist, parameters, return values, variables, and fields
should all be declared as interface types.

```java
Set<Son> sonSet = new LinkedHashSet<>(); // Good
LinkedHashSet<Son> sonSet = new LinkedHashSet<>(); // Bad
```

---

### Item 65: Prefer interfaces to reflection

Reflection is powerful but has many disadvantages: no compile-time checking, verbose code,
poor performance. Use reflection only to instantiate classes, then access via interfaces.

---

### Item 66: Use native methods judiciously

Rarely need JNI for performance anymore. Use only for accessing platform-specific
facilities not available in Java.

---

### Item 67: Optimize judiciously

Don't optimize prematurely. Write good programs first, then profile. Avoid architectural
decisions that limit performance (like making a public API return mutable internal state
requiring defensive copies on every call).

---

### Item 68: Adhere to generally accepted naming conventions

Follow Java naming conventions:
- Packages: `com.google.common.collect`
- Classes/Interfaces: `BigDecimal`, `Comparator`
- Methods: `ensureCapacity`, `getCrc`
- Constants: `MIN_VALUE`, `NEGATIVE_INFINITY`
- Type parameters: `T`, `E`, `K`, `V`, `X`, `R`, `T1`, `T2`

---

## Chapter 10: Exceptions

### Item 69: Use exceptions only for exceptional conditions

Never use exceptions for ordinary control flow. A well-designed API must not force
its clients to use exceptions for ordinary control flow (provide state-testing methods
or Optional-returning methods).

---

### Item 70: Use checked exceptions for recoverable conditions and runtime exceptions for programming errors

Checked exceptions: caller can reasonably recover.
Runtime exceptions: programming errors (precondition violations).
Errors: reserved for JVM. Don't subclass `Error`.

---

### Item 71: Avoid unnecessary use of checked exceptions

If the caller can't recover, use unchecked. If there's only one checked exception on
a method and it's the sole reason for the `throws` clause, consider returning `Optional`
instead or splitting the method.

---

### Item 72: Favor the use of standard exceptions

Common reusable exceptions:
- `IllegalArgumentException` — non-null parameter value is inappropriate
- `IllegalStateException` — object state is inappropriate for invocation
- `NullPointerException` — parameter is null where prohibited
- `IndexOutOfBoundsException` — index parameter out of range
- `UnsupportedOperationException` — object doesn't support method
- `ConcurrentModificationException` — concurrent modification detected
- `ArithmeticException` — arithmetic error

---

### Item 73: Throw exceptions appropriate to the abstraction

Higher layers should catch lower-level exceptions and throw exceptions appropriate to
their abstraction (exception translation). Use exception chaining to preserve the cause.

```java
try {
    // Lower-level abstraction
} catch (LowerLevelException e) {
    throw new HigherLevelException(e); // Exception chaining
}
```

---

### Item 74: Document all exceptions thrown by each method

Document every exception with `@throws` Javadoc. Declare checked exceptions individually.
Don't declare that a method `throws Exception` or `throws Throwable`.

---

### Item 75: Include failure-capture information in detail messages

Exception detail messages should include the values of all parameters and fields that
contributed to the exception. Don't include passwords or encryption keys.

---

### Item 76: Strive for failure atomicity

A failed method invocation should leave the object in the state it was in prior to
the invocation. Approaches: immutable objects, parameter validation before operation,
temporary copy, recovery code.

---

### Item 77: Don't ignore exceptions

An empty catch block defeats the purpose of exceptions. If you choose to ignore,
document why and name the variable `ignored`.

```java
try { ... }
catch (SomeException ignored) {
    // Safe to ignore because [reason]
}
```

---

## Chapter 11: Concurrency

### Item 78: Synchronize access to shared mutable data

Synchronization is required for reliable communication between threads, not just mutual
exclusion. Use `volatile` for simple communication (e.g., stop flags). Use `synchronized`
or `java.util.concurrent.atomic` for compound actions.

---

### Item 79: Avoid excessive synchronization

Don't call alien methods from within synchronized regions (risk of deadlock or data corruption).
Do as little work as possible inside synchronized regions. Prefer `CopyOnWriteArrayList`
for observable lists with rare modifications.

---

### Item 80: Prefer executors, tasks, and streams to threads

Use `ExecutorService` instead of managing threads directly. Use `Executors.newCachedThreadPool`
for lightly loaded servers, `Executors.newFixedThreadPool` for heavily loaded servers.
Use `ForkJoinPool` for compute-intensive parallel tasks.

---

### Item 81: Prefer concurrency utilities to wait and notify

Use `ConcurrentHashMap`, `BlockingQueue`, `CountDownLatch`, `Semaphore`, and `Phaser`
instead of `wait`/`notify`. Use `ConcurrentHashMap.computeIfAbsent` for thread-safe lazy init.
Always use the wait loop idiom if you must use `wait`:

```java
synchronized (obj) {
    while (!condition) obj.wait();
}
```

---

### Item 82: Document thread safety

Document the thread safety level of every class:
- **Immutable** — Instances are constant (`String`, `Long`, `BigInteger`)
- **Unconditionally thread-safe** — Mutable but with internal synchronization (`AtomicLong`, `ConcurrentHashMap`)
- **Conditionally thread-safe** — Some methods require external synchronization (`Collections.synchronized` wrappers)
- **Not thread-safe** — Must surround each method invocation with external sync (`ArrayList`, `HashMap`)
- **Thread-hostile** — Unsafe even with external sync (rare)

Use `@ThreadSafe`, `@NotThreadSafe`, `@Immutable` annotations (JSR 305).

---

### Item 83: Use lazy initialization judiciously

Most fields should be initialized normally (eagerly). Use lazy init only if needed
for performance or to break circular dependencies.

- **For instance fields**: double-check idiom
- **For static fields**: lazy initialization holder class idiom
- **For fields that can tolerate repeated init**: single-check idiom

```java
// Lazy initialization holder class idiom for static fields
private static class FieldHolder {
    static final FieldType field = computeFieldValue();
}
private static FieldType getField() { return FieldHolder.field; }
```

---

### Item 84: Don't depend on the thread scheduler

Programs that rely on thread scheduling for correctness or performance are non-portable.
Don't use `Thread.yield`. Don't use thread priorities. If threads aren't doing useful work,
restructure the application so they don't run.

---

## Chapter 12: Serialization

### Item 85: Prefer alternatives to Java serialization

Java serialization is dangerous — it enables remote code execution attacks via gadget chains.
Prefer cross-platform structured-data representations: JSON or protobuf.
Never deserialize untrusted data. If you must use serialization, use object deserialization
filtering (`java.io.ObjectInputFilter`).

---

### Item 86: Implement Serializable with great caution

Implementing `Serializable` decreases the flexibility to change a class's implementation,
increases the likelihood of bugs and security holes, and increases the testing burden.
Classes designed for inheritance should rarely implement `Serializable`.

---

### Item 87: Consider using a custom serialized form

Don't accept the default serialized form without considering whether it's appropriate.
The default form is reasonable only if the physical representation is identical to the
logical content. Otherwise, write `writeObject`/`readObject` methods.

Mark fields that are derivable from other state as `transient`.

---

### Item 88: Write readObject methods defensively

`readObject` is effectively a public constructor — it must validate parameters and make
defensive copies of mutable components, just like any other constructor.

---

### Item 89: For instance control, prefer enum types to readResolve

If a singleton class implements `Serializable`, add a `readResolve` method or,
better yet, use a single-element enum. With `readResolve`, all instance fields
with object reference types must be declared `transient`.

---

### Item 90: Consider serialization proxies instead of serialized instances

The serialization proxy pattern: write a private static nested class that represents
the logical state, implement `writeReplace` and `readResolve`. This is the most robust
approach when you must implement `Serializable`.

```java
private static class SerializationProxy implements Serializable {
    private final Date start;
    private final Date end;
    SerializationProxy(Period p) {
        this.start = p.start;
        this.end = p.end;
    }
    private Object readResolve() {
        return new Period(start, end); // Uses public constructor
    }
}
```
