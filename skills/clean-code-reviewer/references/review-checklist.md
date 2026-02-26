# Clean Code — Code Review Checklist

Systematic checklist for reviewing code against the principles from Robert C. Martin's
*Clean Code: A Handbook of Agile Software Craftsmanship*.

---

## Chapter 2 — Meaningful Names

### Intention and Clarity
- [ ] **N1 — Descriptive names** — Does every name (variable, function, class) tell you *why* it exists, *what* it does, and *how* it's used? Would a name require a comment to explain it?
- [ ] **N4 — Unambiguous names** — Is each name precise and unambiguous? Could `rename()` instead be `renamePageAndOptionallyAllReferences()`? Would a more specific name prevent confusion?
- [ ] **N2 — Appropriate abstraction level** — Do names match the level of abstraction of the code? Is `dial(phoneNumber)` where `connect(connectionLocator)` would be more general and honest?

### Avoiding Misinformation and Noise
- [ ] **No disinformation** — Do any names actively mislead? Is `accountList` actually not a `List`? Are platform abbreviations (`hp`, `aix`, `sco`) used as variable names?
- [ ] **No meaningless distinctions** — Are names meaningfully different from each other? Is there `ProductData` vs. `ProductInfo`, `data` vs. `info`, `a1` vs. `a2`? Noise words add nothing.
- [ ] **N6 — No encodings** — Is there Hungarian notation, `m_` member prefixes, or `I`-prefixed interface names? Modern IDEs make these unnecessary.

### Conventions and Consistency
- [ ] **Class names** — Are class names nouns or noun phrases (`Customer`, `WikiPage`, `Account`)? Are vague names like `Manager`, `Processor`, `Data`, `Info` avoided?
- [ ] **Method names** — Are method names verbs or verb phrases (`postPayment`, `deletePage`, `save`)? Do accessors, mutators, and predicates use `get`/`set`/`is` prefixes?
- [ ] **One word per concept** — Is one consistent word used per abstract concept across the codebase? Is the code mixing `fetch`, `retrieve`, and `get` for equivalent operations?
- [ ] **No puns** — Is the same word used for two different purposes? Does `add` mean "concatenate" in one place and "insert into collection" in another?
- [ ] **N3 — Standard nomenclature** — Are design pattern names used when patterns are applied (`AccountVisitor`, `JobQueue`)? Does code near domain concepts use domain vocabulary?
- [ ] **N5 — Scope-appropriate length** — Is `i` used in a 5-line loop but a 500-line scope? The length of a name should correspond to the size of its scope.

### Context
- [ ] **Meaningful context** — Does `state` alone appear where `addrState` or an `Address` class would clarify? Does the surrounding structure provide context?
- [ ] **No gratuitous context** — Are class or variable names prefixed with an application abbreviation (e.g., every class starting with `GSD`)? Short, clear names are better.
- [ ] **Pronounceable** — Could every name be discussed in conversation? Is `genymdhms` used where `generationTimestamp` belongs?
- [ ] **Searchable** — Are single-letter variables and magic numbers scoped to very short blocks where their meaning is unambiguous?

---

## Chapter 3 — Functions

### Size and Focus
- [ ] **Small** — Are functions short? Does each block within `if`, `else`, and `while` resolve to one line, ideally a function call? Would any function fit on one screen?
- [ ] **G30 / Do one thing** — Can you extract a meaningfully named function from the body? If yes, the function is doing more than one thing.
- [ ] **One level of abstraction** — Does the function mix high-level intent (e.g., `renderPage()`) with low-level manipulation (e.g., direct string concatenation)? Functions should read top-down, each leading to the next level of abstraction (the Stepdown Rule).
- [ ] **G34 — Descend only one level** — Does each function descend exactly one level of abstraction below the function's stated name?

### Arguments
- [ ] **F1 — Argument count** — Does any function take more than three arguments? Three requires strong justification. More than three: extract into an argument object.
- [ ] **F3 — Flag arguments** — Does any function take a boolean parameter? A flag argument loudly declares the function does two things. Split it into two functions.
- [ ] **F2 — Output arguments** — Does any argument serve as an output? Output arguments are counterintuitive. Use return values, or use `this`/`self`.
- [ ] **Argument objects** — When 2-3 arguments are closely related (e.g., `x, y, radius`), should they be grouped into an object (`Point center, double radius`)?

### Side Effects and Structure
- [ ] **No side effects** — Does a function named `checkPassword` also initialize a session? Does a function do something other than what its name says?
- [ ] **Command-Query Separation** — Does any function both modify state *and* return a value? Functions should either do something or answer something, never both.
- [ ] **F4 — Dead functions** — Are there functions that are never called? Delete them; version control remembers.
- [ ] **G5 — No duplication** — Is any algorithm, validation rule, or business logic repeated? Is TEMPLATE METHOD or STRATEGY applicable?

### Error Handling
- [ ] **Exceptions over return codes** — Are error conditions signaled by throwing exceptions rather than returning error codes?
- [ ] **Error handling is one thing** — If a function has a `try` block, does the function do *only* error handling? Are the bodies of `try` and `catch` extracted into their own functions?
- [ ] **Switch statements** — If a switch statement exists, is it buried in an abstract factory that uses polymorphism? Is it the only such switch in the codebase for that type?

---

## Chapter 4 — Comments

### Bad Comments to Eliminate
- [ ] **C5 — Commented-out code** — Is there any code that has been commented out? Delete it. Version control remembers. This is the worst comment smell.
- [ ] **C3 — Redundant comments** — Does any comment restate what the code already says clearly? (`i++; // increment i`). Does the comment take longer to read than the code?
- [ ] **C2 — Obsolete comments** — Do any comments describe behavior that the code no longer performs? Have comments drifted from the code they annotate?
- [ ] **C1 — Inappropriate information** — Do comments contain changelogs, author attributions, dates, or metadata that belongs in version control?
- [ ] **C4 — Poorly written comments** — Are any comments grammatically wrong, rambling, or unclear? If a comment is worth writing, it's worth writing well.
- [ ] **Noise comments** — Are there comments like `/** Default constructor */` or `/** The day of the month */` that state the obvious?
- [ ] **Closing brace comments** — Are there comments like `} // while` or `} // if`? These indicate functions that are too long. Shorten the function instead.
- [ ] **Byline comments** — Are there `// Added by Rick` comments? Version control tracks authorship.

### Good Comments to Verify
- [ ] **Intent comments** — Do comments explain *why* a decision was made, not *what* the code does? This is the only comment form that adds value not already in the code.
- [ ] **Warning comments** — Are there consequences worth warning future developers about (e.g., `// Don't run unless you have time to kill`)?
- [ ] **TODO comments** — Are TODO comments specific and actionable? Are they tracked and not accumulating as permanent clutter?
- [ ] **Public API documentation** — Do all public APIs have clear documentation comments that explain parameters, return values, and exceptions?

---

## Chapter 5 — Formatting

- [ ] **Newspaper metaphor** — Does each source file read like a newspaper? Is the class name at the top, high-level abstractions near the top, and details near the bottom?
- [ ] **Vertical openness** — Are separate concepts separated by blank lines? Can distinct sections (imports, fields, methods) be visually distinguished?
- [ ] **Vertical density** — Are closely related lines grouped tightly together without blank lines breaking up what belongs together?
- [ ] **Vertical distance** — Are variables declared close to their first use? Are related functions close to each other, with callers above callees?
- [ ] **Line length** — Are all lines short enough to avoid horizontal scrolling? Is a consistent maximum line length enforced across the team?
- [ ] **Team rules** — Does the formatting match team conventions? Is an automated formatter (Prettier, Black, ktlint, gofmt) enforced?

---

## Chapter 6 — Objects and Data Structures

- [ ] **Data/Object anti-symmetry** — Is data hiding appropriate? Do objects expose behavior and hide data? Do data structures expose data and have no significant behavior?
- [ ] **G36 / Law of Demeter** — Does any method call a method on an object returned by another method (`a.getB().getC().doSomething()`)? Does the code navigate association chains it should not know about?
- [ ] **No train wrecks** — Are chained method calls (`a.getB().getC().getD()`) broken up into intermediate variables or redesigned?
- [ ] **No hybrids** — Are there classes that are half-object (hiding data behind methods) and half-data structure (exposing fields directly)? These are the worst of both worlds.
- [ ] **DTOs** — Are Data Transfer Objects (database rows, API payloads) simple data structures with public fields and no behavior?

---

## Chapter 7 — Error Handling

- [ ] **Exceptions over return codes** — Are all error conditions communicated by exceptions, not return codes or sentinel values?
- [ ] **Try-catch-finally first** — When writing functions that can fail, does the structure start with the `try-catch-finally` to define the transaction boundary?
- [ ] **Context with exceptions** — Do thrown exceptions include the failed operation and the type of failure? Are raw stack traces the only diagnostic?
- [ ] **Caller-defined exception classes** — Are third-party exceptions wrapped into a common type that the caller needs, rather than leaking library-specific exception hierarchies?
- [ ] **Special Case pattern** — Is null returned where a Special Case object (e.g., `NullEmployee`, `Collections.emptyList()`) would let the caller avoid special-case logic?
- [ ] **Don't return null** — Does any function return `null` to indicate failure or absence? Every null return is a potential crash. Return a Special Case object or throw.
- [ ] **Don't pass null** — Is `null` passed as a function argument? This forces defensive null checks everywhere. Use Optional, overloading, or a Special Case.

---

## Chapter 8 — Boundaries

- [ ] **Wrap third-party APIs** — Are third-party interfaces accessed directly throughout the codebase? Do you control the vocabulary for the dependency, or does the dependency control yours?
- [ ] **Learning tests** — Are third-party APIs explored and verified through learning tests? Do these tests serve as living documentation of expected behavior?
- [ ] **Clean boundaries** — Is third-party knowledge isolated to specific adapter/wrapper classes? Would a library swap require changes in more than one place?

---

## Chapter 9 — Unit Tests

### Test Quality
- [ ] **T1 — Sufficient tests** — Does the test suite cover everything that could possibly break? Are there critical paths, edge cases, or error conditions with no tests?
- [ ] **Readable tests** — Is each test readable? Does it follow BUILD-OPERATE-CHECK (Arrange-Act-Assert / Given-When-Then)?
- [ ] **One concept per test** — Does each test verify one and only one concept? When a test fails, is it immediately obvious what is broken?
- [ ] **T3 — No skipped trivial tests** — Are trivial tests skipped or deleted? Even trivial tests have documentary value.
- [ ] **T4 — Ignored tests documented** — Are any tests marked as skipped or ignored? Does each have a clear note about the ambiguity or open question it represents?

### F.I.R.S.T. Properties
- [ ] **T9 — Fast** — Do all tests run quickly? Would slow tests cause developers to avoid running them?
- [ ] **Independent** — Do tests depend on each other? Can they be run in any order?
- [ ] **Repeatable** — Do tests pass in every environment (local, CI, other machines)?
- [ ] **Self-validating** — Do tests produce a clear pass/fail with no manual inspection required?
- [ ] **Timely** — Were tests written alongside or before the production code they cover?

### Coverage and Boundaries
- [ ] **T2 — Coverage tool** — Is a coverage tool being used? Are coverage gaps reviewed, not just a coverage number?
- [ ] **T5 — Boundary conditions** — Are boundary conditions tested? Off-by-one errors, empty collections, maximum sizes, negative values?
- [ ] **T6 — Near bugs** — When a bug is found and fixed, are exhaustive tests added for the surrounding code? Bugs cluster.
- [ ] **T7 — Failure patterns** — Do test failures form a pattern? Can that pattern diagnose the root cause rather than a symptom?
- [ ] **T8 — Coverage patterns** — Does the pattern of uncovered code reveal structural problems?

---

## Chapter 10 — Classes

- [ ] **Small (by responsibility)** — Is each class small? Measured not in lines but in *responsibilities*. Can you describe what the class does without using "and" or "or"?
- [ ] **Single Responsibility Principle** — Does each class have one, and only one, reason to change? Is there any mixing of business logic, persistence, presentation, or logging?
- [ ] **High cohesion** — Do most methods in the class use most of the instance variables? Are there methods that touch only 1-2 fields — a sign they belong elsewhere?
- [ ] **Open-Closed Principle** — Can the behavior of the class be extended without modifying it? Do new features require changing existing classes, or adding new ones?
- [ ] **Dependency Inversion** — Do high-level classes depend on abstractions (interfaces/abstract classes) rather than concrete implementations?

---

## Chapter 11 — Systems

- [ ] **Separate construction from use** — Is object construction (dependency wiring) mixed into business logic? Construction should happen at startup; business logic should work with already-built objects.
- [ ] **Dependency injection** — Are dependencies injected rather than instantiated inside classes? Does any business logic call `new` on a concrete class it shouldn't know about?
- [ ] **Cross-cutting concerns** — Are cross-cutting concerns (logging, security, transactions) handled through aspects, decorators, or interceptors rather than scattered throughout business logic?
- [ ] **G35 — Configurable data at high levels** — Are magic constants and configurable values (hostnames, limits, feature flags) defined at the top level and passed down, not buried deep in low-level code?

---

## Chapter 17 — Smells and Heuristics (Full Heuristic Reference)

### Comments (C-codes)
- [ ] **C1** — Does any comment contain changelog entries, author names, dates, or other metadata that belongs in version control?
- [ ] **C2** — Does any comment describe behavior that the current code no longer performs? Is it stale?
- [ ] **C3** — Does any comment simply restate what the code says clearly on its own?
- [ ] **C4** — Is any comment poorly written, rambling, or grammatically incorrect?
- [ ] **C5** — Is there any commented-out code? Delete it immediately.

### General (G-codes)
- [ ] **G1** — Does any source file contain code in multiple languages (HTML embedded in Java, SQL inline in Python)?
- [ ] **G2** — Does the code implement what a reader would obviously expect from the function/class name? (Principle of Least Surprise)
- [ ] **G3** — Has the code been tested at all boundary conditions? Not just the happy path.
- [ ] **G4** — Are any safeties disabled? Overridden warnings? Silently caught exceptions? Commented-out assertions?
- [ ] **G5** — Is any code, algorithm, or business rule duplicated? Every duplication should be addressed with TEMPLATE METHOD, STRATEGY, or extraction.
- [ ] **G6** — Are any methods or variables at the wrong level of abstraction? Do lower-level details appear in higher-level classes?
- [ ] **G7** — Do any base classes import or depend on their derived classes?
- [ ] **G8** — Do any interfaces expose more methods than the caller needs? Do data classes expose more fields than necessary?
- [ ] **G9** — Is there any unreachable code, dead conditional branches, or functions that can never be called?
- [ ] **G10** — Are variables or utility functions defined far from where they are used?
- [ ] **G11** — Is the same concept handled differently in different parts of the codebase?
- [ ] **G12** — Is there clutter: unused variables, empty constructors, functions that are never called?
- [ ] **G13** — Are there artificial couplings between modules that share no structural relationship?
- [ ] **G14** — Do methods use data from another class more than their own? Feature Envy — move the method closer to the data.
- [ ] **G15** — Do any functions take boolean or enum selector arguments to choose behavior? Split into separate functions.
- [ ] **G16** — Are there magic numbers, Hungarian notation, or run-on expressions that obscure intent?
- [ ] **G17** — Is any functionality placed in a surprising module or class? (Principle of Least Surprise for placement)
- [ ] **G18** — Are there static methods that should be instance methods? Would the behavior need to vary polymorphically?
- [ ] **G19** — Are complex calculations broken into named intermediate variables that explain each step?
- [ ] **G20** — Does `date.add(5)` exist where `date.addDays(5)` would be clearer? Do function names say what they do?
- [ ] **G21** — Is there any algorithm that was arrived at by trial-and-error? Does the author understand why the algorithm works?
- [ ] **G22** — Does any module assume something about another module without making that assumption explicit in the structure?
- [ ] **G23** — Are there `if/else` or `switch/case` chains where polymorphism would be cleaner and more extensible?
- [ ] **G24** — Does the code follow the team's standard conventions for naming, formatting, and structure?
- [ ] **G25** — Are there magic numbers (3, 86400, 0.01) that should be named constants?
- [ ] **G26** — Is float used for currency? Are concurrent data structures used without locks? Is precision being assumed where it must be enforced?
- [ ] **G27** — Is a naming convention used where an abstract method would force compliance? (`switch` on type tag vs. polymorphic method)
- [ ] **G28** — Are complex conditionals extracted into descriptive boolean functions? (`if (shouldBeDeleted(timer))` vs. `if (timer.hasExpired() && !timer.isRecurrent())`)
- [ ] **G29** — Are conditionals written positively where possible? (`if (buffer.shouldCompact())` vs. `if (!buffer.shouldNotCompact())`)
- [ ] **G30** — Do functions do more than one thing? (Same as Ch. 3 — "Do one thing")
- [ ] **G31** — Are there hidden temporal couplings where one function must be called before another with no structural enforcement?
- [ ] **G32** — Is there unexplained structure — decisions made without a discernible reason?
- [ ] **G33** — Are boundary conditions (`level + 1`, `offset + 1`) encapsulated in explanatory variables rather than scattered inline?
- [ ] **G34** — Do functions descend more than one level of abstraction below the function's name?
- [ ] **G35** — Are configurable constants buried deep in a function body rather than defined at the highest meaningful level?
- [ ] **G36** — Does any code reach through a chain of associations to get at data? (`a.getB().getC()`) — Law of Demeter violation.

### Names (N-codes)
- [ ] **N1** — Are all names descriptive? Do they make the code readable on its own?
- [ ] **N2** — Are names appropriate for the level of abstraction? Not too specific, not too vague?
- [ ] **N3** — Are standard names from design patterns and domain language used where applicable?
- [ ] **N4** — Are names precise enough to be unambiguous between similar concepts?
- [ ] **N5** — Do names scale in length with their scope? Long names for long-lived variables, short for tightly scoped.
- [ ] **N6** — Is there any encoding in names (Hungarian notation, `m_` prefix, type suffixes)?
- [ ] **N7** — Do function names describe side effects? Does `getOos()` that creates an object need to be `createOrReturnOos()`?

### Tests (T-codes)
- [ ] **T1** — Does the test suite cover all logic that could possibly break?
- [ ] **T2** — Is a coverage tool being used and its output reviewed?
- [ ] **T3** — Are trivial tests present? They have documentary value even if they seem obvious.
- [ ] **T4** — Are ignored/skipped tests marked with a note explaining the open question?
- [ ] **T5** — Are boundary conditions tested?
- [ ] **T6** — When a bug is fixed, are exhaustive tests added for the surrounding logic?
- [ ] **T7** — Are patterns of test failure used to diagnose root causes?
- [ ] **T8** — Is the pattern of uncovered code analyzed for structural insight?
- [ ] **T9** — Do all tests run fast enough that developers run them frequently?

---

## Quick Review Workflow

1. **Naming pass** — Read every name. Does each name reveal intent? Would any name require a comment to explain it?
2. **Function pass** — Evaluate each function: size, argument count, single responsibility, no side effects, no flag args.
3. **Comment audit** — Eliminate C1-C5 smells. Verify any surviving comments add intent not present in the code.
4. **Structure check** — Formatting, vertical distance, newspaper metaphor, class cohesion.
5. **Error handling** — No null returns, no error codes, exceptions with context, Special Case pattern where applicable.
6. **G-code scan** — Run through G1-G36 for systemic smells.
7. **Test quality** — F.I.R.S.T., T1-T9, one concept per test, boundary conditions.

## Severity Levels

| Severity | Description | Examples |
|----------|-------------|---------|
| **Critical** | Fundamentally undermines readability or introduces likely bugs | Commented-out code (C5), null returns on failure, disabled safeties (G4), dead code (G9) |
| **High** | Meaningful quality violations that should be fixed | Flag arguments (F3), train wrecks (G36), feature envy (G14), insufficient tests (T1) |
| **Medium** | Non-idiomatic patterns that hurt long-term maintainability | Magic numbers (G25), negative conditionals (G29), missing boundary tests (T5), misleading names |
| **Low** | Polish and refinements | Noise comments (C3), missing explanatory variables (G19), minor convention violations (G24) |
