# Design Patterns Catalog

Complete reference for all 23 GoF design patterns organized by category, based on
*Head First Design Patterns* by Eric Freeman & Elisabeth Robson.

---

## Creational Patterns

Patterns that deal with object creation mechanisms, trying to create objects in a
manner suitable to the situation.

### Factory Method

**Intent:** Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.

**Problem it solves:** Client code needs to create objects but shouldn't be coupled to specific concrete classes. New types may be added without modifying existing code.

**Participants:**
- **Creator** — Abstract class with the factory method (e.g., `PizzaStore`)
- **ConcreteCreator** — Subclass that implements the factory method (e.g., `NYPizzaStore`, `ChicagoPizzaStore`)
- **Product** — Interface for the objects created (e.g., `Pizza`)
- **ConcreteProduct** — Specific product classes (e.g., `NYStyleCheesePizza`)

**Key characteristics:**
- Creator declares abstract `factoryMethod()` returning Product type
- Subclasses override to return specific ConcreteProduct
- Creator may have default implementation
- Follows Dependency Inversion Principle: depend on abstractions, not concretions
- The "decision" of what to create is pushed to subclasses

**When to use:**
- A class can't anticipate the class of objects it must create
- A class wants its subclasses to specify the objects it creates
- You need to decouple client code from concrete classes

**Book example:** PizzaStore with orderPizza() template and createPizza() factory method. NYPizzaStore and ChicagoPizzaStore decide which pizza style to create.

---

### Abstract Factory

**Intent:** Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

**Problem it solves:** A system needs to create families of related objects (e.g., all NY-style ingredients or all Chicago-style ingredients) that must be used together.

**Participants:**
- **AbstractFactory** — Interface declaring creation methods for each product type (e.g., `PizzaIngredientFactory`)
- **ConcreteFactory** — Implements creation for a specific family (e.g., `NYPizzaIngredientFactory`)
- **AbstractProduct** — Interface for each product type (e.g., `Dough`, `Sauce`, `Cheese`)
- **ConcreteProduct** — Family-specific products (e.g., `ThinCrustDough`, `MarinaraSauce`)

**Key characteristics:**
- Groups related factory methods into a single interface
- Ensures compatible products are created together
- Adding new product families is easy (new ConcreteFactory)
- Adding new product types requires changing the interface (harder)
- Often uses Factory Methods internally

**When to use:**
- A system must be independent of how its products are created
- A system must use one of several families of products
- Related products are designed to be used together and you need to enforce this constraint

**Book example:** PizzaIngredientFactory creates families of ingredients (dough, sauce, cheese, veggies, pepperoni, clams). NYPizzaIngredientFactory and ChicagoPizzaIngredientFactory produce region-specific ingredient sets.

---

### Singleton

**Intent:** Ensure a class has only one instance and provide a global point of access to it.

**Problem it solves:** Some objects should only have one instance (thread pools, caches, dialog boxes, registry settings, logging objects, device drivers).

**Participants:**
- **Singleton** — Class with a private constructor and a static method that returns the sole instance

**Key characteristics:**
- Private constructor prevents external instantiation
- Static method (e.g., `getInstance()`) returns the unique instance
- Lazy initialization: instance created on first request
- Thread safety considerations are critical:
  - **Eager initialization** — Create at class load time (simplest, always thread-safe)
  - **synchronized method** — Thread-safe but may impact performance
  - **Double-checked locking** — Only synchronize on first creation (use `volatile`)
  - **Enum-based** — Most robust in Java (handles serialization and reflection)

**When to use:**
- Exactly one instance of a class is required
- The sole instance must be accessible from a well-known access point
- Be cautious: Singleton is often overused as a glorified global variable

**Pitfalls:**
- Multiple classloaders can create multiple instances
- Reflection can bypass private constructor
- Serialization can create new instances (unless handled)
- Makes unit testing harder due to global state
- Violates Single Responsibility (manages its own lifecycle + its actual job)

**Book example:** Chocolate boiler that must have only one instance to avoid overflow/waste scenarios. Thread-safety issues demonstrated with multiple threads.

---

### Builder

**Intent:** Separate the construction of a complex object from its representation so that the same construction process can create different representations.

**Problem it solves:** Object creation involves many steps or configurations. Constructors with many parameters become unwieldy. Different representations need the same build process.

**Participants:**
- **Builder** — Interface specifying steps to build each part
- **ConcreteBuilder** — Implements the steps for a specific representation
- **Director** — Constructs the object using the Builder interface
- **Product** — The complex object being built

**Key characteristics:**
- Step-by-step construction process
- Director controls the algorithm; Builder knows the specifics
- Same construction process, different resulting products
- Product is retrieved from the Builder after construction completes
- Often uses fluent interface (method chaining) in modern implementations

**When to use:**
- Algorithm for creating a complex object should be independent of its parts
- Construction must allow different representations
- Constructor has too many parameters (telescoping constructor problem)

**Book example:** Vacation planner that builds different types of vacations (outdoor adventure, city sightseeing) using the same step-by-step planning process.

---

### Prototype

**Intent:** Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.

**Problem it solves:** Creating new objects is expensive or complex, but similar objects already exist. You need many instances that differ slightly from existing ones.

**Participants:**
- **Prototype** — Interface declaring a `clone()` method
- **ConcretePrototype** — Implements clone to copy itself
- **Client** — Creates new objects by asking a prototype to clone itself
- **Registry/Manager** — Optional catalog of available prototypes

**Key characteristics:**
- Objects create copies of themselves
- Shallow vs deep copy considerations are important
- Avoids expensive creation from scratch
- Prototype registry allows dynamic addition of new types at runtime
- Client doesn't need to know concrete classes

**When to use:**
- Creating instances is expensive (database reads, complex computation)
- System should be independent of how its products are created
- Classes to instantiate are specified at runtime
- You need copies of existing objects with slight modifications

**Book example:** Monster registry where game creates new monsters by cloning prototypical instances rather than constructing from scratch each time.

---

## Structural Patterns

Patterns that deal with object composition, creating relationships between objects
to form larger structures.

### Adapter

**Intent:** Convert the interface of a class into another interface that clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.

**Problem it solves:** You have an existing class whose interface doesn't match what client code needs. You want to use a third-party class but its interface doesn't fit your system.

**Participants:**
- **Target** — The interface the client expects (e.g., `Duck`)
- **Adapter** — Translates calls from Target interface to Adaptee (e.g., `TurkeyAdapter`)
- **Adaptee** — The existing class with an incompatible interface (e.g., `Turkey`)
- **Client** — Works with the Target interface

**Key characteristics:**
- Object Adapter uses composition (wraps adaptee) — preferred
- Class Adapter uses multiple inheritance (where available)
- Adapter translates method calls, may need to handle mismatches in methods
- Can adapt a single class or multiple classes (facade-like adapter)
- The adaptee doesn't know it's being adapted

**When to use:**
- You want to use an existing class but its interface doesn't match your needs
- You want to create a reusable class that cooperates with unrelated classes
- You need to use several existing subclasses but can't adapt each by subclassing

**Book example:** TurkeyAdapter wrapping Turkey to make it work where Duck is expected. Also Enumeration-to-Iterator adapter for Java legacy collections.

---

### Bridge

**Intent:** Decouple an abstraction from its implementation so that the two can vary independently.

**Problem it solves:** You have a class hierarchy that is growing in two dimensions (e.g., different types AND different platforms). Without Bridge, you get a combinatorial explosion of subclasses.

**Participants:**
- **Abstraction** — High-level control interface (e.g., `RemoteControl`)
- **RefinedAbstraction** — Extension of the abstraction (e.g., `AdvancedRemoteControl`)
- **Implementor** — Interface for implementation classes (e.g., `TV`)
- **ConcreteImplementor** — Specific implementation (e.g., `SonyTV`, `LGTV`)

**Key characteristics:**
- Abstraction holds a reference to an Implementor
- Both hierarchies can be extended independently
- Avoids permanent binding between abstraction and implementation
- Composition replaces inheritance across two dimensions
- Changes to implementation don't affect client code

**When to use:**
- You want to avoid a permanent binding between abstraction and implementation
- Both abstractions and implementations should be extensible by subclassing
- Implementation changes should not impact clients
- You have a proliferation of classes resulting from coupled interface/implementation hierarchy

**Book example:** Remote controls (abstraction) and TVs (implementation). New remote features and new TV brands can be added independently without affecting each other.

---

### Composite

**Intent:** Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly.

**Problem it solves:** You need to represent hierarchical structures where both individual items and groups of items should be treated the same way (menus with sub-menus, file systems, organizational charts).

**Participants:**
- **Component** — Interface for all objects in the composition (e.g., `MenuComponent`)
- **Leaf** — Represents end objects with no children (e.g., `MenuItem`)
- **Composite** — Has children, implements child-related operations (e.g., `Menu`)
- **Client** — Manipulates objects through the Component interface

**Key characteristics:**
- Tree structure with uniform interface
- Leaves and composites implement the same interface
- Composites delegate to children and may add own behavior
- Trade-off: transparency (uniform interface) vs safety (separate leaf/composite types)
- Null Iterator pattern for leaves that have no children
- Component may throw UnsupportedOperationException for inapplicable methods

**When to use:**
- You want to represent part-whole hierarchies of objects
- You want clients to ignore the difference between compositions and individual objects
- All objects in the structure should be treated uniformly

**Book example:** Restaurant menu system with Menus containing MenuItems and sub-Menus. Printing the entire menu hierarchy traverses the composite tree uniformly.

---

### Decorator

**Intent:** Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

**Problem it solves:** You need to add behavior to individual objects without affecting others of the same class. Subclassing for every combination leads to class explosion.

**Participants:**
- **Component** — Interface for objects that can have responsibilities added (e.g., `Beverage`)
- **ConcreteComponent** — Object to which additional responsibilities can be attached (e.g., `DarkRoast`)
- **Decorator** — Abstract class that wraps a Component and conforms to its interface (e.g., `CondimentDecorator`)
- **ConcreteDecorator** — Adds responsibilities (e.g., `Mocha`, `Whip`, `Soy`)

**Key characteristics:**
- Decorators have the same supertype as the objects they decorate
- One or more decorators can wrap an object
- Decorator adds its own behavior before/after delegating to the wrapped object
- Objects can be decorated at runtime with any combination
- Follows Open-Closed Principle: extend behavior without modifying existing code
- Can result in many small objects — harder to debug

**When to use:**
- You need to add responsibilities to individual objects dynamically and transparently
- Extending functionality by subclassing is impractical (too many combinations)
- You want to add behavior that can be withdrawn later

**Book example:** Starbuzz Coffee with beverages and condiments. Mocha(Whip(DarkRoast)) computes cost and description by wrapping, each decorator adding its price and label.

---

### Facade

**Intent:** Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.

**Problem it solves:** A subsystem has many classes with complex interactions. Clients need a simpler way to perform common tasks without understanding the subsystem's internals.

**Participants:**
- **Facade** — Provides simplified methods that delegate to subsystem classes (e.g., `HomeTheaterFacade`)
- **Subsystem classes** — The complex classes being simplified (e.g., `Amplifier`, `DVDPlayer`, `Projector`, `Screen`, `PopcornPopper`)

**Key characteristics:**
- Doesn't encapsulate subsystem — clients can still use subsystem directly if needed
- Simplifies the interface without adding new functionality
- Decouples client from subsystem classes
- Follows Principle of Least Knowledge (Law of Demeter)
- Can have multiple facades for different aspects of a subsystem
- Facade doesn't prevent direct access to subsystem when needed

**When to use:**
- You want to provide a simple interface to a complex subsystem
- There are many dependencies between clients and implementation classes
- You want to layer your subsystems

**Book example:** Home theater system where watchMovie() coordinates turning on amplifier, setting tuner, dimming lights, lowering screen, starting projector, and playing the DVD.

---

### Flyweight

**Intent:** Use sharing to support large numbers of fine-grained objects efficiently.

**Problem it solves:** An application needs a huge number of objects that share common state. Storing all state in each object would consume too much memory.

**Participants:**
- **Flyweight** — Interface through which flyweights receive and act on extrinsic state
- **ConcreteFlyweight** — Stores intrinsic (shared) state
- **FlyweightFactory** — Creates and manages flyweight objects, ensures proper sharing
- **Client** — Maintains extrinsic state, passes it to flyweights

**Key characteristics:**
- **Intrinsic state** — Stored in the flyweight, shared, context-independent (e.g., tree type, texture)
- **Extrinsic state** — Stored externally, context-dependent, passed to flyweight (e.g., position, age)
- Factory ensures flyweights are shared (returns existing instance or creates new)
- Dramatic reduction in number of objects
- Trade-off: computation time for looking up/computing extrinsic state

**When to use:**
- An application uses a large number of objects
- Storage costs are high due to sheer quantity
- Most object state can be made extrinsic
- Many groups of objects can be replaced by relatively few shared objects
- The application doesn't depend on object identity

**Book example:** Tree landscape with thousands of trees. Each tree type (oak, birch, pine) is a flyweight with shared texture/shape. Position (x, y) is extrinsic state.

---

### Proxy

**Intent:** Provide a surrogate or placeholder for another object to control access to it.

**Problem it solves:** You need to control access to an object — for remote access, lazy loading, access control, logging, caching, or other cross-cutting concerns.

**Participants:**
- **Subject** — Interface shared by RealSubject and Proxy
- **RealSubject** — The actual object being proxied
- **Proxy** — Controls access to RealSubject, may create/manage it

**Proxy variants:**
- **Remote Proxy** — Represents an object in a different JVM/address space (e.g., Java RMI). The proxy handles network communication transparently
- **Virtual Proxy** — Creates expensive objects on demand. Displays a placeholder until the real object is loaded (e.g., image loading with placeholder)
- **Protection Proxy** — Controls access based on permissions (e.g., Java's dynamic Proxy with InvocationHandler checks caller rights)
- **Other variants** — Firewall proxy, caching proxy, synchronization proxy, smart reference proxy, copy-on-write proxy

**Key characteristics:**
- Proxy and RealSubject share the same interface
- Proxy holds a reference to RealSubject (or can create it)
- Proxy adds control logic before/after delegating to RealSubject
- Similar structure to Decorator, but different intent: Proxy controls access, Decorator adds behavior
- Java dynamic proxy creates proxy classes at runtime

**When to use:**
- You need a local representative for a remote object
- You want to create expensive objects only on demand
- You need to control access to the original object
- You want a smart reference (reference counting, locking, etc.)

**Book example:** Gumball machine monitoring via Remote Proxy (Java RMI). Virtual Proxy for CD cover images loading asynchronously. Protection Proxy using Java's InvocationHandler to control who can set ratings.

---

## Behavioral Patterns

Patterns that deal with communication between objects, how objects interact and
distribute responsibility.

### Strategy

**Intent:** Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

**Problem it solves:** Multiple related classes differ only in their behavior. You need different variants of an algorithm. Conditional statements for selecting desired behavior become complex.

**Participants:**
- **Strategy** — Interface common to all supported algorithms (e.g., `FlyBehavior`)
- **ConcreteStrategy** — Implements the algorithm (e.g., `FlyWithWings`, `FlyNoWay`)
- **Context** — Configured with a Strategy, delegates to it (e.g., `Duck`)

**Key characteristics:**
- Context composes a Strategy via an interface field
- Behavior can be changed at runtime via setter
- Eliminates conditional statements for selecting behavior
- Follows "encapsulate what varies" and "program to interfaces"
- Favors composition over inheritance
- Each strategy is independently testable

**When to use:**
- Many related classes differ only in behavior
- You need different variants of an algorithm
- An algorithm uses data that clients shouldn't know about
- A class defines many behaviors via conditional statements

**Book example:** SimUDuck where ducks compose FlyBehavior and QuackBehavior. MallardDuck flies with wings, RubberDuck squeaks, and behaviors can be swapped at runtime with setFlyBehavior().

---

### Observer

**Intent:** Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

**Problem it solves:** Multiple objects need to stay synchronized with another object's state. Tight coupling between the source of data and its consumers makes the system rigid.

**Participants:**
- **Subject** — Maintains list of observers, sends notifications (e.g., `WeatherData`)
- **Observer** — Interface for objects that should be notified (e.g., `Observer` with `update()`)
- **ConcreteSubject** — Stores state of interest, notifies observers when state changes
- **ConcreteObserver** — Maintains reference to ConcreteSubject, implements update (e.g., `CurrentConditionsDisplay`)

**Key characteristics:**
- Loose coupling: Subject knows only the Observer interface
- Observers can be added/removed at runtime
- **Push model** — Subject sends data with notification
- **Pull model** — Observer queries Subject for data after notification
- Subject doesn't need to know concrete observer classes
- Be careful with notification order dependencies
- Remember to unregister observers to prevent memory leaks

**When to use:**
- When a change to one object requires changing others, and you don't know how many
- When an object should notify others without making assumptions about who they are
- When you need a publish-subscribe mechanism

**Book example:** WeatherStation where WeatherData (Subject) notifies CurrentConditionsDisplay, StatisticsDisplay, and ForecastDisplay (Observers) whenever measurements change.

---

### Command

**Intent:** Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

**Problem it solves:** You need to issue requests to objects without knowing anything about the operation being requested or the receiver. You need to support undo/redo, queuing, logging.

**Participants:**
- **Command** — Interface declaring `execute()` (and optionally `undo()`)
- **ConcreteCommand** — Binds a receiver to an action (e.g., `LightOnCommand`)
- **Invoker** — Asks the command to carry out the request (e.g., `RemoteControl`)
- **Receiver** — Knows how to perform the actual work (e.g., `Light`, `Stereo`)
- **Client** — Creates commands and sets their receivers

**Key characteristics:**
- Decouples invoker from receiver
- Commands can be stored, queued, and logged
- **Undo** — Command stores previous state; `undo()` reverses `execute()`
- **Macro Command** — Command that executes a sequence of commands
- **NoCommand** (Null Object) — Placeholder command that does nothing; eliminates null checks
- Commands can be serialized for replay or remote execution

**When to use:**
- Parameterize objects with an action to perform
- Specify, queue, and execute requests at different times
- Support undo/redo functionality
- Support logging changes so they can be reapplied after a crash
- Structure a system around high-level operations built from primitives

**Book example:** Universal remote control where buttons are assigned commands. LightOnCommand, StereoOnWithCDCommand, etc. Undo button reverses last command. Party mode via MacroCommand.

---

### Template Method

**Intent:** Define the skeleton of an algorithm in a method, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps without changing the algorithm's structure.

**Problem it solves:** Two or more classes have algorithms with the same structure but different steps. Duplicating the algorithm in each class violates DRY.

**Participants:**
- **AbstractClass** — Defines the template method and abstract primitive operations (e.g., `CaffeineBeverage`)
- **ConcreteClass** — Implements the primitive operations (e.g., `Tea`, `Coffee`)

**Key characteristics:**
- Template method defines the algorithm structure, calls abstract/hook methods
- **Abstract methods** — Subclasses MUST implement these steps
- **Hook methods** — Subclasses CAN override these; default (often empty) implementation provided
- **Hollywood Principle** — "Don't call us, we'll call you." Superclass controls when subclasses are called
- Template method itself should be `final` to prevent subclass overriding
- Strategy vs Template Method: Strategy uses composition, Template Method uses inheritance

**When to use:**
- Implement the invariant parts of an algorithm once and leave variable parts to subclasses
- Common behavior among subclasses should be factored into a common class to avoid duplication
- Control subclass extensions (hooks let subclasses extend at specific points)

**Book example:** CaffeineBeverage prepareRecipe() calls boilWater(), brew(), pourInCup(), addCondiments(). Tea and Coffee implement brew() and addCondiments() differently. Hook: customerWantsCondiments().

---

### Iterator

**Intent:** Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.

**Problem it solves:** Collections have different internal structures (arrays, lists, hashtables) but clients need a uniform way to traverse them without knowing the internals.

**Participants:**
- **Iterator** — Interface for accessing and traversing elements (`hasNext()`, `next()`)
- **ConcreteIterator** — Implements Iterator for a specific aggregate
- **Aggregate** — Interface for creating an Iterator (`createIterator()`)
- **ConcreteAggregate** — Implements the Aggregate; returns appropriate ConcreteIterator

**Key characteristics:**
- Uniform traversal interface regardless of collection type
- Collection doesn't expose its internal structure
- Multiple iterators can traverse the same collection simultaneously
- Follows Single Responsibility Principle: collection manages elements, iterator manages traversal
- In Java, `java.util.Iterator` provides standard interface
- Internal vs external iterators (who controls traversal)

**When to use:**
- Access a collection's contents without exposing its internal representation
- Support multiple traversals of collections
- Provide a uniform interface for traversing different collection structures

**Book example:** Diner menu (array) and Pancake House menu (ArrayList) need a common way for a waitress to iterate. Each menu provides an Iterator, waitress uses the same loop for both.

---

### State

**Intent:** Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.

**Problem it solves:** An object's behavior depends on its state, and it must change behavior at runtime depending on that state. Large conditional statements test the current state and select behavior.

**Participants:**
- **State** — Interface defining behavior for each state (e.g., `State` with insertQuarter(), turnCrank(), etc.)
- **ConcreteState** — Each state implements behavior appropriate for that state (e.g., `HasQuarterState`, `SoldState`)
- **Context** — Maintains a current State instance, delegates behavior to it (e.g., `GumballMachine`)

**Key characteristics:**
- Eliminates large conditional blocks (switch/if-else on state)
- State transitions handled by state objects (or by context — design choice)
- Each state encapsulates its own behavior
- Similar class diagram to Strategy, but different intent:
  - Strategy: client chooses algorithm, typically configured once
  - State: transitions happen automatically based on context, behavior changes over time
- New states can be added without modifying existing state classes (Open-Closed Principle)
- Context delegates to current state for all state-dependent behavior

**When to use:**
- Object behavior depends on its state and changes at runtime
- Operations have large multipart conditional statements depending on state
- You want to make state transitions explicit

**Book example:** Gumball machine with NoQuarterState, HasQuarterState, SoldState, SoldOutState. Each state handles all actions (insert quarter, eject, turn crank, dispense) appropriately for its context.

---

### Chain of Responsibility

**Intent:** Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it.

**Problem it solves:** Multiple objects may handle a request, and the handler isn't known a priori. The set of handlers and their order should be configurable.

**Participants:**
- **Handler** — Interface defining handleRequest(); may include successor reference
- **ConcreteHandler** — Handles requests it's responsible for; forwards others to successor
- **Client** — Initiates the request to a handler in the chain

**Key characteristics:**
- Request travels along the chain until handled (or falls off the end)
- Sender doesn't know which handler will process the request
- Chain can be configured dynamically
- Each handler decides: handle or pass along
- No guarantee the request will be handled (may need a default handler)
- Reduces coupling between sender and receiver

**When to use:**
- More than one object may handle a request and the handler is not known a priori
- You want to issue a request to one of several objects without specifying the receiver explicitly
- The set of handlers should be specified dynamically

**Book example:** Email handler chain: SpamHandler → FanHandler → ComplaintHandler → NewLocationHandler. Each handler checks if it should process the email, otherwise passes it to the next handler.

---

### Interpreter

**Intent:** Given a language, define a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language.

**Problem it solves:** You have a simple language or grammar that needs to be interpreted. Each rule in the grammar can be represented as a class.

**Participants:**
- **AbstractExpression** — Interface for interpret() operation
- **TerminalExpression** — Implements interpret for terminal symbols in the grammar
- **NonterminalExpression** — Implements interpret for grammar rules (contains other expressions)
- **Context** — Contains global information for the interpreter
- **Client** — Builds the abstract syntax tree and invokes interpret

**Key characteristics:**
- Each grammar rule becomes a class
- Abstract syntax tree (AST) represents sentences in the language
- Easy to change/extend the grammar by adding new expression classes
- Complex grammars become hard to maintain (use parser generators for those)
- Works best for simple, well-defined languages

**When to use:**
- The grammar is simple (complex grammars need parser generators)
- Efficiency is not a critical concern
- You need an easy way to interpret/evaluate a language

**Book example:** Musical notation interpreter where expressions represent notes, rests, and sequences. Each grammar rule is a class with an interpret method.

---

### Mediator

**Intent:** Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly.

**Problem it solves:** Many objects communicate with many others in complex ways. Direct references create a tangled web of dependencies that's hard to understand and modify.

**Participants:**
- **Mediator** — Interface defining communication between colleague objects
- **ConcreteMediator** — Coordinates communication between colleagues; knows all colleagues
- **Colleague** — Each object communicates through the mediator rather than directly with others

**Key characteristics:**
- Centralizes complex communication and control logic
- Colleagues only know the mediator, not each other
- Simplifies object protocols (many-to-many → many-to-one)
- Mediator can become a God Object if not careful
- Promotes loose coupling between colleagues
- Trade-off: complexity moves from distributed interactions to centralized mediator

**When to use:**
- A set of objects communicate in well-defined but complex ways
- Reusing an object is difficult because it refers to many other objects
- Behavior distributed between several classes should be customizable without subclassing

**Book example:** Home automation where an alarm clock, calendar, coffee maker, and sprinkler system communicate through a mediator. Calendar event triggers alarm, which triggers coffee maker, all coordinated by the mediator.

---

### Memento

**Intent:** Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later.

**Problem it solves:** You need to implement undo, checkpoint, or rollback functionality. Saving/restoring state directly would expose internal details and violate encapsulation.

**Participants:**
- **Originator** — Object whose state needs to be saved; creates and restores from Memento
- **Memento** — Stores the internal state of the Originator; opaque to other objects
- **Caretaker** — Responsible for keeping the Memento; never examines or modifies its contents

**Key characteristics:**
- Preserves encapsulation: only Originator can access Memento's internals
- Caretaker holds mementos but doesn't know their contents
- Can store multiple mementos for multi-level undo
- May be expensive if Originator state is large
- Consider incremental changes vs full snapshots
- Originator creates memento, Caretaker stores it, Originator restores from it

**When to use:**
- A snapshot of an object's state must be saved for later restoration
- A direct interface to obtaining the state would expose implementation details
- You need to implement undo/redo, checkpoints, or transactions

**Book example:** Save game state where the game (Originator) creates a Memento of its state, the system (Caretaker) stores it, and the game can restore to any saved state later.

---

### Visitor

**Intent:** Represent an operation to be performed on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.

**Problem it solves:** You have a stable class hierarchy but need to add new operations frequently. Adding methods to each class for every new operation pollutes the interface and requires changing all classes.

**Participants:**
- **Visitor** — Interface declaring visit method for each element type
- **ConcreteVisitor** — Implements operations for each element type (e.g., `NutritionVisitor`, `PricingVisitor`)
- **Element** — Interface declaring accept(Visitor) method
- **ConcreteElement** — Implements accept by calling visitor.visit(this) (double dispatch)
- **ObjectStructure** — Collection of elements that can be iterated

**Key characteristics:**
- **Double dispatch** — Operation depends on both Visitor type AND Element type
- Element.accept(visitor) → visitor.visit(element): two method calls determine behavior
- Easy to add new operations (new Visitor class) without changing elements
- Hard to add new element types (must update all Visitors)
- Gathers related operations in a Visitor instead of spreading across element classes
- Elements must expose enough state for Visitors to work

**When to use:**
- An object structure contains many classes with differing interfaces and you want to perform operations that depend on concrete classes
- Many distinct/unrelated operations need to be performed on objects in a structure
- The classes defining the structure rarely change, but you often want to define new operations

**Book example:** Menu items with NutritionVisitor and PricingVisitor. Each visitor traverses menu items, computing nutritional info or prices without modifying the MenuItem classes.

---

## Compound Patterns

### MVC (Model-View-Controller)

**Intent:** Separate an application into three interconnected components to separate internal representations from the ways information is presented and accepted by the user.

**Patterns used:**
- **Observer** — Model notifies Views when state changes
- **Strategy** — View uses Controller as its strategy for handling user input
- **Composite** — View hierarchy is a composite structure (panels contain buttons, labels, etc.)

**Participants:**
- **Model** — Application data and business logic; notifies observers (views) of changes
- **View** — Renders the model's data; observes model for updates; delegates user actions to controller
- **Controller** — Takes user input from view, interprets it, and manipulates the model; acts as the strategy for the view

**Key characteristics:**
- Model is completely independent of View and Controller
- Views can be swapped without changing the Model
- Controllers can be swapped to change input handling behavior
- Multiple Views can observe the same Model simultaneously
- **Model 2 (Web MVC)** — Adapted for web: Controller is a servlet, View is a JSP/template, Model is a POJO/bean
- Clean separation of concerns enables independent testing and development

**When to use:**
- Building interactive applications where presentation and data should be decoupled
- Multiple views of the same data are needed
- User interface needs to be easily changeable or replaceable

**Book example:** DJ beat controller where BeatModel (Model) tracks BPM and notifies DJView (View) of changes. BeatController (Controller) handles user interactions like setting BPM and starting/stopping beats.
