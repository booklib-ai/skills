# Kotlin In Action — Code Review Checklist

Systematic checklist for reviewing Kotlin code against the 15 chapters
from *Kotlin In Action* (2nd Edition) by Elizarov, Isakova, Aigner, and Jemerov.

---

## 1. Basics & Functions (Chapters 2–3)

### Functions
- [ ] **Ch 2 — Expression-body functions** — Are simple one-expression functions using `= expr` syntax instead of block bodies with explicit return?
- [ ] **Ch 2 — val vs var** — Is `val` used by default? Is `var` used only when mutation is genuinely needed?
- [ ] **Ch 2 — String templates** — Are string templates used instead of string concatenation? Are complex expressions wrapped in `${}`?
- [ ] **Ch 2 — when expressions** — Are chains of if/else replaced with `when` where appropriate? Is `when` used as an expression to return values?
- [ ] **Ch 2 — Smart casts** — Are smart casts leveraged after `is` checks instead of explicit casts?
- [ ] **Ch 2 — Ranges** — Are `..`, `until`, `downTo`, `step` used instead of manual loop bounds?
- [ ] **Ch 2 — try as expression** — Is `try` used as an expression where appropriate to assign results of error-handling logic?

### Defining and Calling Functions
- [ ] **Ch 3 — Named arguments** — Are boolean parameters named? Are same-typed adjacent parameters named? Are arguments named when skipping defaults?
- [ ] **Ch 3 — Default parameter values** — Are default values used instead of function overloads? Are Java-style telescoping constructors replaced?
- [ ] **Ch 3 — Top-level functions** — Are utility functions defined at top level instead of in Java-style static utility classes?
- [ ] **Ch 3 — Extension functions** — Are extensions used to enrich existing types? Are they preferred over utility classes? Are they used appropriately (not for core class behavior)?
- [ ] **Ch 3 — Infix functions** — Are single-parameter functions marked `infix` when it improves readability in DSL contexts?
- [ ] **Ch 3 — Destructuring** — Are data class results destructured where it improves clarity? Are `_` used for unused components?
- [ ] **Ch 3 — Local functions** — Are repeated validation/helper patterns extracted into local functions instead of duplicated?

---

## 2. Classes, Objects, and Interfaces (Chapter 4)

### Inheritance Model
- [ ] **Ch 4 — Final by default** — Are classes kept final unless explicitly designed for inheritance? Is `open` used intentionally?
- [ ] **Ch 4 — Interface defaults** — Are interface default implementations used for shared behavior across unrelated types?
- [ ] **Ch 4 — Sealed classes** — Are type hierarchies with fixed variants modeled as sealed classes/interfaces? Do `when` expressions benefit from exhaustiveness?
- [ ] **Ch 4 — Abstract classes** — Is `abstract` used only for classes that define a template with some implementations?

### Data and Delegation
- [ ] **Ch 4 — Data classes** — Are data-holding classes using the `data` modifier? Are all properties in the primary constructor `val`? Is `copy()` used instead of mutation?
- [ ] **Ch 4 — Class delegation (by)** — Is the `by` keyword used instead of inheritance for delegating interface implementation? Is composition preferred over inheritance for code reuse?

### Visibility and Objects
- [ ] **Ch 4 — Visibility modifiers** — Is the most restrictive visibility used? Is `internal` used for module-private APIs? Are implementation details `private`?
- [ ] **Ch 4 — Nested vs inner classes** — Are nested classes preferred over `inner` to avoid holding outer references? Is `inner` used only when outer access is needed?
- [ ] **Ch 4 — Companion objects** — Are companion objects used for factory methods instead of constructors? Do they implement interfaces where useful?
- [ ] **Ch 4 — Object declarations** — Are singletons implemented with `object` instead of Java-style patterns? Are they used for stateless services and constants?

---

## 3. Lambdas & Collections (Chapters 5–6)

### Lambda Expressions
- [ ] **Ch 5 — Lambda syntax** — Are lambdas moved outside parentheses when they're the last argument? Is `it` used for single-parameter lambdas? Are multi-line lambdas readable?
- [ ] **Ch 5 — Member references** — Are `::functionName` references used instead of wrapper lambdas (e.g., `list.map(::transform)` vs `list.map { transform(it) }`)?
- [ ] **Ch 5 — SAM conversion** — When calling Java APIs expecting SAM interfaces, are lambdas passed directly? For Kotlin, are `fun interface` used for single-method interfaces?

### Collection Processing
- [ ] **Ch 5 — Functional APIs** — Are `filter`, `map`, `flatMap`, `groupBy`, `associate`, `fold`, `reduce` used instead of manual loops?
- [ ] **Ch 5-6 — Sequence for large collections** — For 2+ chained operations on large collections, is `.asSequence()` used? Are intermediate collections avoided?
- [ ] **Ch 6 — Specialized operations** — Is `any {}` used instead of `filter {}.isNotEmpty()`? Is `firstOrNull {}` used instead of `filter {}.firstOrNull()`? Is `count {}` used instead of `filter {}.size`?

### Scope Functions
- [ ] **Ch 5 — apply for configuration** — Is `apply { }` used for object initialization/configuration blocks?
- [ ] **Ch 5 — let for null-safe transforms** — Is `?.let { }` used for null-safe transformations instead of if-not-null blocks?
- [ ] **Ch 5 — also for side effects** — Is `also { }` used for logging/debugging side effects that shouldn't affect the chain?
- [ ] **Ch 5 — with for grouped calls** — Is `with(obj) { }` used when making multiple calls on the same object?
- [ ] **Ch 5 — Scope function overuse** — Are scope functions NOT nested excessively? Is readability maintained?

---

## 4. Null Safety & Types (Chapters 7–8)

### Null Handling
- [ ] **Ch 7 — Safe calls (?.)** — Are safe calls used for nullable navigation instead of explicit null checks? Are they chained for deep access?
- [ ] **Ch 7 — Elvis (?:)** — Is Elvis used for default values? Is it combined with `return` or `throw` for early exits?
- [ ] **Ch 7 — No !! (not-null assertion)** — Is `!!` absent or justified with a comment? Are safe alternatives (safe call, Elvis, let, lateinit) used instead?
- [ ] **Ch 7 — let for null checks** — Is `?.let { }` used appropriately for null-safe blocks? Is it NOT overused where a simple `if` is clearer?
- [ ] **Ch 7 — lateinit** — Is `lateinit` used for properties initialized after construction (DI, tests)? Is it NOT used where a nullable type or lazy init is more appropriate?
- [ ] **Ch 7 — Platform types** — At Java/Kotlin boundaries, are types explicitly annotated? Do platform types (`Type!`) NOT leak into Kotlin APIs?
- [ ] **Ch 7 — Nullable type design** — Are nullable types used only when absence is a meaningful part of the domain? Are non-null types the default?

### Type System
- [ ] **Ch 8 — Primitive types** — In hot paths, are nullable numeric types avoided to prevent boxing? Are `IntArray`/`LongArray`/`DoubleArray` used instead of `Array<Int>`/`List<Int>`?
- [ ] **Ch 8 — Number conversions** — Are explicit conversion functions used instead of relying on implicit widening? No silent precision loss?
- [ ] **Ch 8 — Unit type** — Is `Unit` used correctly as a return type for functions with side effects? Is it used as a generic type argument where needed?
- [ ] **Ch 8 — Nothing type** — Is `Nothing` used for functions that never return? Are throw expressions and infinite loops typed as Nothing?
- [ ] **Ch 8 — Read-only collections** — Are read-only collection types (List, Set, Map) used by default? Are mutable collections exposed only when mutation is part of the contract?

---

## 5. Conventions & Delegation (Chapter 9)

- [ ] **Ch 9 — Operator overloading** — Do operator overloads match conventional mathematical/collection semantics? Are operators used only when their meaning is unambiguous in the domain?
- [ ] **Ch 9 — Comparison via Comparable** — Is `Comparable<T>` implemented for natural ordering? Is `compareValuesBy` used for multi-field comparison?
- [ ] **Ch 9 — Destructuring** — Are data class results destructured for clarity? Are `componentN` operators defined for non-data classes that benefit from destructuring?
- [ ] **Ch 9 — by lazy** — Is `by lazy` used for expensive initializations that may not be needed? Is the thread safety mode appropriate (SYNCHRONIZED, PUBLICATION, NONE)?
- [ ] **Ch 9 — Delegates.observable** — Are change-notification patterns using `Delegates.observable` or `Delegates.vetoable` instead of manual setter logic?
- [ ] **Ch 9 — Map-backed properties** — For dynamic property storage (e.g., JSON deserialization), are map-delegated properties used?
- [ ] **Ch 9 — Custom delegates** — For repeated property patterns, are custom property delegates created with `ReadOnlyProperty`/`ReadWriteProperty`?

---

## 6. Higher-Order Functions & Inline (Chapter 10)

- [ ] **Ch 10 — Function types** — Are function types used for callbacks, strategies, and customizable behavior instead of single-method interfaces (in Kotlin code)?
- [ ] **Ch 10 — Default function parameters** — Do higher-order functions provide sensible default lambdas where appropriate?
- [ ] **Ch 10 — Inline functions** — Are frequently-called higher-order functions marked `inline`? Is inline NOT used for large function bodies?
- [ ] **Ch 10 — noinline** — Are lambda parameters that are stored (not immediately invoked) marked `noinline`?
- [ ] **Ch 10 — crossinline** — Are lambda parameters passed to other execution contexts marked `crossinline`?
- [ ] **Ch 10 — Non-local returns** — Are non-local returns from inline lambdas used intentionally? Are labeled returns (`return@label`) used when only local return is intended?
- [ ] **Ch 10 — Anonymous functions** — Are anonymous functions used instead of labeled returns when local returns are frequent?

---

## 7. Generics (Chapter 11)

- [ ] **Ch 11 — Type parameter constraints** — Are upper bounds applied to restrict type parameters? Is `<T : Any>` used when non-null is required?
- [ ] **Ch 11 — Reified type parameters** — Are inline functions with `reified T` used when runtime type information is needed instead of `Class<T>` parameters?
- [ ] **Ch 11 — Covariance (out)** — Are type parameters that are only produced marked `out`? Are read-only interfaces covariant?
- [ ] **Ch 11 — Contravariance (in)** — Are type parameters that are only consumed marked `in`?
- [ ] **Ch 11 — Star projection** — Is `*` used for runtime type checks and when the specific type argument doesn't matter?
- [ ] **Ch 11 — Type erasure awareness** — Is code aware that generic type information is erased at runtime? No runtime `is List<String>` checks?

---

## 8. Annotations & Reflection (Chapter 12)

- [ ] **Ch 12 — Annotation targets** — Are annotation site targets (`@get:`, `@field:`, `@file:`) used correctly for Java interop?
- [ ] **Ch 12 — Meta-annotations** — Are custom annotations properly annotated with `@Target` and `@Retention`?
- [ ] **Ch 12 — Reflection usage** — Is reflection used sparingly and only where compile-time alternatives are insufficient? Is the Kotlin reflection API (`KClass`, `KProperty`) used instead of Java reflection?

---

## 9. DSL Construction (Chapter 13)

- [ ] **Ch 13 — Lambdas with receivers** — Are DSL builder functions using receiver lambdas (`T.() -> Unit`) for natural syntax?
- [ ] **Ch 13 — @DslMarker** — Is `@DslMarker` used to prevent outer receiver access from inner DSL blocks?
- [ ] **Ch 13 — invoke convention** — Is the `invoke` operator used appropriately for callable objects in DSL contexts?
- [ ] **Ch 13 — Type-safe builders** — Are hierarchical structures built with type-safe builder patterns? Is the builder pattern correct and not leaking mutable state?

---

## 10. Coroutines (Chapter 14)

### Structure
- [ ] **Ch 14 — Structured concurrency** — Are all coroutines launched within a proper CoroutineScope? Is GlobalScope avoided? Do parent-child relationships hold?
- [ ] **Ch 14 — Coroutine builders** — Is `launch` used for fire-and-forget, `async` for results, `runBlocking` only in main/tests?
- [ ] **Ch 14 — coroutineScope** — Is `coroutineScope { }` used in suspend functions to create structured scopes for parallel decomposition?

### Dispatchers
- [ ] **Ch 14 — Dispatcher selection** — Is `Dispatchers.Default` used for CPU work, `Dispatchers.IO` for blocking I/O, `Dispatchers.Main` for UI? Is `withContext` used to switch?
- [ ] **Ch 14 — No blocking in Default** — Are blocking operations NOT running on `Dispatchers.Default`? Are they wrapped in `withContext(Dispatchers.IO)`?

### Error Handling & Cancellation
- [ ] **Ch 14 — Exception handling** — Are exceptions handled properly? Is `CoroutineExceptionHandler` used at top level? Is `supervisorScope` used when child failures should be independent?
- [ ] **Ch 14 — Cancellation cooperation** — Do long-running coroutines check `isActive` or call `ensureActive()`? Are cancellation exceptions not swallowed?
- [ ] **Ch 14 — Timeouts** — Is `withTimeout` or `withTimeoutOrNull` used for time-limited operations?

### Shared State
- [ ] **Ch 14 — Thread safety** — Is shared mutable state protected? Are `Mutex`, atomic types, or single-thread confinement used? No unprotected shared vars across coroutines?

---

## 11. Flows (Chapter 15)

### Flow Basics
- [ ] **Ch 15 — Flow builders** — Are `flow {}`, `flowOf()`, or `.asFlow()` used appropriately? Is `flow {}` used for suspend-based emission?
- [ ] **Ch 15 — Flow context** — Is `flowOn` used to change upstream context instead of `withContext` inside flow builders?
- [ ] **Ch 15 — Cold vs hot** — Are cold Flows used for on-demand data? Are StateFlow/SharedFlow used for state and events?

### Operators
- [ ] **Ch 15 — Intermediate operators** — Are `map`, `filter`, `transform`, `take`, `drop` used instead of manual collection loops?
- [ ] **Ch 15 — Terminal operators** — Is `collect` used for side effects, `toList`/`toSet` for materialization, `first`/`reduce`/`fold` for aggregation?
- [ ] **Ch 15 — Buffering** — Is `buffer()` used when collector is slower than emitter? Is `conflate()` used when only latest value matters?

### Error Handling & Completion
- [ ] **Ch 15 — catch operator** — Is `catch { }` used for upstream exception handling? Are downstream exceptions handled with try/catch around terminal operators?
- [ ] **Ch 15 — onCompletion** — Is `onCompletion { }` used for cleanup and finalization logic?

### Hot Flows
- [ ] **Ch 15 — StateFlow** — Is `StateFlow` used for observable state with a current value? Is `value` property used for synchronous access?
- [ ] **Ch 15 — SharedFlow** — Is `SharedFlow` used for broadcasting events? Is replay configured appropriately?
- [ ] **Ch 15 — shareIn/stateIn** — Are cold flows converted to hot flows with proper `SharingStarted` strategy (Eagerly, Lazily, WhileSubscribed)?

---

## Quick Review Workflow

1. **Basics pass** — Scan for Java-style code: utility classes, getter/setter methods, missing named args, string concatenation, manual loops
2. **Class design pass** — Check for proper sealed hierarchies, data classes, delegation, visibility, final by default
3. **Null safety pass** — Hunt for `!!`, unchecked platform types, nullable types where non-null works, missing safe calls
4. **Collection pass** — Check for Sequence usage on large pipelines, proper functional APIs, scope function clarity
5. **Concurrency pass** — Verify structured concurrency, proper dispatchers, cancellation cooperation, shared state protection
6. **Flow pass** — Check for correct Flow usage, hot vs cold, buffering, exception handling, context preservation
7. **Prioritize findings** — Rank by severity: concurrency bugs > null safety > class design > idioms > style

## Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Concurrency bugs, null safety violations, resource leaks | Unprotected shared state in coroutines, `!!` on user input, GlobalScope usage in production, missing cancellation cooperation |
| **High** | Incorrect Kotlin usage, missed type safety, structural issues | Platform types leaking, eager collection processing on large data, blocking on Default dispatcher, missing structured concurrency |
| **Medium** | Non-idiomatic code, missed Kotlin features, readability issues | Java-style utility classes, manual loops instead of functional APIs, inheritance instead of delegation, missing named arguments |
| **Low** | Polish, minor optimizations, style improvements | Missing destructuring, sequence opportunity, infix function opportunity, scope function preference |
