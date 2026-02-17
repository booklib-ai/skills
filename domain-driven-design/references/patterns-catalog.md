# Domain-Driven Design — Patterns Catalog

Complete catalog of patterns from Eric Evans' *Domain-Driven Design: Tackling
Complexity in the Heart of Software*, organized by part and chapter.

---

## Part I — Putting the Domain Model to Work

### Ubiquitous Language
**Problem:** Developers and domain experts use different vocabularies, leading to
translation overhead, misunderstandings, and models that diverge from reality.

**Solution:** Establish a shared language rooted in the domain model. Use this
language in all communication — conversations, documentation, code, diagrams.
Class names, method names, and module names should all reflect the Ubiquitous
Language. When the language changes, the model changes, and vice versa.

**Key rules:**
- One language per Bounded Context
- Language appears in code — not just documents
- Changes to the language are changes to the model
- If a concept has no name in the language, the model is incomplete

### Model-Driven Design
**Problem:** Analysis models and design models diverge. The conceptual model
doesn't map to the code, creating a disconnect that undermines the model's value.

**Solution:** The design model IS the analysis model. The code directly reflects
the domain model. No separate "analysis model" that gets translated into a
"design model." Model-Driven Design requires that the model work as both
an analysis tool and as the basis for the code.

**Key rules:**
- Every design decision reflects a modeling decision
- If the code can't express the model, revise the model
- If the model doesn't serve the design, revise the model
- Hands-on modelers: the people writing code must participate in modeling

### Hands-On Modelers
**Problem:** When modelers don't code and coders don't model, the model
degrades. "Ivory tower" architects produce models that don't work in practice.

**Solution:** The modeler must also be a hands-on implementer. Modeling
and implementation feed back into each other. Anyone responsible for changing
code must learn to express a model through code. Any developer who touches
the code must be empowered to refactor the model.

---

## Part II — Building Blocks of Model-Driven Design

### Layered Architecture
**Problem:** Domain logic mixed with UI, database, and application concerns
becomes tangled and impossible to reason about.

**Solution:** Separate the system into four layers:

| Layer | Responsibility |
|-------|---------------|
| **User Interface (Presentation)** | Display information, interpret user commands |
| **Application** | Coordinates tasks, delegates to domain objects. Thin layer — no business logic. Manages transactions, security, and use case flow |
| **Domain** | Heart of the software. Business concepts, rules, information. This is where DDD patterns live |
| **Infrastructure** | Technical capabilities: persistence, messaging, UI frameworks. Supports all other layers |

**Key rules:**
- Each layer depends only on layers below it
- Domain layer has NO dependencies on other layers
- Infrastructure implements interfaces defined in the domain layer (Dependency Inversion)
- Application layer orchestrates but contains no business rules

### Entity
**Problem:** Some objects are defined by their identity and continuity, not by
their attributes. A Person isn't defined by their name (which can change) but by
a persistent identity.

**Solution:** Model objects with identity and lifecycle as Entities. Define
equality based on identity (ID), not attributes. Maintain continuity through
a lifecycle of changes.

**Key rules:**
- Each Entity has a unique identifier
- Equality is based on ID, not attributes
- Strip Entity classes down to the most intrinsic characteristics — identity and lifecycle behavior
- Attributes can change; identity persists
- Define what "same" means clearly (e.g., same database row, same SSN, same order number)

### Value Object
**Problem:** Not every object needs identity. Modeling everything as an Entity
adds unnecessary complexity.

**Solution:** When you care only about the attributes of an element, model it as
a Value Object. Make it immutable. Define equality based on attribute values.

**Key rules:**
- No identity — two Value Objects with the same attributes are equal and interchangeable
- Immutable — all operations return new instances, no state modification
- Side-effect-free — methods on Value Objects are pure functions
- Can be freely shared, passed, and copied
- Rich behavior — don't make them anemic. Put computation and domain logic on Value Objects
- Examples: Money, Address, DateRange, Color, Coordinates, PhoneNumber

**Design preference:** Favor Value Objects over Entities. They are simpler,
safer (immutable, no aliasing bugs), and easier to test.

### Domain Service
**Problem:** Some domain operations don't naturally belong to any Entity or Value
Object. Forcing them onto an Entity makes the Entity bloated and unclear.

**Solution:** Model these operations as stateless Services in the domain layer.
Name them using the Ubiquitous Language. They operate on domain objects but
live as standalone operations.

**Three characteristics of a good Domain Service:**
1. The operation relates to a domain concept not a natural part of an Entity or Value Object
2. The interface is defined in terms of other domain model elements
3. The operation is stateless

**Distinguish from other service layers:**
| Layer | Service examples |
|-------|-----------------|
| Application Service | Transfer between accounts (orchestration), Send notification |
| Domain Service | Calculate transfer fee, Determine overdraft policy |
| Infrastructure Service | Send email, Log to file, Query external API |

### Module (Package)
**Problem:** As models grow, developers need a way to organize and navigate
large numbers of classes.

**Solution:** Use Modules to group highly cohesive domain concepts. Modules
are part of the model — they tell a story about the domain, not the technology.

**Key rules:**
- Low coupling between Modules, high cohesion within
- Module names are part of the Ubiquitous Language
- Don't organize by pattern type (all Entities in one package). Organize by domain concept
- Refactor Modules as the model evolves — don't let packaging become rigid

### Aggregate
**Problem:** Complex associations between objects make it impossible to maintain
consistency. If any object can change any other, invariants break.

**Solution:** Cluster Entities and Value Objects into Aggregates. Each has a
root Entity and a boundary. External objects can only hold references to the root.
The root enforces all invariants for objects within the boundary.

**Key rules:**
- Root Entity has global identity; internal entities have local identity only
- Nothing outside the Aggregate boundary can hold a reference to an internal object (except transient references)
- Only the root can be obtained directly from a Repository. All other objects are reached by traversal from the root
- Objects within the Aggregate can hold references to other Aggregate roots
- Deletion of the root removes everything within the boundary
- When a change to any object within the Aggregate is committed, all invariants of the whole Aggregate must be satisfied
- Keep Aggregates small — prefer references by ID to other Aggregates over large clusters
- One transaction per Aggregate. Cross-Aggregate consistency is eventual

### Factory
**Problem:** Creating complex Aggregates or objects with many invariants is
cumbersome and leaks construction details into client code.

**Solution:** Encapsulate creation logic in Factories. A Factory creates an
object in one atomic operation, enforcing all invariants.

**When to use a Factory vs. constructor:**
- Constructor: Simple creation, few arguments, no invariants
- Factory Method on Aggregate root: Creating internal elements of the Aggregate
- Standalone Factory: Complex creation crossing multiple objects, reconstitution from persistence

**Key rules:**
- Each creation method is atomic — yields a consistent product or throws
- Factory is not part of the domain model. It's a design element serving the model
- Reconstitution Factories (from persistence) don't assign new IDs or run validation that only applies to new objects
- Factory abstracts away the concrete classes created — client depends on interfaces/abstract types

### Repository
**Problem:** Clients need to obtain references to existing domain objects.
Direct database queries scatter persistence logic throughout the domain.

**Solution:** Provide a collection-like interface for accessing domain objects.
Repositories encapsulate the technology used for data retrieval. To the client,
it feels like an in-memory collection of domain objects.

**Key rules:**
- Repositories exist only for Aggregate roots
- Provide add/remove/query operations using the Ubiquitous Language
- Encapsulate all storage and retrieval technology
- Reconstitute full Aggregates (not partial objects)
- Repository interface is defined in the domain layer; implementation is in infrastructure
- Delegate to Factories for reconstitution when complex
- Keep queries focused — query specifications can help for complex searching

---

## Part III — Refactoring Toward Deeper Insight

### Specification Pattern
**Problem:** Business rules like "is this customer eligible?" combine multiple
predicates. Embedding them in Entities bloats the Entity; putting them in the
application layer drains behavior from the domain.

**Solution:** Create explicit Specification objects that encapsulate boolean
business rules. Each Specification has an `isSatisfiedBy(candidate)` method.
Specifications can be combined with AND, OR, NOT.

**Three use cases:**
1. **Validation** — Does this object satisfy the specification?
2. **Selection** — Find objects matching the specification (query)
3. **Building to order** — Create an object that satisfies the specification

**Key rules:**
- Each specification is a Value Object — immutable and side-effect-free
- Combinators (and, or, not) enable composition without modifying existing specifications
- The specification expresses a domain concept, named in the Ubiquitous Language
- Can be used to generate database queries (specification-to-query translation)

### Intention-Revealing Interfaces
**Problem:** If a developer must read the implementation to understand what a
component does, the design has failed.

**Solution:** Name classes and operations to describe their effect and purpose,
not their implementation. Write method signatures so the return type and
parameters tell the story. Clients should be able to use a component correctly
by reading the interface alone.

### Side-Effect-Free Functions
**Problem:** Operations that modify state create hidden complexity. Combining
them creates unpredictable results.

**Solution:** Place as much domain logic as possible in pure functions —
operations that return results without modifying any observable state. Value
Objects are the natural home for side-effect-free functions.

**Key rules:**
- Commands (modify state) and queries (return values) should be separate
- Move complex logic to Value Objects that compute and return new Value Objects
- Commands on Entities should be simple state changes; heavy computation goes to Value Objects

### Assertions
**Problem:** When side effects are buried in complex method chains, developers
can't predict what will happen.

**Solution:** State post-conditions of operations and invariants of classes and
Aggregates. Document or enforce what must be true after an operation completes.
Use assertion-based testing to verify invariants.

### Conceptual Contours
**Problem:** Object boundaries that don't match domain concepts lead to
awkward APIs — splitting what should be together or coupling what should be separate.

**Solution:** Align object boundaries with the conceptual contours of the domain.
Find the natural seams where concepts divide. Operations that change together
belong together. A change in the domain should require changes in only one place.

### Standalone Classes
**Problem:** Every dependency makes a class harder to understand. A web of
dependencies can make simple concepts unmanageable.

**Solution:** Actively minimize dependencies. Low coupling is fundamental to
object design. Where possible, create classes that can be understood in isolation.

### Closure of Operations
**Problem:** Introducing new types for every operation result increases
complexity.

**Solution:** Where it fits, define operations so the return type is the same
as the type of the argument(s). Example: adding two Money objects returns Money.
Combining two Specifications returns a Specification.

### Strategy / Policy Pattern (in Domain Context)
**Problem:** A process or rule needs to vary by context but the overall algorithm
structure remains the same.

**Solution:** Factor out the varying part into a separate Strategy object
(called a "Policy" in domain terms). The Strategy encapsulates an alternative
algorithm or business rule, expressed in domain language.

**Example:** Different shipping cost policies (FlatRate, WeightBased, ZoneBased)
implement a ShippingPolicy interface.

### Composite Pattern (in Domain Context)
**Problem:** Domain concepts have a natural recursive, nested structure where
individual elements and groups should be treated uniformly.

**Solution:** Define an abstract type for the domain concept. Both individual
items and groups implement this type. Operations on the group delegate to
all children.

**Example:** A Route composed of Legs. Each Leg is itself a Route. Operations
like calculateDistance work identically on simple and composite routes.

---

## Part IV — Strategic Design

### Bounded Context
**Problem:** In any large system, a single unified model is impractical.
Different parts of the organization have different meanings for the same terms.
"Account" means one thing to billing and another to authentication.

**Solution:** Explicitly define the boundary within which a particular model is
defined and applicable. Within a Bounded Context, keep the model strictly
consistent. Don't try to apply a model outside its context.

**Key rules:**
- Each Bounded Context has its own Ubiquitous Language
- The same real-world concept may be modeled differently in different contexts
- Code for one context should not be mixed with another
- Context boundaries often align with team boundaries
- A Bounded Context is not a Module — it's an explicit boundary around a model

### Continuous Integration
**Problem:** Within a Bounded Context, models fragment as multiple developers
make independent changes.

**Solution:** Institute Continuous Integration within each Bounded Context:
frequent merging of all code, automated tests exercising the model, and constant
communication. The goal is model-level integration, not just code compilation.

### Context Map
**Problem:** Without a global view of contexts, integration is ad hoc and teams
make incompatible assumptions.

**Solution:** Draw a Context Map — a document identifying each Bounded Context
and the relationships between them. The map is descriptive (what IS), not
prescriptive. It shows upstream/downstream relationships, shared models,
and translation layers.

**Relationship patterns on a Context Map:**
- Shared Kernel
- Customer/Supplier
- Conformist
- Anticorruption Layer
- Open Host Service / Published Language
- Separate Ways

### Shared Kernel
**Problem:** Two teams need to share a subset of the model. Without explicit
agreement, changes in one team break the other.

**Solution:** Designate a small subset of the domain model that both teams agree
to share. This shared code can't be changed without consulting the other team.
Include CI tests that both teams run.

**Key rules:**
- Keep the shared kernel as small as possible
- Both teams must agree to any change
- Automated tests run by both teams validate consistency
- Larger than necessary shared kernels become Big Balls of Mud

### Customer/Supplier Development
**Problem:** One system (downstream/customer) depends on another
(upstream/supplier). The downstream team has no influence over the upstream API.

**Solution:** Establish a clear customer/supplier relationship. The downstream
team communicates their needs. The upstream team negotiates and commits to
supporting them. Automated acceptance tests, written by the downstream team
and run in the upstream CI, validate that needs are met.

### Conformist
**Problem:** The upstream team has no motivation or ability to support the
downstream team's needs. The Customer/Supplier relationship has failed.

**Solution:** The downstream team conforms to the upstream model. Eliminates
the complexity of translation at the cost of limiting the downstream model.
Use when the upstream model is good enough and translation isn't worth the cost.

### Anticorruption Layer (ACL)
**Problem:** Integrating with a legacy system, external service, or different
Bounded Context whose model is unsuitable for your domain.

**Solution:** Build a translation layer — the Anticorruption Layer — that
isolates your model from the external model.

**Components:**
- **Façade** — Simplified interface to the external system (optional — use when the external API is complex)
- **Adapter** — Translates between the external system's interface and your domain's interface
- **Translator** — Converts data between the external model and your domain model

**Key rules:**
- Your domain layer never imports external system types
- The ACL is infrastructure, implementing domain-defined interfaces
- Testing the ACL validates the translation, not the external system
- The ACL can be thin or thick depending on how different the models are

### Separate Ways
**Problem:** Integration with another context is too costly relative to the
benefit.

**Solution:** Declare the two contexts to have no integration. The teams go
their separate ways. This is a legitimate strategic choice when the cost of
integration exceeds the value.

### Open Host Service
**Problem:** One system needs to expose functionality to many other systems.
Building custom translations for each consumer doesn't scale.

**Solution:** Define a protocol (Open Host Service) that gives access to your
system as a set of well-defined services. When a new integration need arises,
add to the protocol. For special cases, build one-off translators.

### Published Language
**Problem:** Direct translation between two domain models is complex and
tightly couples them.

**Solution:** Use a well-documented shared language (Published Language) as
a common medium for communication between Bounded Contexts. Often combines
with Open Host Service. Examples: iCalendar for scheduling, XBRL for financial
reporting, JSON Schema for APIs.

### Core Domain
**Problem:** In a large domain model, not everything is equally important. If
developers spread equal effort across all parts, the most valuable and complex
part gets insufficient attention.

**Solution:** Identify the Core Domain — the part of the model that is the
fundamental competitive differentiator. Assign the best developers. Focus
modeling effort here. Invest in deep modeling and supple design for the Core.

**Key rules:**
- Core Domain is what makes the system worth building
- It's the hardest part to model and the most valuable
- If you can buy it off-the-shelf or outsource it, it's not the Core Domain
- Write a Domain Vision Statement: a short document describing the Core Domain and its value

### Generic Subdomain
**Problem:** Parts of the model are necessary but not distinctive. Building
custom, polished solutions for them wastes effort that should go to the Core.

**Solution:** Identify Generic Subdomains — areas that can be handled with
off-the-shelf solutions, outsourced development, or simpler implementations.
Don't invest in deep modeling here.

**Options for Generic Subdomains:**
1. Off-the-shelf solution (buy it)
2. Outsource to external team
3. Published design/model from existing literature
4. In-house implementation — but with minimal investment

### Domain Vision Statement
**Problem:** The Core Domain lacks a clear, concise description that guides
decision-making.

**Solution:** Write a short document (about one page) describing the Core Domain
and the value it provides. Focus on what distinguishes the system from others.
Use this to guide model refinement and to communicate with new team members.

### Highlighted Core
**Problem:** Even when the Core Domain is defined, it may not be obvious in a
large codebase which elements belong to it.

**Solution:** Two complementary techniques:
1. **Distillation Document** — A short document (3-7 pages) that describes the
   Core Domain's essential concepts and interactions. Not comprehensive — just
   enough to point developers to the most critical parts
2. **Flagged Core** — Mark Core Domain elements directly in the code with
   annotations, package naming conventions, or documentation tags

### Cohesive Mechanism
**Problem:** Complex computations or algorithms clutter the domain model with
implementation details.

**Solution:** Extract complex mechanisms into separate lightweight frameworks or
utility classes. The domain model delegates to the mechanism. The mechanism is
generic and reusable; the domain model remains expressive.

**Example:** A complex graph traversal algorithm for routing. The routing domain
model expresses what routes mean; the mechanism handles how to compute them.

### Segregated Core
**Problem:** The Core Domain is tangled with supporting code and Generic
Subdomains within the same Bounded Context.

**Solution:** Refactor to separate the Core Domain into its own Module or package.
Reduce coupling to the supporting code. The Core Domain Module should have
minimal dependencies. Supporting elements depend on the Core, not vice versa.

### Abstract Core
**Problem:** Even within a Segregated Core, there may be so much detail that the
essential model is hard to see.

**Solution:** Identify the most fundamental abstract concepts in the Core Domain.
Place these into a separate Module. This abstract core consists of abstract
classes and interfaces that capture the essence of the model. Specialized
implementation Modules depend on and extend the abstract core.

### Responsibility Layers
**Problem:** In a large system, it's hard to understand how the major parts
relate to each other and what role each subsystem plays.

**Solution:** Organize large-scale structure using Responsibility Layers.
Each layer has a broad responsibility within the domain:

| Layer | Responsibility |
|-------|---------------|
| **Potential** | What could be — resources, capabilities, capacity |
| **Decision Support** | Analysis, forecasting, projections |
| **Policy** | Rules, goals, constraints that guide operations |
| **Operations** | What is happening now — day-to-day activities |

**Key rules:**
- Layers depend downward only (Operations depends on Policy, not vice versa)
- This is a domain-concept structuring, not a technical layering
- Not every system needs all layers
- Let the structure evolve — impose it gently

### Knowledge Level
**Problem:** A domain has rules that users need to configure. Hard-coding
the rules forces code changes for what should be configuration. But making
everything configurable creates complexity.

**Solution:** Create a Knowledge Level — a group of objects that describes
how another group of objects should behave. It's a meta-model. The Knowledge
Level defines the rules; the operational level follows them.

**Example:** In an employee scheduling system, the Knowledge Level defines what
types of shifts exist, what qualifications are required, and how assignments
work. The operational level has actual employees, shifts, and assignments
that follow the Knowledge Level's rules.

### Pluggable Component Framework
**Problem:** Multiple implementations of a subsystem need to be interchangeable
in a mature ecosystem.

**Solution:** Define interfaces and a protocol for interaction so that
different implementations can be substituted. All components conform to the
interfaces defined by the Abstract Core.

**Key rules:**
- Requires a mature, well-distilled Abstract Core
- Components interact only through the framework's defined interfaces
- Don't attempt this too early — it requires deep domain understanding first

### Evolving Order
**Problem:** Imposing too much structure too early constrains the design.
No structure at all leads to chaos.

**Solution:** Let large-scale structure evolve gradually. Don't impose it on
day one. As patterns emerge, gently formalize them. Be willing to abandon
or change the structure as understanding deepens.

**Key rules:**
- Structure should make development easier, not harder
- If the structure is getting in the way, simplify or remove it
- A bad structure is worse than no structure
- Favor minimalism — the least structure that helps
