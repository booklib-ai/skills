# Clean Code — Practices Catalog

Catalog of the most actionable principles from Robert C. Martin's
*Clean Code: A Handbook of Agile Software Craftsmanship*, organized by category.
Each entry includes the heuristic code, a short description, and the key test question.

---

## Naming

### N1 — Choose Descriptive Names
**Code:** N1  
**Description:** A name should reveal its purpose so completely that the code reads like
well-written prose. If a name requires a comment to explain it, it doesn't do its job.
**Test question:** If someone reads only this name, do they know *why* this thing exists,
*what* it does, and *how* it's used?

### N2 — Names at the Appropriate Level of Abstraction
**Code:** N2  
**Description:** Names should match the abstraction level of the code they appear in.
A `Modem` interface's `dial(phoneNumber)` reveals implementation; `connect(connectionLocator)`
expresses the concept. Names at the right level can outlast implementation changes.
**Test question:** Would this name still make sense if the underlying implementation changed?

### N4 — Unambiguous Names
**Code:** N4  
**Description:** When two things in the same scope could be confused, names must be
precise enough to remove ambiguity. `doRename()` is ambiguous; `renamePageAndOptionallyAllReferences()`
is not. Verbosity in a name is cheaper than confusion in a reader.
**Test question:** Could a reader confuse this name with anything else in the same context?

### N5 — Long Names for Long Scopes
**Code:** N5  
**Description:** Single-letter variables are fine in a 3-line loop; in a 300-line function,
they are inscrutable. The length of a name should correspond to the size of the scope
it lives in. Long-lived names deserve investment.
**Test question:** If this variable were referenced 50 lines from its declaration,
would its name still be self-explanatory?

### N7 — Names Should Describe Side Effects
**Code:** N7  
**Description:** If a function named `getOos()` creates an `ObjectOutputStream` when
none exists, the name lies. Names must reflect everything the function does, including
side effects. `createOrReturnOos()` is honest.
**Test question:** Does this function's name describe *everything* it does, including
any state it changes?

---

## Functions

### Do One Thing (G30)
**Code:** G30  
**Description:** A function should do one thing, do it well, and do it only. The test:
can you extract a meaningful sub-function from the body? If yes, the function is doing
more than one thing. Functions that do one thing cannot be reasonably subdivided.
**Test question:** Can you extract a meaningfully named sub-function from this function's body?

### F1 — Too Many Arguments
**Code:** F1  
**Description:** The ideal number of function arguments is zero. One is fine. Two requires
thought. Three requires strong justification. More than three is almost always wrong.
When a function needs many related arguments, they usually form a concept that deserves
its own class or struct.
**Test question:** Could two or more arguments be wrapped into a meaningful object?

### F3 — Flag Arguments Are Ugly
**Code:** F3  
**Description:** Passing a boolean to a function is a clear sign the function does two
things — one for `true`, one for `false`. This violates "do one thing." The solution
is always to split the function into two: one for each behavior.
**Test question:** Does this function take a boolean that controls which of two paths it takes?

### F2 — Output Arguments
**Code:** F2  
**Description:** Arguments are inputs. Readers naturally assume you pass things *in* to
a function, not that a function writes results *back* through its parameters.
`appendFooter(s)` is confusing; `report.appendFooter()` is not.
**Test question:** Is the caller expected to read a result out of one of the arguments
passed to this function?

### G5 — Duplication
**Code:** G5  
**Description:** Duplication is the root of all evil in software. Duplicated code means
two chances to make the same mistake, two places to change when the logic evolves,
and two diverging truths. Every duplication should be addressed — usually by extraction,
TEMPLATE METHOD, or STRATEGY.
**Test question:** Does the same algorithm, condition, or business rule appear in more
than one place?

### G19 — Use Explanatory Variables
**Code:** G19  
**Description:** Complex calculations should be broken into named intermediate variables
that explain each step. `(hourlyRate * hoursWorked) - taxRate` becomes three named
variables that document the calculation's intent without a comment.
**Test question:** Would a named intermediate variable replace the need for a comment
explaining this expression?

### G28 — Encapsulate Conditionals
**Code:** G28  
**Description:** Boolean logic is hard to scan. Extract conditions into functions with
meaningful names. `if (shouldBeDeleted(timer))` reads like prose. `if (timer.hasExpired() && !timer.isRecurrent())`
requires the reader to parse logic rather than understand intent.
**Test question:** Can the condition be extracted into a function whose name expresses
what the condition means?

### G29 — Avoid Negative Conditionals
**Code:** G29  
**Description:** Negative conditionals are harder to understand than positive ones.
`buffer.shouldCompact()` is easier to parse than `!buffer.shouldNotCompact()`. Prefer
the positive form. When you need the negative, double-negatives (`not not`) are never acceptable.
**Test question:** Is this conditional expressed in its positive form?

---

## Comments

### C5 — Commented-Out Code
**Code:** C5  
**Description:** Commented-out code is an abomination. No one will delete it because
everyone assumes someone else put it there for a reason. It accumulates like sediment.
Delete it. Version control remembers everything. This is the single most important
comment smell to eliminate.
**Test question:** Is there any code that has been commented out?

### C3 — Redundant Comments
**Code:** C3  
**Description:** A comment that describes exactly what the code already says clearly
is pure noise. It clutters the file, takes time to read, and can drift out of sync.
If the code is clear, the comment is unnecessary. If the comment adds nothing, remove it.
**Test question:** Could you delete this comment and lose no information?

### C2 — Obsolete Comments
**Code:** C2  
**Description:** Comments age badly. A comment that was accurate when written becomes
misleading after the code changes. Misleading comments are worse than no comments —
they actively corrupt the reader's mental model.
**Test question:** Does this comment accurately describe what the code currently does?

### Intent vs. Explanation
**Code:** (general — Ch. 4)  
**Description:** The only valuable comments explain *why* — intent, rationale, warnings.
Comments that explain *what* the code does are redundant with the code itself. Invest in
renaming and restructuring until the *what* is obvious; then write a comment only if
the *why* is not.
**Test question:** Does this comment explain *why* rather than *what*?

---

## Error Handling

### Don't Return Null
**Code:** (Ch. 7)  
**Description:** Every null return is a potential NullPointerException waiting to happen.
If a function can return null, every caller must check — and one check missed causes a
runtime crash. Return a Special Case object (`Collections.emptyList()`, `NullEmployee`),
throw an exception, or use Optional.
**Test question:** Does this function return null to indicate failure or absence?

### Don't Pass Null
**Code:** (Ch. 7)  
**Description:** Passing null as a function argument is even worse than returning it.
There is no reasonable way for a function to handle an argument being null except with
defensive checks throughout. Use overloading, Optional, or default values instead.
**Test question:** Is null passed as an argument to any function?

### Exceptions Carry Context
**Code:** (Ch. 7)  
**Description:** A thrown exception should tell the receiver what operation failed and
why. An exception message of "Error" or a bare stack trace is useless in a log.
Include the operation being attempted and the failure type.
**Test question:** Does this exception message tell a reader what operation failed and why?

### Special Case Pattern
**Code:** (Ch. 7, Martin Fowler)  
**Description:** When a function is asked for something that might not exist
(a customer with no orders, a user with no profile), returning null forces every
caller to handle the absence. The Special Case pattern encapsulates the "nothing here"
behavior into an object that behaves like the real thing — callers don't need to check.
**Test question:** Is there a null check that could be replaced with a Special Case object?

---

## Objects and Data Structures

### G36 — Law of Demeter (Avoid Transitive Navigation)
**Code:** G36  
**Description:** Code should not navigate through a chain of objects to get at behavior
deep inside the structure: `a.getB().getC().doSomething()`. This couples the caller to
the entire chain. Expose what you need directly, or restructure so each class talks
only to its immediate collaborators.
**Test question:** Does this line navigate more than one association to get at behavior?

### G14 — Feature Envy
**Code:** G14  
**Description:** A method that uses another class's data more than its own is envious
of that class. This is a sign the method probably belongs in the other class. Move the
behavior to where the data lives.
**Test question:** Does this method use more fields or methods of another class than its own?

### G23 — Prefer Polymorphism to Switch/If-Else Chains
**Code:** G23  
**Description:** `switch` statements that check a type tag repeat themselves across the
codebase. When you add a new type, you must find and update every switch. Polymorphism
centralizes the variation in one place — the class hierarchy.
**Test question:** Does this switch or if-else chain select behavior based on a type tag?

---

## Classes

### Single Responsibility Principle
**Code:** (Ch. 10)  
**Description:** A class should have one, and only one, reason to change. If you can
describe what a class does only by using "and" or "or," it has more than one responsibility.
A class with multiple responsibilities is coupled to multiple change vectors.
**Test question:** Can this class be described in one sentence without "and" or "or"?

### G8 — Too Much Information
**Code:** G8  
**Description:** Well-defined interfaces expose little and demand little. A class with
many public methods, or a data class with many public fields, is hard to understand
and hard to change. The best interfaces hide almost everything.
**Test question:** Does this interface expose more than the caller absolutely needs?

### Open-Closed Principle
**Code:** (Ch. 10)  
**Description:** Classes should be open for extension but closed for modification.
When new behavior is needed, new code should be added — not existing code changed.
This is achieved through abstraction: depend on interfaces, not concretions.
**Test question:** Would adding a new variant of this behavior require modifying existing classes?

---

## Systems and Boundaries

### G35 — Keep Configurable Data at High Levels
**Code:** G35  
**Description:** Constants and configurable data (server addresses, timeout values,
feature limits) should be defined at the top of the system and passed down. Burying
a magic constant deep inside a business function makes it invisible and fragile.
**Test question:** Are there constants buried in low-level logic that should be defined at a higher level?

### Wrap Third-Party APIs
**Code:** (Ch. 8)  
**Description:** Third-party interfaces should not scatter through your codebase.
Wrap them in your own abstraction so you control the vocabulary, can mock them in tests,
and can swap them with a single change. The wrapping point is the clean boundary.
**Test question:** Can you change the underlying third-party library by modifying only one class?

### G13 — Artificial Coupling
**Code:** G13  
**Description:** Coupling two modules that have no structural reason to be related forces
them to change together. Artificial coupling often appears as a utility function placed
in a class because it was convenient, or a constant defined in a class that has nothing
to do with it.
**Test question:** Does this module have a dependency that exists only for convenience, not structure?

---

## Tests

### T1 — Insufficient Tests
**Code:** T1  
**Description:** A test suite is insufficient if it does not cover everything that could
possibly break. Developers must not be satisfied by a coverage number — they must think
about what the code does and verify each behavior.
**Test question:** Is there any behavior in this code that no test exercises?

### T5 — Test Boundary Conditions
**Code:** T5  
**Description:** Bugs hide at the edges. Empty collections, zero values, maximum values,
negative numbers, null inputs — boundary conditions are exactly where assumptions break.
Every algorithm has its edges; every edge deserves a test.
**Test question:** Are the minimum, maximum, and edge-case inputs tested?

### F.I.R.S.T.
**Code:** (Ch. 9)  
**Description:** Good tests are Fast (run in milliseconds), Independent (no order dependency),
Repeatable (same result in any environment), Self-validating (pass or fail, no manual check),
and Timely (written with the production code). Tests that violate these are not maintained.
**Test question:** Can every test in this suite be run in isolation, in any order, in any environment?
