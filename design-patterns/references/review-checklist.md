# Design Patterns — Code Review Checklist

Systematic checklist for reviewing code against GoF design patterns and OO design
principles from *Head First Design Patterns*.

---

## 1. OO Design Principles

- [ ] **Encapsulate what varies** — Are parts that change separated from parts that stay the same? Look for hardcoded behaviors that should be extracted
- [ ] **Favor composition over inheritance** — Is HAS-A used where IS-A creates rigidity? Are behaviors composed rather than inherited?
- [ ] **Program to interfaces** — Does code depend on abstractions? Are variables declared as interface/abstract types, not concrete?
- [ ] **Loosely coupled** — Do interacting objects know as little as possible about each other? Can objects be changed independently?
- [ ] **Open-Closed Principle** — Is the design open for extension, closed for modification? Can new behavior be added without changing existing code?
- [ ] **Dependency Inversion** — Do high-level modules depend on abstractions? Are concrete classes instantiated through factories or DI?
- [ ] **Least Knowledge (Law of Demeter)** — Do methods only call methods on: (a) the object itself, (b) objects passed as parameters, (c) objects the method creates, (d) component objects? No method chains like a.getB().getC().doThing()
- [ ] **Hollywood Principle** — Do high-level components control flow? Do subclasses/low-level components avoid calling up into high-level components?
- [ ] **Single Responsibility** — Does each class have one reason to change? Are responsibilities cleanly separated?

## 2. Creational Pattern Usage

### Factory Patterns
- [ ] **No direct instantiation of concrete classes in client code** — Are `new ConcreteClass()` calls isolated in factories?
- [ ] **Factory Method applied correctly** — Does the creator have a factory method that subclasses override? Is the return type an abstraction?
- [ ] **Abstract Factory for families** — When related objects must be created together, does a factory ensure compatibility?
- [ ] **Simple Factory distinguished** — Is a Simple Factory (not a true pattern) used where a full Factory Method isn't needed? Not over-engineered?

### Singleton
- [ ] **Genuinely needs to be singleton** — Is there a real reason for exactly one instance, or is it just convenient global access?
- [ ] **Thread-safe** — Is the singleton implementation thread-safe (eager init, synchronized, double-checked locking, or enum)?
- [ ] **Not abused as global state** — Is it holding application state that should be managed differently?
- [ ] **Testable** — Can the singleton be mocked or replaced in tests?

### Builder
- [ ] **Complex construction** — Is step-by-step construction warranted, or would a simple constructor suffice?
- [ ] **Director separates algorithm** — Is the build algorithm separated from the representation?
- [ ] **Fluent interface** — If using method chaining, do methods return the builder for readability?

### Prototype
- [ ] **Clone correctness** — Is deep copy used where needed? Are mutable references properly cloned?
- [ ] **Registry management** — If using a prototype registry, are prototypes properly managed?

## 3. Structural Pattern Usage

### Adapter
- [ ] **Interface translation correct** — Does the adapter properly translate all Target methods to Adaptee calls?
- [ ] **Object adapter preferred** — Is composition used rather than multiple inheritance (unless required)?
- [ ] **Not confused with Facade** — Adapter changes interface; Facade simplifies interface. Is the right one used?

### Decorator
- [ ] **Same interface** — Do decorators implement the same interface/extend the same abstract class as the component?
- [ ] **Wrapping is transparent** — Can decorated objects be used anywhere the original can?
- [ ] **Not overused** — Is the number of decorator layers manageable? Can the design be understood?
- [ ] **Open-Closed Principle honored** — Are new behaviors added via decorators rather than modifying existing classes?
- [ ] **Type checking avoided** — Code doesn't rely on the concrete type of the component (instanceof breaks with decorators)

### Facade
- [ ] **Simplification achieved** — Does the facade genuinely simplify client interaction with the subsystem?
- [ ] **Subsystem still accessible** — Facade doesn't hide the subsystem; power users can still access it directly
- [ ] **Not too many facades** — Facade shouldn't become a God Class. Multiple focused facades are better than one massive one
- [ ] **Law of Demeter respected** — Does client code only talk to the facade, not reach through it into subsystem objects?

### Composite
- [ ] **Uniform interface** — Do leaves and composites implement the same Component interface?
- [ ] **Tree structure correct** — Is the parent-child relationship properly maintained?
- [ ] **Leaf operations handled** — Do leaves properly handle operations that don't apply (throw exception or no-op)?
- [ ] **Transparency vs safety trade-off** — Is the choice between uniform interface and type-safe separate interfaces deliberate?

### Proxy
- [ ] **Same interface** — Does the proxy implement the same interface as the real subject?
- [ ] **Proxy type appropriate** — Is the right proxy variant used (remote, virtual, protection)?
- [ ] **Not confused with Decorator** — Proxy controls access; Decorator adds behavior. Is the intent correct?
- [ ] **Virtual proxy lazy loading** — Does the virtual proxy actually defer expensive creation until needed?
- [ ] **Protection proxy access rules** — Are access control checks implemented correctly?

### Bridge
- [ ] **Two dimensions identified** — Is there a genuine need for two independent hierarchies?
- [ ] **Abstraction and implementation vary independently** — Can you add new abstractions without touching implementations and vice versa?
- [ ] **Not over-engineered** — If there's only one implementation, Bridge may be unnecessary

### Flyweight
- [ ] **Intrinsic/extrinsic split correct** — Is shared state truly context-independent? Is extrinsic state truly per-instance?
- [ ] **Immutable flyweights** — Are flyweight objects immutable (since they're shared)?
- [ ] **Factory manages sharing** — Does a factory ensure flyweights are properly shared and not duplicated?

## 4. Behavioral Pattern Usage

### Strategy
- [ ] **Behavior encapsulated** — Is the varying behavior behind an interface, not in conditionals?
- [ ] **Runtime swappable** — Can the strategy be changed at runtime? Is there a setter?
- [ ] **Context delegates properly** — Does the context forward behavior to the strategy rather than implementing it?
- [ ] **Not confused with State** — Strategy is chosen by client; State transitions happen internally

### Observer
- [ ] **Subject tracks observers** — Does the subject maintain a list of observers and notify them on change?
- [ ] **Loose coupling** — Does the subject know only the Observer interface, not concrete observer types?
- [ ] **Push vs pull model** — Is the update model (push data vs pull data) appropriate for the use case?
- [ ] **Unregistration supported** — Can observers unsubscribe? Are there memory leaks from forgotten registrations?
- [ ] **Notification order** — Is the code safe regardless of notification order?

### Command
- [ ] **Request encapsulated** — Is the request a first-class object with execute()?
- [ ] **Invoker decoupled from receiver** — Does the invoker only know the Command interface?
- [ ] **Undo supported (if needed)** — Does the command store enough state for undo()? Is previous state saved before execute()?
- [ ] **Null Object used** — Is NoCommand or similar used instead of null checks?
- [ ] **Macro commands** — If sequences of commands are needed, is MacroCommand implemented?

### Template Method
- [ ] **Algorithm in base class** — Is the template method final (or equivalent) so subclasses can't change the structure?
- [ ] **Abstract vs hook methods** — Are mandatory steps abstract and optional steps hooks with defaults?
- [ ] **Hollywood Principle** — Does the base class call subclass methods, not the other way around?
- [ ] **Not confused with Strategy** — Template Method uses inheritance; Strategy uses composition. Is the right one used?

### Iterator
- [ ] **Uniform traversal** — Do different collections provide the same Iterator interface?
- [ ] **Internal structure hidden** — Does the client not need to know if it's an array, list, or other structure?
- [ ] **Single Responsibility** — Is traversal logic separated from collection management?
- [ ] **Standard library used** — Are language-standard iterators (java.util.Iterator, Python's __iter__) used where appropriate?

### State
- [ ] **States as objects** — Is each state a class implementing a common State interface?
- [ ] **Context delegates** — Does the context forward all state-dependent behavior to the current state?
- [ ] **Transitions correct** — Are state transitions handled properly? Is each transition in the right state class?
- [ ] **Conditionals eliminated** — Are switch/if-else chains on state replaced with polymorphic state objects?
- [ ] **Not confused with Strategy** — State transitions happen automatically; Strategy is explicitly chosen by client

### Chain of Responsibility
- [ ] **Chain properly linked** — Does each handler have a reference to the next handler?
- [ ] **Default handler exists** — Is there a fallback if no handler processes the request?
- [ ] **Single responsibility per handler** — Does each handler check one condition?

### Visitor
- [ ] **Double dispatch correct** — Does element.accept(visitor) call visitor.visit(this)?
- [ ] **All element types covered** — Does the Visitor interface have a visit method for each ConcreteElement?
- [ ] **Trade-off acknowledged** — Adding new elements is hard (all visitors need updating). Is the element hierarchy stable?

### Mediator
- [ ] **Colleagues decoupled** — Do colleagues communicate only through the mediator?
- [ ] **Mediator not a God Object** — Is the mediator focused, not accumulating all system logic?

### Memento
- [ ] **Encapsulation preserved** — Does only the Originator access Memento internals?
- [ ] **Caretaker doesn't peek** — Does the Caretaker store but not examine Memento contents?
- [ ] **Memory managed** — Are old mementos cleaned up to prevent memory issues?

## 5. Compound Pattern Checks

### MVC
- [ ] **Model independent** — Does the Model know nothing about View or Controller?
- [ ] **Observer applied** — Does the Model notify Views of changes?
- [ ] **Strategy applied** — Is the Controller a swappable strategy for the View?
- [ ] **Composite applied** — Is the View hierarchy a composite structure?
- [ ] **Separation clean** — Is there zero business logic in Views or Controllers?

---

## Quick Review Workflow

1. **Scan for code smells** — Large conditionals, deep inheritance, duplicated algorithm structure, tight coupling to concrete classes, method chains
2. **Identify existing patterns** — What patterns are already in use, intentionally or accidentally?
3. **Check pattern correctness** — Are all participants present? Are responsibilities assigned correctly?
4. **Evaluate principles** — Walk through all nine OO design principles. Which are violated?
5. **Recommend patterns** — Where could a pattern reduce complexity, improve extensibility, or eliminate duplication?
6. **Prioritize** — Rank findings by impact: critical design flaws → pattern opportunities → polish

## Severity Levels

| Severity | Description | Example |
|----------|------------|---------|
| **Critical** | Fundamental design problems, high coupling, untestable code | Massive conditionals that should be Strategy/State, God class, no encapsulation |
| **High** | Incorrect pattern usage, missed key pattern opportunity | Decorator without same interface, Observer without unsubscribe, Singleton abuse |
| **Medium** | Pattern improvement opportunities | Could use Factory instead of direct instantiation, Template Method for duplicate algorithms |
| **Low** | Polish and refinements | Better naming for pattern roles, missing Null Object, documentation of pattern intent |
