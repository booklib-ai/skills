# Domain-Driven Design — Code Review Checklist

Systematic checklist for reviewing code against DDD principles. Organized by
category with specific items to inspect.

---

## 1. Ubiquitous Language

- [ ] **Class names match domain terms** — Classes are named after domain concepts the business recognizes, not technical abstractions (e.g., `Policy` not `RuleEngine`, `Shipment` not `DataTransferObject`)
- [ ] **Method names describe domain operations** — Methods read like domain actions (e.g., `order.cancel()` not `order.setStatus(CANCELLED)`, `account.debit(amount)` not `account.updateBalance(-amount)`)
- [ ] **No technical jargon in domain layer** — Avoid names like Manager, Handler, Processor, Helper, Util, Data, Info in the domain layer
- [ ] **Consistent vocabulary** — Same concept uses the same name everywhere. No synonyms (e.g., don't mix "client" and "customer" for the same concept)
- [ ] **Language reflects current understanding** — Terms have been refined as the model evolved, not stuck with initial naive names
- [ ] **Module/package names tell a domain story** — Packages are organized by domain concept, not by pattern type (not `entities/`, `services/`, `repositories/`)

## 2. Layered Architecture

- [ ] **Four layers identifiable** — UI/Presentation, Application, Domain, Infrastructure are clearly separated
- [ ] **Domain layer has zero outward dependencies** — Domain classes don't import UI, Application, or Infrastructure classes
- [ ] **Infrastructure implements domain interfaces** — Dependency Inversion: domain defines interfaces (e.g., `OrderRepository`), infrastructure implements them (e.g., `JpaOrderRepository`)
- [ ] **Application layer is thin** — Application services coordinate but contain NO business logic. They manage transactions, security, and use-case flow
- [ ] **No domain logic in controllers** — UI/API controllers delegate to application services, never contain business rules
- [ ] **No domain logic in infrastructure** — Persistence logic doesn't enforce business rules; it only stores and retrieves
- [ ] **No circular dependencies** — Lower layers never depend on higher layers

## 3. Entities

- [ ] **Identity is explicit** — Entity has a clear, typed identifier (preferably a Value Object like `OrderId`, not a raw `String` or `long`)
- [ ] **Equality based on identity** — `equals()` and `hashCode()` use the identifier, not attributes
- [ ] **Encapsulates behavior** — Entity contains domain logic, not just getters and setters
- [ ] **Lifecycle management** — Entity handles its own state transitions and lifecycle events
- [ ] **Not overloaded** — Entity is focused on identity and core behavior; ancillary logic is in Value Objects or Services
- [ ] **Attributes that change are still same entity** — Design acknowledges that attributes can change while identity persists

## 4. Value Objects

- [ ] **Immutable** — No setters, no mutable state. All fields are final/readonly
- [ ] **Equality by attributes** — `equals()` compares all attributes, not reference identity
- [ ] **Rich behavior** — Value Objects contain domain logic (calculations, validations, transformations), not just data
- [ ] **Side-effect-free methods** — Operations return new Value Objects rather than modifying state
- [ ] **Used instead of primitives** — Domain concepts like money, dates, addresses, quantities are Value Objects, not raw types (no `double price`, `String email`, `int quantity`)
- [ ] **Freely shareable** — No aliasing bugs because they're immutable
- [ ] **Self-validating** — Value Object constructor validates invariants (e.g., `Email` rejects invalid format)

## 5. Aggregates

- [ ] **Clear root entity** — One Entity is the root with global identity; all access goes through it
- [ ] **Boundary is defined** — It's clear which Entities and Value Objects are inside the Aggregate
- [ ] **Invariants enforced by root** — The root ensures all business rules within the boundary are consistent
- [ ] **No external references to internals** — Outside code cannot hold direct references to internal entities. References are through the root only
- [ ] **Kept small** — Aggregate contains only what's needed for invariant enforcement. Other Aggregates are referenced by ID
- [ ] **One Aggregate per transaction** — Changes to one Aggregate are committed in one transaction. Cross-Aggregate changes are eventually consistent
- [ ] **Delete cascades from root** — Removing the root removes everything inside the boundary
- [ ] **Internal entities have local identity** — IDs of internal entities are meaningful only within the Aggregate

## 6. Repositories

- [ ] **Only for Aggregate roots** — No Repository exists for internal Aggregate entities or Value Objects
- [ ] **Collection-like interface** — API resembles an in-memory collection: add, remove, find, query
- [ ] **Interface in domain layer** — The Repository interface is defined in the domain layer
- [ ] **Implementation in infrastructure** — The concrete class (JPA, JDBC, etc.) is in the infrastructure layer
- [ ] **Returns whole Aggregates** — Queries return fully reconstituted Aggregates, not partial objects or DTOs
- [ ] **No persistence leakage** — Domain code has no awareness of SQL, ORM annotations, or storage details
- [ ] **Encapsulates query strategy** — Complex queries are behind well-named methods, not scattered SQL
- [ ] **Delegates to Factory for reconstitution** — Complex object rebuilding is handled by a Factory, not in the Repository itself

## 7. Factories

- [ ] **Used for complex creation** — If creation requires more than a simple constructor, a Factory exists
- [ ] **Atomic creation** — Factory produces a valid, consistent object or fails entirely (no partially created objects)
- [ ] **Invariants enforced at creation** — All Aggregate invariants are validated during Factory creation
- [ ] **Abstracts concrete types** — Client code depends on abstractions, not on the specific class the Factory creates
- [ ] **Reconstitution vs. creation distinguished** — Factories for loading from persistence don't re-validate business rules that only apply at creation time, and don't generate new IDs

## 8. Domain Services

- [ ] **Stateless** — Domain Services hold no mutable state between calls
- [ ] **Named in Ubiquitous Language** — Service name describes a domain operation (e.g., `TransferService`, `PricingService`)
- [ ] **Not overused** — Domain Services are the exception, not the rule. Most behavior belongs on Entities and Value Objects
- [ ] **Parameters and return types are domain objects** — Service interfaces use domain types, not primitives or infrastructure types
- [ ] **No anemic domain model** — If all logic is in Services and Entities are just data bags, the model is anemic
- [ ] **Distinguished from Application Services** — Domain Services contain business logic; Application Services coordinate use cases

## 9. Supple Design

- [ ] **Intention-Revealing Interfaces** — Can a developer understand what a class/method does without reading the implementation?
- [ ] **Side-Effect-Free Functions** — Complex logic lives in pure functions (especially on Value Objects). Commands are simple state changes
- [ ] **Assertions / Post-conditions** — Critical invariants are documented or enforced. Tests verify post-conditions
- [ ] **Conceptual Contours** — Object boundaries align with natural domain concepts. Things that change together are together
- [ ] **Standalone Classes** — Dependencies are minimized. Each class can be understood with minimal context
- [ ] **Closure of Operations** — Operations on a type return the same type where natural (e.g., `Money.add(Money): Money`)
- [ ] **Declarative style** — Where possible, the code describes WHAT should happen, not HOW (e.g., specifications, rules)

## 10. Specification Pattern

- [ ] **Business rules as objects** — Complex boolean conditions are modeled as Specification objects, not inline conditionals
- [ ] **isSatisfiedBy method** — Each Specification has a clear test method
- [ ] **Composable** — Specifications can be combined with AND, OR, NOT
- [ ] **Three use cases considered** — Validation (testing), Selection (querying), Building-to-order (generation)
- [ ] **Named in domain language** — `OverdueInvoiceSpecification`, not `InvoiceFilter42`
- [ ] **Implemented as Value Objects** — Specifications are immutable and side-effect-free

## 11. Strategic Design — Bounded Contexts

- [ ] **Contexts are explicitly defined** — Each Bounded Context has a clear name and boundary
- [ ] **One model per context** — No concept is defined differently within the same context
- [ ] **Context Map exists** — Relationships between contexts are documented
- [ ] **Integration patterns identified** — Each context-to-context relationship uses a named pattern (Shared Kernel, ACL, Conformist, etc.)
- [ ] **No model bleeding** — Types from one context don't appear in another context's domain layer
- [ ] **Team boundaries align** — Ideally, one team per Bounded Context

## 12. Integration Patterns

- [ ] **Anticorruption Layer present where needed** — External systems and legacy integrations are wrapped in ACL
- [ ] **ACL components identifiable** — Façade, Adapter, and Translator are present as needed
- [ ] **Domain interfaces define integration** — The domain layer defines what it needs; infrastructure implements it
- [ ] **Shared Kernel is minimal** — If two contexts share code, the shared portion is as small as possible with joint CI
- [ ] **Open Host Service is well-documented** — Public APIs have clear protocols and versioning
- [ ] **Published Language is formal** — Shared data formats are documented and standardized
- [ ] **Conformist choice is conscious** — If a team conforms to an upstream model, it's a deliberate decision with documented trade-offs

## 13. Distillation

- [ ] **Core Domain identified** — The team knows which part of the system is the competitive differentiator
- [ ] **Best talent on Core** — The most skilled developers are working on the Core Domain
- [ ] **Generic Subdomains simplified** — Non-core parts use off-the-shelf solutions, simpler models, or outsourced implementations
- [ ] **Domain Vision Statement exists** — A short document describes the Core Domain's value proposition
- [ ] **Core is highlighted** — Developers can quickly identify which code is Core Domain (via packages, annotations, or documentation)
- [ ] **Segregated Core** — Core Domain code is in its own module with minimal dependencies on supporting code

## 14. Large-Scale Structure

- [ ] **Structure serves the team** — If a large-scale structure exists, it helps developers navigate and make decisions
- [ ] **Not over-engineered** — Structure is as simple as possible. No structure is better than bad structure
- [ ] **Evolving** — Structure is allowed to change as understanding deepens
- [ ] **Responsibility Layers (if used)** — Layers have clear domain-level responsibilities and dependencies flow downward
- [ ] **Knowledge Level (if used)** — Configuration rules are separated from operational data in a meta-model

---

## Quick Review Workflow

1. **Start with Ubiquitous Language** — Read the code. Does it speak the domain? Can a domain expert recognize the concepts?
2. **Check architecture** — Are layers separated? Does the domain depend on nothing?
3. **Inspect building blocks** — Are Entities, Value Objects, Aggregates, Repositories, and Services used correctly?
4. **Evaluate design quality** — Is the design supple? Intention-revealing? Side-effect-free where possible?
5. **Assess strategic alignment** — Are Bounded Contexts defined? Is the Core Domain getting the most attention?
6. **Flag anti-patterns** — Look for anemic domain model, God Aggregates, primitive obsession, leaking infrastructure, missing ACL

## Severity Levels

| Severity | Description | Example |
|----------|------------|---------|
| **Critical** | Broken invariants, data corruption risk, no domain model | Anemic domain model, no Aggregate boundaries, infrastructure in domain |
| **High** | Incorrect pattern application, model integrity issues | Repository for non-root, mutable Value Objects, leaked internals |
| **Medium** | Design improvement opportunities | Missing Specifications, primitive types for concepts, overly large Aggregates |
| **Low** | Polish and naming refinements | Inconsistent naming, missing documentation, suboptimal module organization |
