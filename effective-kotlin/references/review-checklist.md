# Effective Kotlin — Code Review Checklist

Systematic checklist for reviewing Kotlin code against the 52 best-practice items
from *Effective Kotlin* (2nd Edition) by Marcin Moskała.

---

## 1. Safety (Items 1–10)

### Mutability & Scope
- [ ] **Item 1 — Limit mutability** — Are `val` and immutable collections used by default? Is `var` used only when truly necessary? Are mutable collections encapsulated?
- [ ] **Item 2 — Minimize variable scope** — Are variables declared close to first use? Are any variables declared at function-top that could be scoped tighter? Are `let`/`run` used to restrict scope?

### Null Safety & Types
- [ ] **Item 3 — Eliminate platform types** — At Java/Kotlin boundaries, are types explicitly annotated? Do platform types (`Type!`) leak into Kotlin APIs?
- [ ] **Item 4 — No exposed inferred types** — Do public functions and properties declare explicit types? Could an implementation change silently alter the public type?

### Preconditions & Error Handling
- [ ] **Item 5 — Specify expectations** — Are `require()` and `check()` used at function entry points? Are preconditions documented for public functions?
- [ ] **Item 6 — Standard errors** — Are standard exceptions (IllegalArgumentException, IllegalStateException) used instead of custom exceptions for common conditions?
- [ ] **Item 7 — Null or Failure for expected outcomes** — Do functions that can legitimately fail return `null` or `Result` instead of throwing? Are exceptions reserved for programming errors?
- [ ] **Item 8 — Proper null handling** — Is `!!` absent or justified? Are safe calls (`?.`), Elvis (`?:`), and smart casts used consistently? No unnecessary null checks?

### Resources & Testing
- [ ] **Item 9 — Resources with use()** — Are all Closeable/AutoCloseable resources wrapped with `use()`? Are file reads using `useLines()` or `use()`?
- [ ] **Item 10 — Unit tests** — Is business logic covered by tests? Are edge cases and error paths tested? Are tests independent and descriptive?

---

## 2. Readability (Items 11–18)

- [ ] **Item 11 — Design for readability** — Is the code clear on first read? Are there unnecessarily clever constructions? Are complex expressions broken into named intermediate variables?
- [ ] **Item 12 — Operator meaning consistent** — Do operator overloads match their conventional function names (`plus`, `times`, `contains`)? No surprising operator semantics?
- [ ] **Item 13 — No Unit? returns** — Does any function return `Unit?`? Is `Unit?` used in conditional logic? Replace with Boolean or sealed type.
- [ ] **Item 14 — Types specified when unclear** — Are inferred types obvious from context? Do public APIs have explicit type annotations? Would a reader need to navigate to a function to understand the type?
- [ ] **Item 15 — Explicit receivers** — In nested scope functions or DSLs, are receivers referenced explicitly when ambiguous? Is `@DslMarker` used for DSL scope control?
- [ ] **Item 16 — Properties represent state** — Do custom getters perform only cheap, side-effect-free, idempotent computations? Is behavior in functions, not properties?
- [ ] **Item 17 — Named arguments** — Are boolean parameters named? Are same-typed parameters named? Are configuration-style calls using named arguments?
- [ ] **Item 18 — Coding conventions** — Does the code follow Kotlin coding conventions? Are naming, formatting, and structure consistent? Is ktlint/detekt configured?

---

## 3. Reusability (Items 19–25)

- [ ] **Item 19 — No repeated knowledge** — Is any business rule, validation, or algorithm defined in more than one place? Is there a single source of truth for each concept?
- [ ] **Item 20 — stdlib used** — Are standard library functions used instead of hand-rolled equivalents? Check: collection operations, string building, scope functions.
- [ ] **Item 21 — Property delegation** — Are there repeated property patterns (lazy init, change notification, validation) that should use `by lazy`, `Delegates.observable`, or custom delegates?
- [ ] **Item 22 — Generics for algorithms** — Are utility functions generic where possible? Is there type-specific duplication that could be parameterized?
- [ ] **Item 23 — No shadowed type parameters** — In generic classes, do member functions avoid redeclaring the class's type parameter with the same name?
- [ ] **Item 24 — Variance considered** — Are `out`/`in` modifiers applied to type parameters that are only produced or consumed? Could variance allow more flexible subtype usage?
- [ ] **Item 25 — Multiplatform reuse** — If targeting multiple platforms, is platform-independent logic in common modules? Are `expect`/`actual` declarations used appropriately?

---

## 4. Abstraction Design (Items 26–32)

- [ ] **Item 26 — Single level of abstraction** — Does each function operate at one consistent level of detail? Are there functions mixing high-level orchestration with low-level manipulation?
- [ ] **Item 27 — Abstraction protects against changes** — Are external dependencies wrapped behind interfaces? Can implementations be swapped without changing business logic?
- [ ] **Item 28 — API stability specified** — Are experimental APIs annotated with `@RequiresOptIn`? Are deprecated elements marked with `@Deprecated` with `ReplaceWith`?
- [ ] **Item 29 — External APIs wrapped** — Are third-party libraries accessed through your own abstractions? Can they be mocked in tests?
- [ ] **Item 30 — Minimal visibility** — Is `private` the default? Are `internal` and `public` used only when needed? Do properties have restricted setters where appropriate?
- [ ] **Item 31 — Contracts documented** — Do public APIs have KDoc? Are parameters, return values, exceptions, and edge cases documented?
- [ ] **Item 32 — Contracts respected** — Do implementations honor the contracts of interfaces they implement? Are `equals`/`hashCode`/`compareTo` contracts maintained?

---

## 5. Object Creation (Items 33–35)

- [ ] **Item 33 — Factory functions considered** — Where constructors are limiting, are factory functions used? Are there complex constructors that would benefit from named factories?
- [ ] **Item 34 — Primary constructor with defaults** — Are Kotlin primary constructors with default values used instead of Java-style builders or telescoping constructors?
- [ ] **Item 35 — DSL for complex creation** — For hierarchical or complex object assembly, is a type-safe builder DSL used? Is `@DslMarker` applied?

---

## 6. Class Design (Items 36–44)

### Composition & Data
- [ ] **Item 36 — Composition over inheritance** — Is inheritance used only for IS-A relationships? Is Kotlin's `by` delegation used for code reuse? Are there fragile base class issues?
- [ ] **Item 37 — Data modifier** — Are data-holding classes using the `data` modifier? Are generated methods (equals, hashCode, copy, toString) appropriate?
- [ ] **Item 38 — Function types for single-method interfaces** — Are single-method interfaces replaced with function types `(A) -> B` or `fun interface`? Is SAM conversion used for Java interop?

### Hierarchies & Contracts
- [ ] **Item 39 — Sealed hierarchies over tagged classes** — Are there classes with type enums and conditional logic that should be sealed class hierarchies? Do `when` blocks benefit from exhaustiveness?
- [ ] **Item 40 — equals contract** — Is `equals` reflexive, symmetric, transitive, and consistent? Is it overridden together with `hashCode`? Does inheritance break symmetry?
- [ ] **Item 41 — hashCode contract** — Is `hashCode` consistent with `equals`? Are the same properties used in both? Are mutable objects used as hash keys?
- [ ] **Item 42 — compareTo contract** — Is `compareTo` antisymmetric, transitive, and consistent with equals? Is `compareBy`/`compareValuesBy` used for clean implementation?

### Extensions
- [ ] **Item 43 — Non-essential API in extensions** — Are classes bloated with utility methods that could be extensions? Could non-essential methods be extracted to improve core API focus?
- [ ] **Item 44 — No member extensions** — Are extension functions defined at top-level or locally, not as class members? Member extensions are confusing and limited.

---

## 7. Efficiency (Items 45–52)

### Object Creation & Inline
- [ ] **Item 45 — No unnecessary objects** — In hot paths: are Regex instances cached? Are strings concatenated with StringBuilder? Are primitives used instead of nullable/boxed types?
- [ ] **Item 46 — Inline for lambdas** — Are frequently-called higher-order functions marked `inline`? Is `noinline` used for stored lambdas? Is `reified` used where runtime type info is needed?
- [ ] **Item 47 — Inline value classes** — Are domain primitives (IDs, quantities, validated strings) using `@JvmInline value class` to avoid allocation? Are boxing scenarios understood?
- [ ] **Item 48 — Obsolete references eliminated** — Are unneeded references nulled out? Are caches bounded? Are listeners/callbacks properly unregistered? Are closure captures reviewed?

### Collection Processing
- [ ] **Item 49 — Sequence for multi-step processing** — For large collections with 2+ chained operations, is `.asSequence()` used? Are intermediate collections avoided?
- [ ] **Item 50 — Operations limited** — Is `any {}` used instead of `filter {}.isNotEmpty()`? Is `count {}` used instead of `filter {}.count()`? Is `maxByOrNull` used instead of `sortedBy {}.last()`?
- [ ] **Item 51 — Primitive arrays** — For numeric-heavy processing, are `IntArray`/`LongArray`/`DoubleArray` used instead of `List<Int>`/`Array<Int>`?
- [ ] **Item 52 — Mutable collections where needed** — In local scope hot paths, are mutable collections used for accumulation instead of repeated immutable concatenation? Is mutability kept local?

---

## Quick Review Workflow

1. **Safety first** — Scan for `!!`, `var`, unclosed resources, missing preconditions, platform types
2. **Readability pass** — Check for clarity, naming, operator usage, coding conventions
3. **Design assessment** — Evaluate abstraction levels, duplication, visibility, inheritance vs composition
4. **Kotlin idiom check** — Are Kotlin features (data class, sealed class, extension functions, scope functions, delegation) used appropriately?
5. **Efficiency review** — For hot paths only: check collection processing, object creation, inline opportunities
6. **Prioritize findings** — Rank by severity: safety > correctness > readability > design > efficiency

## Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Safety issues, potential crashes, data corruption | `!!` on user input, leaked resources, broken equals/hashCode, mutable shared state without synchronization |
| **High** | Incorrect Kotlin usage, missed null safety, design violations | Platform types leaking, inheritance abuse, throwing on expected failures, no precondition checks |
| **Medium** | Non-idiomatic code, missed Kotlin features, readability issues | Java-style builders, manual loops instead of stdlib, tagged classes, no named arguments for booleans |
| **Low** | Polish, minor optimizations, style improvements | Missing KDoc, Sequence opportunity, inline value class opportunity, convention inconsistencies |
