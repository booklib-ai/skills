# Clean Code — Heuristic Code Quick Reference

Complete reference tables for all heuristic codes from Chapter 17 of
*Clean Code* by Robert C. Martin. Use these codes in review feedback
to give reviewees a precise pointer to the underlying principle.

---

## Comments (C1–C5)

| Code | Name | One-Line Description |
|------|------|----------------------|
| **C1** | Inappropriate Information | Comments contain changelog entries, author attributions, dates, or metadata — put it in version control |
| **C2** | Obsolete Comment | Comment describes behavior the code no longer performs; it has drifted from reality |
| **C3** | Redundant Comment | Comment restates exactly what the code already says clearly — pure noise |
| **C4** | Poorly Written Comment | Comment is grammatically wrong, rambling, sloppy, or unclear — if worth writing, write it well |
| **C5** | Commented-Out Code | Code has been commented out instead of deleted — delete it, VCS remembers |

---

## Environment (E1–E2)

| Code | Name | One-Line Description |
|------|------|----------------------|
| **E1** | Build Requires More Than One Step | Building the project requires more than a single command — should be a one-step operation |
| **E2** | Tests Require More Than One Step | Running the tests requires manual configuration or multiple steps — should be one command |

---

## Functions (F1–F4)

| Code | Name | One-Line Description |
|------|------|----------------------|
| **F1** | Too Many Arguments | Function has more than 3 arguments — group related args into an object or redesign |
| **F2** | Output Arguments | A parameter is used as an output — use a return value or mutate `this`/`self` instead |
| **F3** | Flag Arguments | Function takes a boolean to select one of two behaviors — split into two functions |
| **F4** | Dead Function | Function is never called anywhere in the codebase — delete it |

---

## General (G1–G36)

| Code | Name | One-Line Description |
|------|------|----------------------|
| **G1** | Multiple Languages in One Source File | Source file mixes languages (HTML in Java, SQL inline in Python) — separate them |
| **G2** | Obvious Behavior Is Unimplemented | Function or class doesn't do what its name obviously promises — Principle of Least Surprise |
| **G3** | Incorrect Behavior at the Boundaries | Boundary conditions (empty input, max values, zero) are not handled or tested |
| **G4** | Overridden Safeties | Compiler warnings disabled, test failures ignored, assertions commented out — never do this |
| **G5** | Duplication | Same algorithm, business rule, or conditional appears in more than one place — extract it |
| **G6** | Code at Wrong Level of Abstraction | Low-level implementation details appear in high-level abstractions, or vice versa |
| **G7** | Base Classes Depending on Their Derivatives | A parent class imports or references a child class — reverse the dependency |
| **G8** | Too Much Information | Class or interface exposes far more than its clients need — narrow the interface |
| **G9** | Dead Code | Unreachable code paths, unused variables, uncalled functions — delete all of it |
| **G10** | Vertical Separation | Variables or functions are defined far from where they are used — move them closer |
| **G11** | Inconsistency | Same concept is handled differently in different parts of the codebase — pick one approach |
| **G12** | Clutter | Unused constructors, variables, default implementations, or imports that add no value |
| **G13** | Artificial Coupling | Modules are coupled for no structural reason — a utility placed in the wrong class |
| **G14** | Feature Envy | A method uses another class's data or methods more than its own — move it there |
| **G15** | Selector Arguments | Boolean or enum argument selects which of several behaviors to perform — split into separate functions |
| **G16** | Obscured Intent | Magic numbers, Hungarian notation, or dense expressions hide the code's purpose |
| **G17** | Misplaced Responsibility | A function or constant is placed in a surprising module — Principle of Least Surprise for placement |
| **G18** | Inappropriate Static | A static method that should be polymorphic — make it an instance method |
| **G19** | Use Explanatory Variables | A complex calculation should be broken into named intermediate variables that explain each step |
| **G20** | Function Names Should Say What They Do | `date.add(5)` is ambiguous — `date.addDays(5)` says exactly what it does |
| **G21** | Understand the Algorithm | Code arrived at by trial-and-error — understand *why* the algorithm works before shipping |
| **G22** | Make Logical Dependencies Physical | One module assumes something about another — make the assumption explicit in the type system |
| **G23** | Prefer Polymorphism to If/Else or Switch/Case | A switch on a type tag should usually be a polymorphic method call |
| **G24** | Follow Standard Conventions | Code should conform to team naming, formatting, and structural conventions |
| **G25** | Replace Magic Numbers with Named Constants | Literals like `86400` or `3.14159` should be named constants |
| **G26** | Be Precise | Using float for currency, ignoring concurrency, or assuming approximate equality — be exact |
| **G27** | Structure over Convention | Enforce design decisions with abstract methods and types rather than naming conventions |
| **G28** | Encapsulate Conditionals | Extract complex boolean logic into a named function: `shouldBeDeleted(timer)` not `timer.hasExpired() && !timer.isRecurrent()` |
| **G29** | Avoid Negative Conditionals | `buffer.shouldCompact()` is easier to parse than `!buffer.shouldNotCompact()` |
| **G30** | Functions Should Do One Thing | A function that can be subdivided into meaningful named parts is doing more than one thing |
| **G31** | Hidden Temporal Couplings | When function A must be called before function B, make that dependency visible in the structure |
| **G32** | Don't Be Arbitrary | Every structural decision should have a reason — arbitrary structure creates confusion |
| **G33** | Encapsulate Boundary Conditions | `level + 1` scattered inline should be `nextLevel = level + 1` declared once |
| **G34** | Functions Should Descend Only One Level of Abstraction | Each function should drop exactly one level below its stated purpose |
| **G35** | Keep Configurable Data at High Levels | Constants and configuration values belong at the top of the system, passed down — not buried in business logic |
| **G36** | Avoid Transitive Navigation | `a.getB().getC().doSomething()` couples you to the whole chain — Law of Demeter |

---

## Java-Specific (J1–J3)

| Code | Name | One-Line Description |
|------|------|----------------------|
| **J1** | Avoid Long Import Lists by Using Wildcards | When using many classes from a package, prefer wildcard imports (adapt to team convention) |
| **J2** | Don't Inherit Constants | Implementing an interface just to access its constants pollutes the class hierarchy — use static import |
| **J3** | Constants versus Enums | Use enums instead of integer constants — enums can have methods, fields, and are type-safe |

---

## Names (N1–N7)

| Code | Name | One-Line Description |
|------|------|----------------------|
| **N1** | Choose Descriptive Names | Every name should reveal intent so completely that no comment is needed to explain it |
| **N2** | Choose Names at the Appropriate Level of Abstraction | Names should match the abstraction level — `connect(locator)` not `dial(phoneNumber)` on an interface |
| **N3** | Use Standard Nomenclature Where Possible | Use design pattern names (`Visitor`, `Factory`) and domain language where they apply |
| **N4** | Unambiguous Names | Names should be precise enough that no two things in the same context could be confused |
| **N5** | Use Long Names for Long Scopes | Single-letter names in tight loops are fine; in wide scopes, invest in descriptive names |
| **N6** | Avoid Encodings | No Hungarian notation, no `m_` member prefix, no `I` interface prefix — they are noise |
| **N7** | Names Should Describe Side Effects | If `getOos()` creates an object when none exists, call it `createOrReturnOos()` |

---

## Tests (T1–T9)

| Code | Name | One-Line Description |
|------|------|----------------------|
| **T1** | Insufficient Tests | Test suite does not cover everything that could possibly break — if it can break, test it |
| **T2** | Use a Coverage Tool | Use a coverage tool and review gaps — a coverage number alone is not enough |
| **T3** | Don't Skip Trivial Tests | Even obvious tests have documentary value — their cost is low and their value is real |
| **T4** | An Ignored Test Is a Question about an Ambiguity | A skipped test represents an open question — document what is unclear and why |
| **T5** | Test Boundary Conditions | Bugs hide at edges — test minimum, maximum, empty, null, and off-by-one conditions |
| **T6** | Exhaustively Test Near Bugs | Bugs cluster — when you find a bug, test all surrounding logic thoroughly |
| **T7** | Patterns of Failure Are Revealing | Use test failure patterns to diagnose root causes rather than treating each failure in isolation |
| **T8** | Test Coverage Patterns Can Be Revealing | Look at which lines are uncovered — the pattern may reveal structural problems |
| **T9** | Tests Should Be Fast | Slow tests don't get run — if tests are slow, developers skip them and quality degrades |

---

## Chapter Summary Reference

| Chapter | Topic | Core Principle |
|---------|-------|----------------|
| Ch. 2 | Meaningful Names | Names should reveal intent; avoid disinformation and noise words |
| Ch. 3 | Functions | Small, one thing, one level of abstraction, minimal arguments |
| Ch. 4 | Comments | Comments are a failure to express intent in code; use sparingly and purposefully |
| Ch. 5 | Formatting | Code is communication; newspaper metaphor, vertical density/openness, team consistency |
| Ch. 6 | Objects and Data Structures | Objects hide data; data structures expose it. Law of Demeter. No hybrids. |
| Ch. 7 | Error Handling | Use exceptions; never return null; exceptions carry context |
| Ch. 8 | Boundaries | Wrap third-party APIs; write learning tests; maintain clean boundaries |
| Ch. 9 | Unit Tests | F.I.R.S.T.; one concept per test; tests are as important as production code |
| Ch. 10 | Classes | Small (by responsibility); SRP; high cohesion; OCP; DIP |
| Ch. 11 | Systems | Separate construction from use; dependency injection; cross-cutting concerns |
| Ch. 12 | Emergence | Four rules: tests pass, no duplication, expresses intent, minimizes classes/methods |
| Ch. 13 | Concurrency | Separate concurrency from logic; limit shared data; keep synchronized sections small |
| Ch. 17 | Smells and Heuristics | C1-C5, E1-E2, F1-F4, G1-G36, J1-J3, N1-N7, T1-T9 |

---

## Heuristic Code Pattern for Review Comments

When writing review feedback, reference heuristic codes inline:

```
The function `processData` takes four arguments [F1] including a boolean flag [F3].
The flag controls whether to validate or skip — split into `processAndValidate()` 
and `processWithoutValidation()` [G30].

The variable `x` is used 40 lines from its declaration [G10] and the name 
doesn't reveal its purpose [N1].

There are two near-identical validation blocks on lines 34 and 78 [G5]. 
Extract to a shared `validateInput()` function.
```
