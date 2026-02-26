# Effective Kotlin — Practices Catalog

Complete catalog of all 52 items from *Effective Kotlin* (2nd Edition) by Marcin Moskała,
organized by part and chapter.

---

## Part 1: Good Code

### Chapter 1: Safety (Items 1–10)

#### Item 1: Limit Mutability

**Category:** Safety — Mutability Control

**Core Practice:** Prefer read-only properties (val), immutable collections, and data class
copy() over mutable state. Mutable state makes reasoning about code harder, introduces
concurrency risks, and increases the surface for bugs.

**Key Techniques:**
- Use `val` instead of `var` wherever possible
- Use read-only collection interfaces (`List`, `Map`, `Set`) instead of mutable variants
- Use `data class` with `copy()` for state updates instead of mutating fields
- If mutation is needed, limit its scope: prefer local mutable variables over mutable properties
- For shared mutable state, use synchronization or concurrent data structures
- Prefer `Sequence` or `Flow` (which produce new elements) over mutable accumulation

**When to Apply:** Always — this is the default stance. Only introduce mutability when
there's a clear performance or API need.

**Anti-Pattern:** Public `var` properties, returning `MutableList` from functions, using
mutable collections as class properties without encapsulation.

---

#### Item 2: Minimize the Scope of Variables

**Category:** Safety — Scope Control

**Core Practice:** Declare variables in the tightest scope possible and prefer defining
variables close to their first usage. Use `if`, `when`, `let`, and `run` to tighten scope.

**Key Techniques:**
- Declare variables inside the block where they're used, not at the top of a function
- Use destructuring declarations to limit what's visible
- Prefer `let`/`run` scoping functions to restrict a value's visibility
- Use `when` with variable binding: `when (val result = compute()) { ... }`
- For loops, prefer `for` with a narrow iteration variable over external counters
- Prefer `val` with conditional initialization over `var` with later reassignment

**When to Apply:** Always — every variable declaration should be as close to first use and
as narrow in scope as possible.

**Anti-Pattern:** Declaring all variables at the top of a function; using `var` initialized
to a default and reassigned in a branch.

---

#### Item 3: Eliminate Platform Types as Soon as Possible

**Category:** Safety — Null Safety at Boundaries

**Core Practice:** When calling Java code, the return types are "platform types" (noted as
`Type!`) where nullability is unknown. Specify nullability explicitly at the call site to
prevent NPEs from propagating through Kotlin code.

**Key Techniques:**
- Annotate Java code with `@Nullable`/`@NotNull` (JSR-305, JetBrains, AndroidX annotations)
- When consuming Java APIs, declare the expected nullability explicitly: `val name: String? = javaObj.getName()`
- Never let platform types leak into public Kotlin APIs — always resolve them
- Write wrapper functions around Java APIs with explicit nullability

**When to Apply:** At every Java/Kotlin boundary. Critical for Android development and
mixed-language projects.

**Anti-Pattern:** Letting platform types propagate as inferred types throughout Kotlin code;
assuming Java return values are non-null without verification.

---

#### Item 4: Do Not Expose Inferred Types

**Category:** Safety — Type Clarity

**Core Practice:** When a public function or property's type is inferred, changes to the
implementation can inadvertently change the public type. Always specify types explicitly for
public/protected API members.

**Key Techniques:**
- Explicit return types on all public/protected functions and properties
- Explicit types for all public constants and companion object properties
- Allow inference only for local variables and private members where the type is obvious
- Be especially careful with factory functions — the inferred return type may be too specific

**When to Apply:** For all public API surfaces. Local variables and private members can
use inference when the type is obvious from context.

**Anti-Pattern:** `fun createAnimal() = Dog()` — infers `Dog` instead of desired `Animal`.

---

#### Item 5: Specify Your Expectations on Arguments and State

**Category:** Safety — Preconditions and Contracts

**Core Practice:** Use `require()`, `check()`, and `assert()` to document and enforce
expectations at function boundaries. Fail fast with clear messages.

**Key Techniques:**
- `require(condition) { "message" }` — for argument validation; throws `IllegalArgumentException`
- `check(condition) { "message" }` — for state validation; throws `IllegalStateException`
- `assert(condition)` — for assertions checked only in testing (-ea flag)
- `requireNotNull(value) { "message" }` and `checkNotNull(value) { "message" }` — for null checks that smart-cast
- Place preconditions at the top of functions, before any logic
- Use the `contract` mechanism for custom smart-cast functions

**When to Apply:** At public function boundaries, constructors, and any place where
invariants must hold. Use `require` for input validation, `check` for state validation.

**Anti-Pattern:** Proceeding with invalid arguments and failing deep in the call stack
with unclear errors; custom exception types where standard ones suffice.

---

#### Item 6: Prefer Standard Errors to Custom Ones

**Category:** Safety — Error Types

**Core Practice:** Use standard Kotlin/Java exception types (`IllegalArgumentException`,
`IllegalStateException`, `UnsupportedOperationException`, `ConcurrentModificationException`,
`NoSuchElementException`, `IndexOutOfBoundsException`) rather than defining custom exception
hierarchies for common error conditions.

**Key Techniques:**
- `require` throws `IllegalArgumentException` — use for argument validation
- `check` throws `IllegalStateException` — use for state validation
- Custom exceptions only when callers need to catch and handle specific error types differently
- In library code, document which exceptions can be thrown

**When to Apply:** Default to standard exceptions. Create custom exceptions only when
the caller needs to distinguish between different error conditions programmatically.

**Anti-Pattern:** Creating `UserNotFoundException`, `InvalidEmailException`, etc. when
`IllegalArgumentException` with a descriptive message would suffice.

---

#### Item 7: Prefer Null or Failure Result When Lack of Result Is Possible

**Category:** Safety — Expected Failure Handling

**Core Practice:** For functions where failure is expected (not exceptional), return `null`
or a `Result`/sealed class instead of throwing exceptions. Reserve exceptions for truly
exceptional situations.

**Key Techniques:**
- Return `T?` when the "no result" case is simple (e.g., `find` operations)
- Return `Result<T>` or a sealed class when the caller needs to know *why* it failed
- Use sealed class hierarchies: `sealed interface Result<T> { data class Success<T>(val value: T) : Result<T>; data class Failure<T>(val error: Error) : Result<T> }`
- Naming convention: `getOrNull()`, `findOrNull()` for nullable returns
- Functions named `getX()` may throw; functions named `getXOrNull()` return null
- Use `runCatching { }` to convert throwing code to `Result`

**When to Apply:** For operations that can legitimately fail: parsing, lookups, network
calls, user input validation. NOT for programming errors (those should throw).

**Anti-Pattern:** Throwing exceptions for expected failure paths like "user not found" or
"invalid format"; using exceptions for flow control.

---

#### Item 8: Handle Nulls Properly

**Category:** Safety — Null Handling

**Core Practice:** Kotlin's null-safety system is powerful but must be used correctly.
Prefer safe calls, smart casting, Elvis operator, and `let` over force-unwrapping (`!!`).

**Key Techniques:**
- Safe call: `user?.name` — returns null if user is null
- Elvis operator: `user?.name ?: "Unknown"` — provides default for null
- Smart casting: `if (user != null) { user.name }` — compiler tracks non-null
- `let` for null-safe scoping: `user?.let { sendEmail(it) }`
- `lateinit` for properties that can't be initialized in constructor but are set before use
- `Delegates.notNull<T>()` — alternative to lateinit for primitives
- Avoid `!!` except where you can prove the value is non-null and want to fail fast

**When to Apply:** Every time you encounter a nullable type. Default to safe handling.

**Anti-Pattern:** Widespread `!!` usage; nested null checks instead of safe calls;
checking for null then using `!!` in the next line.

---

#### Item 9: Close Resources with use

**Category:** Safety — Resource Management

**Core Practice:** Use the `use` extension function (Kotlin's equivalent of try-with-resources)
for any `Closeable`/`AutoCloseable` resource to ensure proper cleanup.

**Key Techniques:**
- `FileReader(path).use { reader -> reader.readText() }`
- `BufferedReader(reader).use { it.readLine() }` — `it` reference in simple cases
- `File(path).useLines { lines -> lines.filter { ... }.toList() }` — for line-by-line processing
- `use` works with any `Closeable`: streams, connections, database cursors
- Nest `use` calls for multiple resources, or use extension functions to flatten

**When to Apply:** Every time you open a file, database connection, network stream,
or any other closeable resource.

**Anti-Pattern:** Manual try/finally for resource cleanup; forgetting to close resources
in error paths; using `readLines()` for large files instead of `useLines()`.

---

#### Item 10: Write Unit Tests

**Category:** Safety — Testing

**Core Practice:** Unit tests are the primary mechanism for verifying correctness and
preventing regressions. Write tests for all non-trivial business logic.

**Key Techniques:**
- Test public API contracts, not implementation details
- Use descriptive test names that explain the scenario and expected outcome
- Structure tests as Arrange-Act-Assert (Given-When-Then)
- Test edge cases: empty inputs, null values, boundary conditions
- Test error paths: verify correct exceptions or Result.failure
- Use parameterized tests for multiple input/output combinations
- Mock external dependencies, but prefer fakes/stubs over mocking frameworks
- Aim for meaningful coverage of business logic, not just line coverage numbers

**When to Apply:** For all modules with business logic. Less critical for simple
data classes or pass-through wrappers.

**Anti-Pattern:** No tests; tests that test framework behavior instead of business logic;
tests tightly coupled to implementation; testing only the happy path.

---

### Chapter 2: Readability (Items 11–18)

#### Item 11: Design for Readability

**Category:** Readability — General

**Core Practice:** Code is read far more often than it is written. Optimize for the reader,
not the writer. Prefer clear, obvious code over clever, concise code.

**Key Techniques:**
- Prefer explicit over implicit: clear names, explicit types where helpful, named arguments
- Avoid clever tricks: nested scope functions, complex lambda chains, operator abuse
- Keep functions short and focused on a single level of abstraction
- Use intermediate variables with descriptive names to break complex expressions
- Prefer `if`/`when` expressions with clear branches over complex ternary-style logic
- Code should read like well-written prose — a developer should understand it on first read

**When to Apply:** Always. Every code decision should consider "will the next reader
understand this immediately?"

**Anti-Pattern:** Chaining multiple scope functions; using `also` inside `let` inside `apply`;
excessively compact code that requires mental unpacking.

---

#### Item 12: Operator Meaning Should Be Consistent with Its Function Name

**Category:** Readability — Operators

**Core Practice:** Kotlin allows operator overloading, but each operator has a conventional
meaning tied to its function name (`plus`, `times`, `contains`, etc.). Don't overload
operators with meanings that violate these conventions.

**Key Techniques:**
- `plus` should represent addition or combination, not unrelated operations
- `times` should represent multiplication or repetition
- `contains` (the `in` operator) should check membership
- `get`/`set` (index operators) should provide indexed access
- `invoke` should "call" or "execute" the object
- If the operation doesn't naturally match the operator's name, use a named function instead
- It's acceptable to use operators on domain types when the meaning is universally clear (e.g., `Vector + Vector`)

**When to Apply:** Whenever defining operator overloads. Ask: "Does this operation match
what `plus`/`times`/`contains`/etc. conventionally means?"

**Anti-Pattern:** Using `+` to mean "add to database"; using `*` to mean "format string";
using `invoke` for operations that aren't conceptually "calling" the object.

---

#### Item 13: Avoid Returning or Operating on Unit?

**Category:** Readability — Return Types

**Core Practice:** `Unit?` has only two values: `Unit` and `null`, making it essentially
a boolean but far less clear. Avoid functions that return `Unit?` or use `Unit?` in
conditional logic.

**Key Techniques:**
- If a function can succeed or fail, return `Boolean`, `Result`, or a sealed class
- Don't chain `?.let { }` on functions returning `Unit?` for conditional execution
- If you see `Unit?` in your code, refactor to use explicit boolean or sealed type
- Common source: `map {}` on nullable, where the lambda returns Unit

**When to Apply:** Whenever you see `Unit?` appear in types, return values, or conditionals.

**Anti-Pattern:** `val result: Unit? = user?.let { save(it) }; if (result != null) { ... }`

---

#### Item 14: Specify the Variable Type When It Is Not Clear

**Category:** Readability — Type Clarity

**Core Practice:** Kotlin's type inference is powerful, but when the type isn't obvious
from the right-hand side, specify it explicitly for readability.

**Key Techniques:**
- Omit type when obvious: `val name = "Alice"`, `val count = 42`, `val users = listOf<User>()`
- Specify type when not obvious: `val data: UserProfile = api.fetchData()`, `val result: Map<String, List<Int>> = process(input)`
- Always specify types for public API members (functions, properties)
- Be explicit with numeric types when precision matters: `val rate: Double = 0.05`

**When to Apply:** Whenever the reader would need to navigate to the function definition
to understand the type. When in doubt, be explicit.

**Anti-Pattern:** `val data = repository.getData()` — what type is `data`?

---

#### Item 15: Consider Referencing Receivers Explicitly

**Category:** Readability — Scope Clarity

**Core Practice:** In nested scope functions or classes with multiple receivers (this, outer
class, extension receiver), use explicit receiver references (`this@ClassName`,
labeled `this@functionName`) to avoid ambiguity.

**Key Techniques:**
- In nested lambdas with receivers, use labels: `this@outer` vs `this@inner`
- In extension functions called within a class, be explicit about which `this` is used
- Use `@DslMarker` in DSLs to prevent accidental use of outer receivers
- Prefer `also` (uses `it`) over `apply` (uses `this`) when the receiver context would be confusing
- When using `with`/`apply`/`run`, ensure the reader can clearly identify the receiver

**When to Apply:** Whenever there's ambiguity about which receiver is being used, especially
in nested scope functions, DSLs, and classes with extension function members.

**Anti-Pattern:** Nested `apply` blocks where it's unclear which `this` is being referenced;
DSL builders that accidentally access outer scope receivers.

---

#### Item 16: Properties Should Represent State, Not Behavior

**Category:** Readability — Properties vs Functions

**Core Practice:** Properties should represent the state of an object. If an operation is
computationally expensive, has side effects, or conceptually does something rather than
returns something, use a function instead.

**Key Techniques:**
- Property: `val name: String`, `val isValid: Boolean`, `val size: Int`
- Function: `fun calculateTotal(): BigDecimal`, `fun findUser(id: String): User?`
- Properties should be O(1) or at most O(n) with caching expectations
- Properties should not throw exceptions (except for lazy initialization)
- Properties should be idempotent — same result on consecutive calls (no side effects)
- Custom getters are fine for derived state: `val fullName: String get() = "$first $last"`

**When to Apply:** For every decision between `val x: T get() = ...` and `fun x(): T`.

**Anti-Pattern:** `val users: List<User> get() = database.query("SELECT * FROM users")` —
this is behavior masquerading as state.

---

#### Item 17: Consider Naming Arguments

**Category:** Readability — Named Arguments

**Core Practice:** Use named arguments for parameters where the meaning isn't clear from
context, especially for booleans, numbers, strings, and functions with multiple parameters
of the same type.

**Key Techniques:**
- Named booleans: `setVisible(visible = true)` instead of `setVisible(true)`
- Named same-type params: `sendMessage(from = alice, to = bob)` instead of `sendMessage(alice, bob)`
- Named lambda: `repeat(times = 3) { ... }`
- Always name arguments for builder-style or configuration functions
- Optional parameters with defaults benefit greatly from naming: `createUser(name = "Alice", role = Admin, active = true)`
- You don't need to name arguments when meaning is clear from type: `listOf(1, 2, 3)`

**When to Apply:** Whenever the argument's purpose isn't obvious from its type and position.
Especially for boolean parameters, same-typed parameters, and numeric parameters.

**Anti-Pattern:** `createRect(0, 0, 100, 50, true, false)` — what do these mean?

---

#### Item 18: Respect Coding Conventions

**Category:** Readability — Conventions

**Core Practice:** Follow Kotlin's official coding conventions and the project's style guide.
Consistency across a codebase is more important than any individual preference.

**Key Techniques:**
- Follow the Kotlin Coding Conventions (kotlinlang.org/docs/coding-conventions.html)
- Use ktlint or detekt for automated enforcement
- CamelCase for classes, camelCase for functions/properties, SCREAMING_SNAKE_CASE for constants
- Package naming: lowercase, no underscores
- File naming: PascalCase matching the main class, or descriptive lowercase for utility files
- Indentation: 4 spaces (Kotlin convention)
- Blank lines: separate logical sections, between functions, before/after class bodies

**When to Apply:** Always. Adopt a style guide and enforce it with tooling.

**Anti-Pattern:** Inconsistent naming; mixing conventions from other languages (snake_case
for functions, Hungarian notation); tabs-vs-spaces debates without tooling enforcement.

---

## Part 2: Code Design

### Chapter 3: Reusability (Items 19–25)

#### Item 19: Do Not Repeat Knowledge

**Category:** Reusability — DRY Principle

**Core Practice:** Every piece of knowledge should have a single, unambiguous representation
in the system. Duplication leads to inconsistency when one copy is updated but others aren't.

**Key Techniques:**
- Extract common logic into shared functions or classes
- Distinguish between true knowledge duplication (same business rule expressed twice) and
  accidental similarity (two things that happen to look alike but vary independently)
- Single source of truth for: business rules, algorithms, validation logic, URL patterns, key names
- Use constants for magic values, enums for fixed sets, configuration for environment-specific values
- Don't over-DRY: if two similar-looking code sections serve different concerns and change
  for different reasons, they may be better kept separate

**When to Apply:** When the same business rule, algorithm, or decision exists in multiple
places. NOT when two code sections coincidentally look similar but represent different concepts.

**Anti-Pattern:** Same validation logic in UI layer and service layer; hardcoded strings
duplicated across files; copy-pasted algorithm with slight variations.

---

#### Item 20: Do Not Repeat Common Algorithms

**Category:** Reusability — Standard Library Usage

**Core Practice:** Kotlin's standard library provides a rich set of collection operations,
scope functions, and utility functions. Use them instead of writing custom implementations.

**Key Techniques:**
- Collection: `map`, `filter`, `flatMap`, `fold`, `reduce`, `groupBy`, `associate`, `partition`, `zip`, `windowed`, `chunked`
- Searching: `find`, `first`, `firstOrNull`, `any`, `all`, `none`, `count`
- Transformation: `sorted`, `sortedBy`, `distinct`, `distinctBy`, `take`, `drop`, `reversed`
- Aggregation: `sum`, `sumOf`, `average`, `min`, `max`, `minBy`, `maxBy`
- Scope: `let`, `run`, `with`, `apply`, `also`
- String: `buildString`, `joinToString`, `split`, `replace`, `trim`, `padStart`, `padEnd`
- If a common algorithm isn't in stdlib, extract it as an extension function in your project

**When to Apply:** Before writing any collection processing, searching, sorting, or
string manipulation logic, check if a stdlib function already does it.

**Anti-Pattern:** Writing manual loops for filtering, manual StringBuilder usage instead
of `buildString`/`joinToString`, reimplementing `groupBy` or `associate`.

---

#### Item 21: Use Property Delegation to Extract Common Property Patterns

**Category:** Reusability — Delegation

**Core Practice:** Kotlin's property delegation (`by` keyword) lets you extract common
property patterns like lazy initialization, observable changes, and map-backed properties.

**Key Techniques:**
- `by lazy { }` — lazy initialization (thread-safe by default)
- `by Delegates.observable(initial) { prop, old, new -> }` — react to changes
- `by Delegates.vetoable(initial) { prop, old, new -> condition }` — validate changes
- `by map` — delegate to a map for dynamic property lookup
- Custom delegates: implement `ReadOnlyProperty` or `ReadWriteProperty`
- Use custom delegates for cross-cutting concerns: logging, validation, caching, preferences

**When to Apply:** When you see repeated property patterns (lazy init, change notification,
validation on set, caching). Extract the pattern into a delegate.

**Anti-Pattern:** Manual lazy initialization with null checks; manual change listeners with
backing fields; repeated boilerplate property patterns across classes.

---

#### Item 22: Use Generics When Implementing Common Algorithms

**Category:** Reusability — Generics

**Core Practice:** When extracting common algorithms, use generics to make them work
with any type rather than duplicating for specific types.

**Key Techniques:**
- Generic functions: `fun <T> List<T>.lastHalf(): List<T>`
- Generic classes: `class Cache<T>(val loader: () -> T)`
- Bounded generics: `fun <T : Comparable<T>> List<T>.sorted(): List<T>`
- Multiple bounds: `fun <T> doWork(value: T) where T : Serializable, T : Comparable<T>`
- Use generics with extension functions for powerful, reusable utilities
- Star projection (`*`) when you don't care about the type parameter

**When to Apply:** When writing utility functions or classes that operate on "some type"
where the algorithm doesn't depend on the specific type.

**Anti-Pattern:** Separate `processStringList()`, `processIntList()`, `processUserList()`
functions that do the same thing with different types.

---

#### Item 23: Avoid Shadowing Type Parameters

**Category:** Reusability — Generic Safety

**Core Practice:** Don't declare a type parameter on a function that shadows a type parameter
from the enclosing class. This creates confusing independent type parameters that look related.

**Key Techniques:**
- If a class is `class Box<T>`, a member function using `T` should NOT redeclare `<T>`
- Use different names if you need an independent type parameter: `fun <R> map(f: (T) -> R): Box<R>`
- Shadowing leads to subtle bugs where the function's `T` is unrelated to the class's `T`

**When to Apply:** When writing generic member functions in generic classes.

**Anti-Pattern:** `class Box<T> { fun <T> add(item: T) }` — the function's `T` shadows and
is independent from the class's `T`.

---

#### Item 24: Consider Variance for Generic Types

**Category:** Reusability — Variance

**Core Practice:** Use declaration-site variance (`in`/`out` modifiers) to specify whether a
generic type is a producer (covariant, `out`) or consumer (contravariant, `in`), enabling
more flexible subtype relationships.

**Key Techniques:**
- `out T` (covariant): the class only produces T (returns T, never takes T as input). `List<out T>` means `List<Dog>` is a subtype of `List<Animal>`
- `in T` (contravariant): the class only consumes T (takes T as input, never returns T). `Comparable<in T>` means `Comparable<Animal>` is a subtype of `Comparable<Dog>`
- Use-site variance (`out`/`in` at call site) when declaration-site isn't possible
- Star projection (`*`) when you don't care about the type parameter at all
- Kotlin collections use this well: `List<out T>` is covariant, `MutableList<T>` is invariant

**When to Apply:** When designing generic interfaces and classes. Think about whether your
type only produces, only consumes, or does both.

**Anti-Pattern:** Invariant type parameters where covariance would be safe and useful;
requiring exact type matches where subtype relationships should work.

---

#### Item 25: Reuse Between Different Platforms

**Category:** Reusability — Multiplatform

**Core Practice:** Kotlin Multiplatform allows sharing code between JVM, JS, Native, and
other targets. Put platform-independent logic in common modules.

**Key Techniques:**
- `expect`/`actual` mechanism for platform-specific implementations
- Common module for: business logic, data models, validation, algorithms
- Platform modules for: UI, platform APIs, file system, networking specifics
- Share serialization models with kotlinx.serialization
- Share coroutine-based async code with kotlinx.coroutines
- Use `expect`/`actual` sparingly — prefer interfaces with platform-specific DI

**When to Apply:** When building applications that target multiple platforms (mobile,
web, server). Put as much business logic as possible in common code.

**Anti-Pattern:** Duplicating business logic per platform; using platform-specific APIs
in code that could be platform-independent.

---

### Chapter 4: Abstraction Design (Items 26–32)

#### Item 26: Each Function Should Be Written in Terms of a Single Level of Abstraction

**Category:** Abstraction — Function Design

**Core Practice:** A function should operate at one consistent level of abstraction. Don't
mix high-level operations (business logic) with low-level details (string parsing, I/O).

**Key Techniques:**
- Extract low-level details into well-named helper functions
- A high-level function should read like a summary of steps: `validate()`, `process()`, `save()`
- Each helper function should also maintain a single abstraction level
- This creates a natural hierarchy: high-level orchestration → mid-level operations → low-level details
- Functions at the same level of abstraction should have similar levels of detail in their names

**When to Apply:** When a function mixes different levels of detail. The classic sign is
a function that alternates between business-meaningful operations and mechanical details.

**Anti-Pattern:** A function that calls `validateOrder(order)` then directly manipulates
`StringBuilder` for formatting, then calls `repository.save()`.

---

#### Item 27: Use Abstraction to Protect Code Against Changes

**Category:** Abstraction — Change Protection

**Core Practice:** Introduce abstractions (interfaces, abstract classes, function types)
at boundaries where change is expected. Abstractions isolate the impact of changes.

**Key Techniques:**
- Interface for dependencies that might have multiple implementations (repositories, services)
- Function type parameters for varying behavior (`(T) -> R` instead of a specific strategy class)
- Wrapper/adapter classes around external APIs that might change
- Constant extraction: name magic values, extract configuration
- Use abstraction layers at system boundaries: database, network, file system, third-party APIs

**When to Apply:** At boundaries where the other side might change: external APIs,
infrastructure dependencies, business rules that vary by configuration.

**Anti-Pattern:** Directly depending on a specific HTTP library throughout the codebase;
hardcoding database queries in business logic; no abstraction around third-party SDKs.

---

#### Item 28: Specify API Stability

**Category:** Abstraction — API Lifecycle

**Core Practice:** Communicate the stability of your API elements so consumers know what's
safe to depend on. Use annotations and versioning conventions.

**Key Techniques:**
- `@Deprecated("message", replaceWith = ReplaceWith("newFunction()"))` — for removed APIs
- `@OptIn(ExperimentalApi::class)` / `@RequiresOptIn` — for experimental/unstable APIs
- Semantic versioning: major for breaking changes, minor for additions, patch for fixes
- Mark internal implementation details as `internal` or `private`
- Document stability guarantees in KDoc
- Use `@Deprecated` with `DeprecationLevel.WARNING`, then `ERROR`, then `HIDDEN` for gradual removal

**When to Apply:** For any code consumed by other modules or teams. Library authors
must be especially careful about API stability contracts.

**Anti-Pattern:** Breaking public API without deprecation cycle; experimental APIs without
opt-in annotation; no versioning strategy.

---

#### Item 29: Consider Wrapping External APIs

**Category:** Abstraction — Dependency Isolation

**Core Practice:** Wrap third-party libraries and external APIs behind your own interfaces
to isolate your code from their changes, enable testing, and allow swapping implementations.

**Key Techniques:**
- Create a repository/service interface for each external dependency
- Implement the interface using the specific library
- Inject the interface, not the implementation
- This enables: unit testing with fakes, swapping implementations, adapting to API changes
- Don't over-wrap: simple, stable utilities (like Kotlin stdlib) don't need wrapping
- Focus wrapping effort on: HTTP clients, databases, third-party SDKs, analytics, logging

**When to Apply:** For external dependencies that are complex, likely to change, or need
to be mocked in tests.

**Anti-Pattern:** Calling Retrofit/OkHttp/Room directly throughout business logic; untestable
code due to tight coupling with external libraries.

---

#### Item 30: Minimize Elements' Visibility

**Category:** Abstraction — Encapsulation

**Core Practice:** Use the most restrictive visibility modifier that works. Less visibility
means less API surface, fewer invariants to maintain, and more freedom to refactor.

**Key Techniques:**
- Default to `private`; widen only when needed
- Kotlin visibility: `private` (file/class), `protected` (class + subclasses), `internal` (module), `public` (everyone)
- Use `internal` for module-internal APIs that shouldn't be exposed to consumers
- Properties: prefer `private set` with public getter if external mutation isn't needed
- Classes: prefer `private` nested classes or `internal` top-level classes
- In interfaces, keep the surface minimal — don't expose implementation helpers

**When to Apply:** For every class, function, and property declaration. Start `private`
and widen only with justification.

**Anti-Pattern:** Everything `public` by default; `internal` classes with `public` members
that expose implementation; mutable properties without restricted setters.

---

#### Item 31: Define Contract with Documentation

**Category:** Abstraction — Documentation

**Core Practice:** Use KDoc to document the contract of public API elements: what the function
does, what it expects, what it returns, and what exceptions it may throw.

**Key Techniques:**
- `/** */` KDoc for all public classes, functions, and properties
- `@param` for parameter descriptions
- `@return` for return value description
- `@throws` / `@exception` for documented exceptions
- `@sample` for linking to example code
- `@see` for referencing related elements
- Focus documentation on the *what* and *why*, not the *how* (code shows how)
- Document edge cases, nullability semantics, threading guarantees, and lifecycle

**When to Apply:** For all public API elements. Internal elements benefit from documentation
when the behavior isn't obvious from the name and signature.

**Anti-Pattern:** No KDoc on public APIs; documentation that restates the function name
(`/** Gets the user */` on `fun getUser()`); outdated documentation.

---

#### Item 32: Respect Abstraction Contracts

**Category:** Abstraction — Contract Compliance

**Core Practice:** When implementing an interface or extending a class, respect the contract
defined by the supertype. Violating contracts leads to bugs in code that depends on the
documented behavior (Liskov Substitution Principle).

**Key Techniques:**
- Read and follow the documented contracts of interfaces you implement
- Maintain postconditions: if the contract says "returns non-empty list," ensure it
- Maintain invariants: if the contract says "thread-safe," ensure thread safety
- `equals`, `hashCode`, `compareTo`, `toString` all have well-defined contracts — respect them
- When overriding, the subclass behavior should be substitutable for the superclass
- Don't throw unexpected exceptions from overridden methods

**When to Apply:** Whenever implementing interfaces or extending classes, especially
well-known contracts like `Collection`, `Comparable`, `Iterable`.

**Anti-Pattern:** `equals` that isn't symmetric; `Comparable` that isn't consistent with
`equals`; `Iterator` that doesn't throw `NoSuchElementException` when exhausted.

---

### Chapter 5: Object Creation (Items 33–35)

#### Item 33: Consider Factory Functions Instead of Constructors

**Category:** Object Creation — Factory Patterns

**Core Practice:** Factory functions offer naming, caching, return-type flexibility,
and can return subtypes. Use them when constructors are limiting.

**Key Techniques:**
- Companion object factory: `User.create(name)` or `User(name)` (invoke operator)
- Top-level factory: `listOf()`, `mapOf()`, `buildString { }`
- Extension factory: `String.toUser()` — conversion factory as extension
- Fake constructors: companion `invoke` operator for constructor-like syntax with factory benefits
- Factory functions can: have descriptive names, cache instances, return subtypes, hide implementation
- Kotlin stdlib examples: `listOf()`, `mutableListOf()`, `lazy { }`, `coroutineScope { }`

**When to Apply:** When you need: named construction, caching/pooling, subtype returns,
complex initialization logic, or platform factory patterns (Android `Fragment.newInstance()`).

**Anti-Pattern:** Complex logic in constructors; constructors that do I/O or heavy
computation; inability to name construction scenarios; no caching opportunity.

---

#### Item 34: Consider a Primary Constructor with Named Optional Arguments

**Category:** Object Creation — Constructor Design

**Core Practice:** Kotlin's primary constructor with default parameter values and named
arguments often eliminates the need for the Builder pattern, telescoping constructors,
or multiple factory overloads.

**Key Techniques:**
- Primary constructor with defaults: `class User(val name: String, val age: Int = 0, val active: Boolean = true)`
- Callers use named args: `User(name = "Alice", active = false)`
- This gives the builder pattern's readability without the ceremony
- Migration: convert Java builders to Kotlin primary constructors with defaults
- Data classes work perfectly with this pattern: `data class Config(val host: String = "localhost", val port: Int = 8080)`
- Use `copy()` on data classes for partial modifications

**When to Apply:** As the default object creation approach in Kotlin. Prefer over
Builder pattern unless construction involves complex validation or multi-step building.

**Anti-Pattern:** Java-style Builder pattern in Kotlin (rarely needed); telescoping
constructor overloads; multiple factory functions that differ only in defaults.

---

#### Item 35: Consider Defining a DSL for Complex Object Creation

**Category:** Object Creation — DSLs

**Core Practice:** For complex, hierarchical object creation, Kotlin's type-safe builders
(DSLs with lambda receivers) provide the most readable syntax.

**Key Techniques:**
- Lambda with receiver: `fun html(init: HTML.() -> Unit): HTML`
- `@DslMarker` to restrict scope and prevent accidental use of outer receivers
- `inline` builder functions to eliminate lambda overhead
- Builder DSL examples: HTML builders, Gradle build scripts, Ktor routing, kotlinx.html
- Use when: object hierarchies, configuration, structured data, multi-step assembly
- Combine with `apply`: `val config = Config().apply { host = "localhost"; port = 8080 }`

**When to Apply:** When building hierarchical or tree-structured objects (UI layouts,
configuration, document structures, routing tables).

**Anti-Pattern:** Nested constructor calls for hierarchical structures; verbose imperative
code for what is naturally a declarative structure.

---

### Chapter 6: Class Design (Items 36–44)

#### Item 36: Prefer Composition over Inheritance

**Category:** Class Design — Composition vs Inheritance

**Core Practice:** Use composition (HAS-A) with delegation over inheritance (IS-A) when
the goal is code reuse. Inheritance creates tight coupling and fragile hierarchies.

**Key Techniques:**
- Kotlin's `by` delegation: `class CountingSet<T>(val inner: MutableSet<T> = mutableSetOf()) : MutableSet<T> by inner`
- Interface delegation eliminates boilerplate forwarding methods
- Use inheritance only for true IS-A relationships with substitutability
- Prefer interfaces over abstract classes for defining capabilities
- Composition allows: changing implementation at runtime, combining multiple behaviors, easier testing

**When to Apply:** Default to composition. Use inheritance only when there's a genuine
IS-A relationship and the Liskov Substitution Principle is satisfied.

**Anti-Pattern:** Inheriting from a utility class for code reuse; deep inheritance trees;
overriding methods in ways that break superclass assumptions; "inheritance for convenience."

---

#### Item 37: Use the Data Modifier to Represent a Bundle of Data

**Category:** Class Design — Data Classes

**Core Practice:** Use `data class` for classes whose primary purpose is holding data.
They automatically generate `equals`, `hashCode`, `toString`, `copy`, and destructuring.

**Key Techniques:**
- `data class User(val name: String, val email: String)` — auto-generated methods
- `copy()` for creating modified copies: `user.copy(name = "New Name")`
- Destructuring: `val (name, email) = user`
- Properties in the primary constructor participate in equals/hashCode/toString/copy
- Properties declared in the body do NOT participate in generated methods
- Use data classes for: DTOs, value objects, events, messages, records
- Data classes should generally be immutable (all `val` properties)

**When to Apply:** For any class that primarily holds data and needs structural equality,
copying, and sensible toString.

**Anti-Pattern:** Regular classes with manually written equals/hashCode/toString for data
holders; mutable data classes with var properties (breaks hash-based collections).

---

#### Item 38: Use Function Types or Functional Interfaces to Pass Behaviors

**Category:** Class Design — Behavioral Abstraction

**Core Practice:** Instead of interfaces with a single method (SAM interfaces in Java), use
Kotlin function types `(A) -> B` or `fun interface` for passing behavior.

**Key Techniques:**
- Function type parameter: `fun process(filter: (User) -> Boolean)`
- Type alias for clarity: `typealias UserFilter = (User) -> Boolean`
- `fun interface` (SAM) when you want both lambda convenience and named interface: `fun interface Validator { fun validate(input: String): Boolean }`
- Lambda expressions are naturally concise: `process { it.isActive }`
- Method references for existing functions: `process(User::isActive)`
- `fun interface` gives SAM conversion from Java and named type for documentation

**When to Apply:** When a behavior needs to be parameterized. Use function types for
simple cases; `fun interface` when you need a named concept with documentation.

**Anti-Pattern:** Regular interfaces with a single method that require anonymous object
syntax; verbose callback interfaces where a lambda would suffice.

---

#### Item 39: Prefer Class Hierarchies Instead of Tagged Classes

**Category:** Class Design — Sealed Hierarchies

**Core Practice:** Replace "tagged classes" (classes with a type enum and conditional logic)
with sealed class hierarchies. Each variant becomes its own class with type-specific behavior.

**Key Techniques:**
- Sealed class/interface: `sealed interface Shape { data class Circle(val r: Double) : Shape; data class Rect(val w: Double, val h: Double) : Shape }`
- `when` exhaustiveness: compiler ensures all cases are handled
- Each subclass carries only the data it needs (no null fields for other variants)
- Type-specific behavior lives in the subclass, not in switch/when blocks
- Sealed interfaces allow a class to implement multiple sealed hierarchies

**When to Apply:** Whenever you see a class with: a type/kind enum field, when/switch
blocks checking that type, nullable fields that are only relevant for some types.

**Anti-Pattern:** `class Shape(val type: Type, val radius: Double?, val width: Double?, val height: Double?)` with `when (type)` checks everywhere.

---

#### Item 40: Respect the Contract of equals

**Category:** Class Design — Equality

**Core Practice:** `equals` must satisfy: reflexive (a == a), symmetric (a == b ↔ b == a),
transitive (a == b && b == c → a == c), consistent (same result on repeated calls),
and null comparison (a.equals(null) == false).

**Key Techniques:**
- Use `data class` for automatic correct `equals` (based on constructor properties)
- For custom `equals`: override both `equals` and `hashCode` together
- `equals` should compare by value, not identity, for value types
- Be careful with inheritance: a subclass `equals` can easily break symmetry with parent
- Consider using `abstract class` with `equals` defined in terms of an abstract property set
- Use sealed classes to avoid the inheritance-equality problem

**When to Apply:** When defining value types or any class used in collections, maps,
or equality comparisons. `data class` handles most cases automatically.

**Anti-Pattern:** Overriding `equals` without `hashCode`; `equals` that isn't symmetric
between parent and child; mutable properties in `equals` computation.

---

#### Item 41: Respect the Contract of hashCode

**Category:** Class Design — Hashing

**Core Practice:** `hashCode` must be consistent with `equals`: if `a == b`, then
`a.hashCode() == b.hashCode()`. Objects used as hash map keys or set elements MUST
have correct hashCode.

**Key Techniques:**
- `data class` generates correct `hashCode` automatically
- Always override `hashCode` when overriding `equals`
- Use the same properties in `hashCode` that you use in `equals`
- Kotlin's `Objects.hash()` or manual combination: `31 * hash1 + hash2`
- Immutable objects: compute hash once and cache it
- Mutable objects used as keys is dangerous: mutation changes hash, losing the entry

**When to Apply:** Whenever overriding `equals`. Also when placing objects in hash-based
collections (HashMap, HashSet, LinkedHashMap).

**Anti-Pattern:** `equals` override without `hashCode` override; mutable properties in
hashCode; hashCode that returns a constant (legal but destroys performance).

---

#### Item 42: Respect the Contract of compareTo

**Category:** Class Design — Ordering

**Core Practice:** `compareTo` (and `Comparable` interface) must be: antisymmetric
(a > b implies b < a), transitive (a > b && b > c implies a > c), and consistent
(`a.compareTo(b) == 0` should ideally mean `a == b`).

**Key Techniques:**
- Implement `Comparable<T>` for natural ordering: `class User : Comparable<User>`
- Use `compareBy`/`compareByDescending` for clean comparator construction
- `compareValuesBy(this, other, { it.lastName }, { it.firstName })` for multi-field comparison
- Sorted collections, ranges, and sorting functions all rely on correct compareTo
- Ensure consistency with equals when possible (TreeMap depends on this)

**When to Apply:** When objects have a natural ordering. Use `Comparator` for alternative
orderings that don't change the class definition.

**Anti-Pattern:** `compareTo` that returns 0 for unequal objects used in TreeSet (loses entries);
inconsistent ordering that isn't transitive.

---

#### Item 43: Consider Extracting Non-Essential Parts of Your API into Extensions

**Category:** Class Design — Extension Functions

**Core Practice:** Keep classes focused on their core responsibility. Move non-essential
operations (convenience methods, formatting, integration utilities) to extension functions.

**Key Techniques:**
- Core API in the class: essential operations that need access to private state
- Extensions for: convenience overloads, format conversions, integration with other libraries
- Extensions can be imported selectively — unlike members which are always available
- Extensions improve discoverability through IDE completion based on receiver type
- Extension properties for derived state that doesn't need private access:
  `val String.isPalindrome: Boolean get() = this == reversed()`

**When to Apply:** When a method doesn't need private access and represents a secondary
operation. When different consumers need different utility functions on the same type.

**Anti-Pattern:** Bloated classes with dozens of utility methods; convenience methods
that clutter the core API; methods that could work with only the public interface.

---

#### Item 44: Avoid Member Extensions

**Category:** Class Design — Extension Placement

**Core Practice:** Extensions defined as members of another class have confusing dispatch
behavior (static for the extension receiver, virtual for the dispatch receiver). Prefer
top-level extensions or local extensions.

**Key Techniques:**
- Top-level extensions: `fun String.toCamelCase(): String` — clear and predictable
- Local extensions (inside a function): limited scope, good for one-off utilities
- Member extensions have two receivers (`this` and the extension receiver), creating confusion
- Member extensions can't be used outside the class they're defined in
- Only valid use: DSL markers where restricting scope is intentional

**When to Apply:** Avoid member extensions in general code. Use top-level extensions for
broad utilities, local extensions for scoped utilities.

**Anti-Pattern:** Defining extension functions as members of a class to "organize" them;
using member extensions when a top-level extension or regular method would be clearer.

---

## Part 3: Efficiency

### Chapter 7: Make It Cheap (Items 45–48)

#### Item 45: Avoid Unnecessary Object Creation

**Category:** Efficiency — Allocation

**Core Practice:** Object creation has a cost (allocation, initialization, GC pressure).
In performance-sensitive code, reuse objects, use primitives, and avoid unnecessary allocation.

**Key Techniques:**
- Object reuse: `companion object` singletons, cached instances, `object` declarations
- Use `Int`, `Long`, `Double` (JVM primitives) instead of nullable `Int?`, `Long?`, `Double?` (boxed) in hot paths
- String: avoid concatenation in loops, use `buildString` or `StringBuilder`
- Caching: `lazy`, companion object caches, `HashMap`-based memoization
- Avoid: creating objects in tight loops when a mutable reusable object works
- Kotlin-specific: `inline` classes to wrap without allocation; `Sequence` to avoid intermediate lists
- Known costly operations: `Regex` creation (compile once, reuse), date formatter creation

**When to Apply:** In performance-critical paths: tight loops, hot functions, frequently
called code. Don't over-optimize cold paths — readability matters more there.

**Anti-Pattern:** Creating `Regex` in every function call; string concatenation in loops;
nullable primitives where non-null works; creating temporary objects per iteration.

---

#### Item 46: Use Inline Modifier for Functions with Functional Parameters

**Category:** Efficiency — Inline Functions

**Core Practice:** Lambda parameters create anonymous class instances and add invocation
overhead. The `inline` modifier copies the lambda body at the call site, eliminating
this overhead.

**Key Techniques:**
- `inline fun <T> Iterable<T>.myFilter(predicate: (T) -> Boolean): List<T>` — no lambda object created
- Most stdlib collection functions (`map`, `filter`, `forEach`, `let`, `apply`, etc.) are already inline
- `noinline` for lambda parameters that shouldn't be inlined (stored, passed elsewhere)
- `crossinline` for lambdas used in other contexts (coroutines, nested lambdas)
- `reified` type parameters: only work with `inline` — allow `T::class` usage
- Inline functions support non-local returns from lambdas

**When to Apply:** For higher-order functions that are called frequently, especially
utility functions and collection operations. Don't inline large function bodies (code bloat).

**Anti-Pattern:** Not inlining frequently-called higher-order functions; inlining large
functions with minimal lambda parameters (code bloat for little benefit).

---

#### Item 47: Consider Using Inline Value Classes

**Category:** Efficiency — Value Classes

**Core Practice:** Inline value classes (`@JvmInline value class`) wrap a single value
with type safety but are erased to the underlying type at runtime — zero allocation overhead.

**Key Techniques:**
- `@JvmInline value class UserId(val id: Long)` — type-safe wrapper, compiled to `Long` at runtime
- Use for: IDs, quantities with units, validated strings, domain primitives
- Prevents mixing up parameters of the same type: `fun assign(userId: UserId, taskId: TaskId)`
- Can have methods, implement interfaces, and have init blocks
- Limitations: single property in constructor, no `lateinit` or delegated properties
- On JVM, boxing occurs when: used as nullable, used as generic type parameter, used through interface

**When to Apply:** When you want type safety for primitive-like values without the
overhead of full wrapper classes. Great for domain IDs, measurements, and validated wrappers.

**Anti-Pattern:** Using raw `Long` for user IDs, task IDs, and order IDs (easy to mix up);
using full classes for simple wrappers adding GC pressure in hot paths.

---

#### Item 48: Eliminate Obsolete Object References

**Category:** Efficiency — Memory Management

**Core Practice:** Even with garbage collection, memory leaks occur when objects hold
references to other objects that are no longer needed. Null out references, use weak
references, and clean up listeners/callbacks.

**Key Techniques:**
- Set fields to `null` when the referenced object is no longer needed
- Clear collections that hold references to expired data
- Use `WeakReference` for caches and observer registrations
- Android-specific: unregister listeners in `onDestroy`/`onStop`, avoid Activity references in long-lived objects
- Beware closures: lambdas capture outer variables, potentially keeping large objects alive
- Use memory profilers to detect leaks: Android Studio Profiler, VisualVM, YourKit
- Common sources: static collections, listeners/callbacks, caches without eviction

**When to Apply:** Especially in long-running applications (servers, Android apps) and
when dealing with callbacks, caches, and observer patterns.

**Anti-Pattern:** Growing static collections without cleanup; registered observers never
unregistered; closures capturing Activity/Fragment references on Android.

---

### Chapter 8: Efficient Collection Processing (Items 49–52)

#### Item 49: Prefer Sequence for Big Collections with More Than One Processing Step

**Category:** Efficiency — Lazy Processing

**Core Practice:** Standard collection operations (`map`, `filter`, etc.) are eager — each
step creates an intermediate collection. `Sequence` is lazy — elements are processed one
at a time through the entire pipeline, with no intermediate collections.

**Key Techniques:**
- Convert with `.asSequence()`: `list.asSequence().filter { ... }.map { ... }.toList()`
- Sequence advantages: no intermediate collections, short-circuits (find/first/any stop early), handles large/infinite data
- Collection advantages: simpler debugging, order of operations sometimes matters, result is ready to use
- Rule of thumb: use Sequence when you have multiple chained operations on a large collection
- Terminal operations (`.toList()`, `.first()`, `.count()`, `.forEach()`) trigger evaluation
- `sequence { yield(); yieldAll() }` for custom generators
- For file processing: `File.useLines()` returns a Sequence

**When to Apply:** When chaining 2+ operations on collections of hundreds+ elements. The
larger the collection and the more operations, the bigger the benefit.

**Anti-Pattern:** Chaining `filter { }.map { }.flatMap { }` on large lists (creates 3 intermediate lists); not using `asSequence()` before complex collection pipelines.

---

#### Item 50: Limit the Number of Operations

**Category:** Efficiency — Operation Optimization

**Core Practice:** Choose the right collection function to minimize the number of operations.
Many common patterns have single-function equivalents that avoid unnecessary work.

**Key Techniques:**
- `any { }` instead of `filter { }.isNotEmpty()` — short-circuits on first match
- `none { }` instead of `filter { }.isEmpty()` — short-circuits on first match
- `firstOrNull { }` instead of `filter { }.firstOrNull()` — stops at first match
- `count { }` instead of `filter { }.count()` — avoids intermediate list
- `mapNotNull { }` instead of `map { }.filterNotNull()` — single pass
- `maxByOrNull { }` instead of `sortedBy { }.last()` — O(n) instead of O(n log n)
- `associateBy { }` instead of `map { it.key to it }.toMap()` — direct construction
- `flatMap { }` instead of `map { }.flatten()` — single pass
- `sumOf { }` instead of `map { }.sum()` — avoids intermediate list

**When to Apply:** Every time you chain collection operations. Check if a single function
can replace two chained ones.

**Anti-Pattern:** `list.filter { it > 0 }.count()` instead of `list.count { it > 0 }`;
`list.sortedBy { it.name }.first()` instead of `list.minByOrNull { it.name }`.

---

#### Item 51: Consider Arrays with Primitives for Performance-Critical Processing

**Category:** Efficiency — Primitive Arrays

**Core Practice:** `Array<Int>` boxes each element as `Integer`. For performance-critical
numeric processing, use `IntArray`, `LongArray`, `DoubleArray`, etc. which map to JVM
primitive arrays.

**Key Techniques:**
- `IntArray(size)`, `intArrayOf(1, 2, 3)` — JVM `int[]`, no boxing
- `LongArray`, `DoubleArray`, `FloatArray`, `BooleanArray`, `ByteArray`, etc.
- Significant performance difference in tight loops and large arrays
- `IntArray` uses ~4 bytes per element; `Array<Int>` uses ~16 bytes per element (object + reference)
- Can convert: `list.toIntArray()`, `intArray.toList()`
- Standard operations work: `intArray.map { }`, `intArray.filter { }`, but these return `List<Int>` — for staying in primitive land, use indices and manual loops or specialized libraries

**When to Apply:** For numeric processing with large arrays: scientific computing,
image processing, financial calculations, game engines, data analysis.

**Anti-Pattern:** Using `List<Int>` or `Array<Int>` for large numeric datasets where
`IntArray` would avoid boxing overhead.

---

#### Item 52: Consider Using Mutable Collections

**Category:** Efficiency — Collection Mutability for Performance

**Core Practice:** Immutable collections are preferred for safety, but in performance-critical
local scopes, mutable collections with in-place operations can be significantly faster
than immutable chains that create new collections at each step.

**Key Techniques:**
- Local mutability: `buildList { }`, `buildMap { }`, `buildSet { }` — mutable inside, immutable result
- `mutableListOf<T>()` + `add()` instead of `list + element` in a loop (avoiding O(n) copies)
- In-place sorting: `list.sort()` (mutates) vs `list.sorted()` (creates new list)
- For accumulation: `mutableMapOf<K, MutableList<V>>()` + `getOrPut { mutableListOf() }.add()`
- Keep mutability local: function builds with mutable, returns immutable
- API boundaries should use immutable types; internal hot paths can use mutable

**When to Apply:** In performance-sensitive code where collection operations are a bottleneck.
Always keep the mutability scope as narrow as possible.

**Anti-Pattern:** Using `fold` to accumulate into new lists (O(n²) for n elements); using
`+` in a loop to build a list; returning mutable collections from public APIs.
