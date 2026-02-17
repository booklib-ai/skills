# Kotlin In Action — Practices Catalog

Comprehensive catalog of practices from *Kotlin In Action* (2nd Edition) by Roman Elizarov,
Svetlana Isakova, Sebastian Aigner, and Dmitry Jemerov, organized by chapter.

---

## Part 1: Introducing Kotlin

### Chapter 1 — Kotlin: What and Why

**1.1 — Statically typed with type inference**
Kotlin is statically typed but uses extensive type inference to reduce boilerplate. Declare types explicitly only when they add clarity (public APIs, complex expressions).

**1.2 — Multi-paradigm: functional + object-oriented**
Kotlin supports both functional and OOP styles. Use functional style (immutable data, pure functions, higher-order functions) for data transformations; OOP for domain modeling and encapsulation.

**1.3 — Interoperable with Java**
Kotlin compiles to JVM bytecode and has seamless Java interop. Call Java from Kotlin and vice versa. Be aware of platform types at boundaries.

**1.4 — Safe by design**
Kotlin's type system eliminates null pointer exceptions at compile time. Non-null types are the default; nullable types require explicit `?` annotation.

**1.5 — Concise and expressive**
Kotlin reduces boilerplate through data classes, type inference, default arguments, extension functions, and string templates. Prefer concise idioms over verbose patterns.

---

### Chapter 2 — Kotlin Basics

**2.1 — Functions with expression bodies**
For simple functions, use expression-body syntax (`= expression`) instead of block bodies with explicit return. This improves readability for one-expression functions.

**2.2 — Variables: val vs var**
Use `val` (immutable) by default. Use `var` (mutable) only when the value truly needs to change. This communicates intent and prevents accidental mutation.

**2.3 — String templates**
Use string templates (`"Hello, $name"` or `"Result: ${expr}"`) instead of string concatenation. They're more readable and efficient.

**2.4 — Classes with properties**
Kotlin classes declare properties directly in the class header or body. The compiler generates getters/setters automatically. Use custom accessors only when needed.

**2.5 — Enum classes with properties and methods**
Enum classes can have properties, methods, and implement interfaces. Use them for fixed sets of constants with associated behavior.

**2.6 — when expression**
Use `when` as a more powerful replacement for switch. It works with any type, supports pattern matching with smart casts, and can be used as an expression returning a value.

**2.7 — Smart casts**
After an `is` check, the compiler automatically casts the variable to the checked type. Combine with `when` for elegant type-based dispatching.

**2.8 — Ranges and progressions**
Use `..` operator, `downTo`, `step`, and `in` for ranges. Ranges work with any Comparable type. Use `until` for half-open ranges.

**2.9 — Exceptions as expressions**
`try` is an expression in Kotlin and returns a value. Kotlin has no checked exceptions. Use exceptions for programming errors, not for expected conditions.

---

### Chapter 3 — Defining and Calling Functions

**3.1 — Named arguments**
Use named arguments for clarity, especially with boolean parameters, multiple parameters of the same type, or when skipping default values. Named arguments serve as self-documentation.

**3.2 — Default parameter values**
Use default parameter values instead of method overloading. This reduces the number of functions while maintaining flexibility.

**3.3 — Top-level functions and properties**
Use top-level functions instead of Java-style utility classes with static methods. Top-level properties are useful for constants (`const val`).

**3.4 — Extension functions**
Add functions to existing classes without modifying them. Extensions are resolved statically (not virtual). Use them to enrich third-party APIs with domain-specific operations.

**3.5 — Extension properties**
Like extension functions but accessed as properties. Use for computed values that feel natural as properties of the extended type.

**3.6 — Varargs and spread operator**
Use `vararg` for functions accepting variable numbers of arguments. Use the spread operator (`*`) to pass arrays to vararg parameters.

**3.7 — Infix functions**
Mark single-parameter member/extension functions with `infix` for natural DSL-like syntax (e.g., `1 to "one"`, `route matches "/api"`).

**3.8 — Destructuring declarations**
Use destructuring to unpack data classes, maps, and other structures into individual variables. Works with `componentN()` operator functions.

**3.9 — Triple-quoted strings**
Use triple-quoted strings (`"""..."""`) for multi-line strings, regex patterns, and strings containing special characters. Use `trimMargin()` or `trimIndent()` for clean formatting.

**3.10 — Local functions**
Define functions inside other functions to encapsulate helper logic and reduce duplication. Local functions have access to the enclosing function's variables.

---

### Chapter 4 — Classes, Objects, and Interfaces

**4.1 — Interfaces with default implementations**
Kotlin interfaces can have default method implementations and properties (without backing fields). Use interfaces with defaults for mix-in behavior.

**4.2 — Final by default (open/abstract)**
Classes and methods are `final` by default. Mark as `open` only when designed for inheritance. Use `abstract` for classes that must be subclassed.

**4.3 — Visibility modifiers**
Kotlin has four visibility levels: `public` (default), `internal` (module), `protected` (subclass), `private` (class/file). Use the most restrictive visibility that works.

**4.4 — Inner vs nested classes**
Nested classes (default) don't hold a reference to the outer class. Use `inner` only when access to the outer instance is needed. Prefer nested to avoid memory leaks.

**4.5 — Sealed classes and interfaces**
Use `sealed` for restricted class hierarchies. The compiler enforces exhaustive `when` expressions. Subclasses must be defined in the same package (same file for sealed classes pre-1.5).

**4.6 — Primary constructors and init blocks**
Use the primary constructor for essential properties. Use `init` blocks for validation logic. Secondary constructors should delegate to the primary.

**4.7 — Data classes**
Use the `data` modifier for classes that primarily hold data. Automatically generates `equals()`, `hashCode()`, `toString()`, `copy()`, and `componentN()` functions. Use `val` properties.

**4.8 — Class delegation with by**
Use the `by` keyword to delegate interface implementation to a composed object. This replaces inheritance-based code reuse with composition.

**4.9 — Object declarations (singletons)**
Use `object` declarations for singletons. They're thread-safe and lazily initialized. Use for stateless utility objects, service locators, or named constants.

**4.10 — Companion objects**
Use `companion object` for factory methods and constants associated with a class. Companion objects can implement interfaces and have extension functions.

**4.11 — Object expressions (anonymous objects)**
Use object expressions to create anonymous implementations of interfaces or abstract classes. Unlike Java anonymous classes, they can access and modify local variables.

---

## Part 2: Embracing Kotlin

### Chapter 5 — Programming with Lambdas

**5.1 — Lambda syntax and conventions**
Lambda expressions use `{ params -> body }` syntax. When a lambda is the last argument, move it outside parentheses. For single-parameter lambdas, use `it`.

**5.2 — Member references**
Use `::functionName` to pass existing functions as lambdas. Works with top-level functions, member functions, constructors, and extension functions. Prefer references when they're clearer than lambdas.

**5.3 — Functional collection APIs**
Use `filter`, `map`, `all`, `any`, `count`, `find`, `groupBy`, `flatMap`, `flatten`, `fold`, `reduce`, `associate`, `zip`, `windowed`, `chunked` instead of manual loops. Chain operations for declarative data processing.

**5.4 — Lazy collection operations with Sequences**
For collections with 2+ chained operations on large data, use `.asSequence()` to avoid creating intermediate collections. Sequences process elements lazily, one at a time.

**5.5 — SAM conversion**
When calling Java methods expecting single-abstract-method interfaces, pass a lambda directly. Kotlin automatically converts the lambda to the SAM interface. For Kotlin interfaces, use `fun interface`.

**5.6 — Lambdas with receivers (with, apply, also)**
- `with(obj) { ... }` — Group multiple calls on the same object; returns lambda result
- `apply { ... }` — Configure an object; returns the receiver
- `also { ... }` — Perform side effects; returns the receiver
- `let { ... }` — Transform a value or null-check; returns lambda result
- `run { ... }` — Scoped computation; returns lambda result
- `buildString { ... }` — Build strings with StringBuilder receiver

---

### Chapter 6 — Working with Collections and Sequences

**6.1 — Extended collection functional APIs**
Beyond basic filter/map, use: `associate` for building maps, `groupBy` for categorization, `partition` for splitting by predicate, `zip` for pairing collections, `windowed` and `chunked` for sliding windows.

**6.2 — Sequence operations in depth**
Sequences have intermediate operations (lazy, return Sequence) and terminal operations (eager, trigger computation). Order matters: put `filter` before `map` to reduce processed elements. Use `generateSequence` for infinite sequences.

---

### Chapter 7 — Working with Nullable Values

**7.1 — Nullable types**
Append `?` to make a type nullable: `String?`. The compiler enforces null safety: you cannot call methods on nullable types without null checks.

**7.2 — Safe call operator (?.) **
Use `?.` to call methods on nullable values. Returns null if the receiver is null. Chain safe calls for deep navigation: `person?.address?.city`.

**7.3 — Elvis operator (?:)**
Use `?:` to provide a default value when an expression is null. Combine with `return` or `throw` for early exits: `val name = input ?: return`.

**7.4 — Safe cast (as?)**
Use `as?` for safe type casts that return null instead of throwing ClassCastException. Combine with Elvis for safe cast with fallback.

**7.5 — Not-null assertion (!!)**
Avoid `!!` whenever possible. It converts null to NPE. Use only when you can prove non-nullness but the compiler cannot. Document why it's safe.

**7.6 — let for null checks**
Use `?.let { ... }` to execute a block only when a value is non-null. The value is available as `it` (non-null) inside the block.

**7.7 — lateinit properties**
Use `lateinit var` for properties that are initialized after construction (e.g., dependency injection, test setup). Accessing before initialization throws. Cannot be used with primitive types.

**7.8 — Extensions on nullable types**
Extension functions can be defined on nullable types (e.g., `String?.isNullOrBlank()`). Inside the extension, `this` can be null. Use for utility functions that should handle null gracefully.

**7.9 — Platform types**
Types from Java without nullability annotations are platform types (`Type!`). They can be treated as nullable or non-null. Always add explicit nullability at Java/Kotlin boundaries to prevent runtime NPEs.

---

### Chapter 8 — Basic Types, Collections, and Arrays

**8.1 — Primitive types**
Kotlin maps basic types (Int, Long, Double, etc.) to Java primitives when possible. Nullable types (Int?) map to boxed types (Integer). Avoid nullable numeric types in performance-critical code.

**8.2 — Number conversions**
Kotlin does not auto-widen numbers. Use explicit conversion functions: `toInt()`, `toLong()`, `toDouble()`, etc. This prevents silent precision loss.

**8.3 — Any, Unit, and Nothing**
- `Any` — Root of the Kotlin type hierarchy (equivalent to Object)
- `Unit` — Equivalent to void but is an actual type with a single value; use as generic type parameter
- `Nothing` — No value; used for functions that never return (throw, infinite loop); is a subtype of every type

**8.4 — Read-only vs mutable collections**
Kotlin distinguishes `Collection` (read-only) from `MutableCollection`. Use read-only collections by default. Expose mutable collections only when mutation is part of the API contract.

**8.5 — Arrays and primitive arrays**
Use `IntArray`, `LongArray`, `DoubleArray`, etc. for primitive arrays (no boxing). Use `Array<T>` for reference type arrays. Use `intArrayOf()`, `arrayOf()` factory functions. Prefer collections over arrays in most cases.

---

### Chapter 9 — Operator Overloading and Other Conventions

**9.1 — Arithmetic operator overloading**
Define `plus`, `minus`, `times`, `div`, `rem` as operator functions. Operator meaning must match the conventional mathematical semantics. Can be defined as member or extension functions.

**9.2 — Compound assignment operators**
`plusAssign`, `minusAssign`, etc. are called for `+=`, `-=`. For mutable collections, these modify in place. For immutable collections, they create new instances.

**9.3 — Unary operators**
`unaryMinus`, `unaryPlus`, `not`, `inc`, `dec` for unary operations. Use for domain types where these operations have clear mathematical meaning.

**9.4 — Comparison operators**
Implement `Comparable<T>` to enable `<`, `>`, `<=`, `>=` comparisons. Use `compareValuesBy` for multi-field comparison. `==` calls `equals`, `===` checks reference identity.

**9.5 — Collection conventions (get, set, in, rangeTo)**
Define `get` operator for index access (`obj[key]`), `set` for mutation (`obj[key] = value`), `contains` for `in` checks, `rangeTo` for `..` operator.

**9.6 — Destructuring declarations**
Data classes automatically generate `component1()` through `componentN()`. Define `componentN` operators on other classes for destructuring. Works in for loops, lambda parameters, and variable declarations.

**9.7 — Delegated properties**
Use `by lazy { }` for lazy initialization (thread-safe by default). Use `Delegates.observable` for change notification. Use `by map` for storing properties in maps. Create custom delegates with `ReadOnlyProperty`/`ReadWriteProperty`.

---

### Chapter 10 — Higher-Order Functions: Lambdas as Parameters and Return Values

**10.1 — Function types**
Kotlin has first-class function types: `(Int, String) -> Boolean`. Use them as parameter types, return types, and variable types. Nullable function types: `((Int) -> Unit)?`.

**10.2 — Calling functions passed as arguments**
Higher-order functions accept function types as parameters. Use them for strategy pattern, callbacks, and customizable algorithms.

**10.3 — Default values for function type parameters**
Provide default implementations for function type parameters. This makes higher-order functions flexible without requiring callers to always pass a lambda.

**10.4 — Returning functions**
Functions can return other functions. Use for factory patterns, partial application, and creating specialized behavior at runtime.

**10.5 — Inline functions**
Mark higher-order functions as `inline` to eliminate lambda allocation overhead. The compiler inlines both the function body and the lambda at call sites. Use for frequently-called utility functions.

**10.6 — noinline and crossinline**
Use `noinline` for lambda parameters that should not be inlined (e.g., stored in a variable). Use `crossinline` for lambdas passed to other contexts where non-local returns are not allowed.

**10.7 — Non-local returns**
In inline functions, `return` inside a lambda returns from the enclosing function (non-local return). Use labeled returns (`return@functionName`) for local returns from lambdas.

**10.8 — Anonymous functions**
Use anonymous functions (`fun(x: Int): Int { ... }`) when you need local returns without labels. Anonymous functions use `return` to return from themselves, not the enclosing function.

---

### Chapter 11 — Generics

**11.1 — Type parameters and constraints**
Use generic type parameters for reusable algorithms. Apply upper bounds with `:` to constrain type parameters: `fun <T : Comparable<T>> sort(list: List<T>)`.

**11.2 — Non-null type parameters**
By default, `<T>` allows nullable types. Use `<T : Any>` to ensure non-null type parameters when null values would be invalid.

**11.3 — Type erasure**
Generic type information is erased at runtime on JVM. You cannot check `is List<String>` at runtime. Use star projection `is List<*>` for runtime type checks.

**11.4 — Reified type parameters**
Use `inline fun <reified T>` to preserve type information at runtime. Enables `is T` checks and `T::class` access. Only works with inline functions.

**11.5 — Covariance (out)**
Use `out` for type parameters that are only produced (returned). A `Producer<out T>` allows `Producer<Cat>` to be used where `Producer<Animal>` is expected. Read-only collections are covariant.

**11.6 — Contravariance (in)**
Use `in` for type parameters that are only consumed (accepted as arguments). A `Consumer<in T>` allows `Consumer<Animal>` to be used where `Consumer<Cat>` is expected.

**11.7 — Declaration-site vs use-site variance**
Declare variance at the class level (declaration-site) when it applies everywhere. Use use-site variance (type projection) when variance applies only at specific usage points.

**11.8 — Star projection (*)**
Use `*` when you don't care about or don't know the type argument. `List<*>` is like `List<out Any?>` — you can read Any? but can't write. Use for runtime type checks.

---

## Part 3: Expanding Kotlin

### Chapter 12 — Annotations and Reflection

**12.1 — Applying annotations**
Annotations are applied with `@AnnotationName`. Can target classes, functions, properties, parameters, and expressions. Use annotation arguments for configuration.

**12.2 — Annotation targets**
Use site targets to specify where an annotation applies: `@get:Rule`, `@field:Inject`, `@file:JvmName`. Important for Java interop and annotation processing.

**12.3 — Meta-annotations**
Annotations on annotations control retention, targets, and repetition. `@Target` specifies allowed elements, `@Retention` controls availability at runtime.

**12.4 — Classes as annotation parameters**
Use `KClass` parameters in annotations to reference types: `@DeserializeInterface(CompanyImpl::class)`. Access with `::class` syntax.

**12.5 — Kotlin Reflection API**
Use `KClass` (via `::class` or `javaClass.kotlin`) for runtime class inspection. `KCallable`, `KFunction`, `KProperty` for accessing members. Use for serialization, dependency injection, and framework construction.

**12.6 — Member access with reflection**
Use `KProperty1<T, R>` for property references, `KFunction` for function references. Access `call()` for invocation, `get()` for property access. Handle visibility with `isAccessible = true`.

---

### Chapter 13 — DSL Construction

**13.1 — From APIs to DSLs**
DSLs provide more readable, domain-specific syntax than plain API calls. Kotlin's lambdas with receivers enable clean DSL construction. Compare chained method calls vs nested DSL blocks.

**13.2 — Lambdas with receivers in DSLs**
The receiver type in `T.() -> Unit` makes `this` refer to the receiver inside the lambda. This enables calling methods on the receiver without explicit qualification, creating a natural DSL syntax.

**13.3 — @DslMarker for scope control**
Use `@DslMarker` meta-annotation to prevent access to outer receivers from inner DSL blocks. This prevents bugs from accidentally calling methods on wrong receiver scopes.

**13.4 — invoke convention in DSLs**
Define `operator fun invoke()` to make objects callable like functions. Useful for DSL entry points and configurable function objects.

**13.5 — Type-safe builders**
Build hierarchical structures (HTML, XML, UI layouts) using nested lambdas with receivers. Each builder function creates a child node and adds it to the parent. Combine with extension functions for clean DSL APIs.

---

## Part 4: Kotlin for Concurrency

### Chapter 14 — Structured Concurrency with Coroutines

**14.1 — Coroutines as lightweight threads**
Coroutines are lightweight, suspendable computations. Thousands can run concurrently without thread overhead. Use `suspend` functions for asynchronous operations.

**14.2 — Coroutine builders**
- `launch { }` — Fire-and-forget coroutine, returns Job
- `async { }` — Coroutine with a result, returns Deferred<T>; use `await()` to get result
- `runBlocking { }` — Bridges regular and coroutine world; blocks the current thread. Use only in main() or tests.

**14.3 — Structured concurrency principles**
Every coroutine must have a scope (CoroutineScope). Child coroutines are tied to their parent's lifecycle. When a parent is cancelled, all children are cancelled. When a child fails, the parent and siblings are cancelled.

**14.4 — CoroutineScope and context**
CoroutineScope defines the lifecycle for coroutines. CoroutineContext holds Job, Dispatcher, and other elements. Use `coroutineScope { }` for scoped concurrent operations within suspend functions.

**14.5 — Dispatchers**
- `Dispatchers.Default` — CPU-intensive work (shared thread pool)
- `Dispatchers.IO` — Blocking I/O operations (expandable thread pool)
- `Dispatchers.Main` — UI thread (Android/Swing)
- `Dispatchers.Unconfined` — Starts in caller thread; resumes in whatever thread. Use with care.
Use `withContext(dispatcher)` to switch dispatchers within a coroutine.

**14.6 — Exception handling**
Uncaught exceptions in `launch` propagate to the parent and cancel siblings. Use `CoroutineExceptionHandler` for top-level error handling. `async` stores exceptions and rethrows on `await()`. Use `supervisorScope` to prevent child failure from cancelling siblings.

**14.7 — Cancellation and timeouts**
Cancellation is cooperative: coroutines must check `isActive` or call suspending functions that check for cancellation. Use `withTimeout(ms)` or `withTimeoutOrNull(ms)` for time-limited operations. Use `ensureActive()` in computation-heavy loops.

**14.8 — Sequential vs concurrent execution**
By default, suspend function calls are sequential. Use `async { }` to run operations concurrently. Use `coroutineScope { }` + `async { }` for structured concurrent decomposition.

**14.9 — Shared mutable state**
Coroutines can share mutable state unsafely. Solutions: use thread-safe data structures (`AtomicInteger`, `ConcurrentHashMap`), confine state to a single thread with `newSingleThreadContext`, use `Mutex` for mutual exclusion, or use actors (channel-based).

---

### Chapter 15 — Flows

**15.1 — Cold streams with Flow**
Flow represents an asynchronous stream of values computed lazily. Unlike sequences, flows support suspension. Flow is cold: the producer code runs only when collected.

**15.2 — Flow builders**
- `flow { emit(value) }` — General-purpose flow builder with suspend block
- `flowOf(1, 2, 3)` — Flow from fixed values
- `.asFlow()` — Convert collections, sequences, or ranges to flows

**15.3 — Flow operators**
Intermediate operators (return Flow, lazy):
- `map { }` — Transform each element
- `filter { }` — Keep elements matching predicate
- `transform { }` — General transformation; can emit multiple values
- `take(n)` — Limit to first n elements
- `drop(n)` — Skip first n elements

**15.4 — Terminal operators**
Terminal operators (trigger collection, suspend):
- `collect { }` — Process each emitted value
- `toList()` / `toSet()` — Collect into a collection
- `first()` / `single()` — Get first/only element
- `reduce { }` / `fold { }` — Accumulate values

**15.5 — Flow context and flowOn**
Flow preserves context: the collector's coroutine context is used by default. Use `flowOn(dispatcher)` to change the upstream execution context. Never use `withContext` inside a flow builder.

**15.6 — Buffering and conflation**
- `buffer()` — Run collector and emitter concurrently with a buffer
- `conflate()` — Drop intermediate values when collector is slow
- `collectLatest { }` — Cancel previous collection when new value arrives

**15.7 — Combining flows**
- `zip(otherFlow) { a, b -> }` — Pair elements from two flows
- `combine(otherFlow) { a, b -> }` — Combine latest values from two flows

**15.8 — Flattening flows**
- `flatMapConcat { }` — Sequentially process inner flows
- `flatMapMerge { }` — Concurrently process inner flows
- `flatMapLatest { }` — Cancel previous inner flow on new emission

**15.9 — Exception handling in flows**
Use `catch { }` operator to handle upstream exceptions declaratively. Use `try/catch` around terminal operators for downstream exceptions. The `catch` operator can emit fallback values.

**15.10 — Flow completion**
Use `onCompletion { cause -> }` to perform actions when flow completes (normally or with exception). Works as a declarative alternative to try/finally.

**15.11 — StateFlow and SharedFlow**
- `StateFlow<T>` — Hot flow holding a single updatable value; always has a current value; replays latest to new collectors. Use for state management.
- `SharedFlow<T>` — Hot flow for broadcasting events to multiple collectors; configurable replay; use for events that shouldn't be missed.
- Convert cold Flow to SharedFlow with `shareIn(scope, started, replay)` or StateFlow with `stateIn(scope, started, initialValue)`.
