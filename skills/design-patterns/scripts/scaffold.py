#!/usr/bin/env python3
"""
GoF Pattern Scaffold — generates complete, idiomatic boilerplate for design patterns.
Usage: python scaffold.py <pattern> <ClassName> [--lang python|kotlin|java]

Supported patterns: strategy, observer, factory, decorator, command, singleton
"""

import argparse
import sys
from pathlib import Path
from string import Template

# ---------------------------------------------------------------------------
# Pattern templates per language
# ---------------------------------------------------------------------------

PATTERNS: dict[str, dict] = {}

# ---- STRATEGY --------------------------------------------------------------
PATTERNS["strategy"] = {
    "python": Template('''\
#!/usr/bin/env python3
"""Strategy pattern — ${Name}."""
from abc import ABC, abstractmethod


# Interface
class ${Name}Strategy(ABC):
    @abstractmethod
    def execute(self, data: str) -> str: ...


# Concrete strategy A
class ${Name}StrategyA(${Name}Strategy):
    def execute(self, data: str) -> str:
        return f"[StrategyA] {data.upper()}"


# Concrete strategy B
class ${Name}StrategyB(${Name}Strategy):
    def execute(self, data: str) -> str:
        return f"[StrategyB] {data[::-1]}"


# Context
class ${Name}Context:
    def __init__(self, strategy: ${Name}Strategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: ${Name}Strategy) -> None:
        self._strategy = strategy

    def run(self, data: str) -> str:
        return self._strategy.execute(data)


# Usage example
if __name__ == "__main__":
    ctx = ${Name}Context(${Name}StrategyA())
    print(ctx.run("hello"))          # [StrategyA] HELLO
    ctx.set_strategy(${Name}StrategyB())
    print(ctx.run("hello"))          # [StrategyB] olleh
'''),
    "kotlin": Template('''\
package com.example.patterns

// Interface
interface ${Name}Strategy {
    fun execute(data: String): String
}

// Concrete A
class ${Name}StrategyA : ${Name}Strategy {
    override fun execute(data: String) = "[StrategyA] ${dollar}{data.uppercase()}"
}

// Concrete B
class ${Name}StrategyB : ${Name}Strategy {
    override fun execute(data: String) = "[StrategyB] ${dollar}{data.reversed()}"
}

// Context
class ${Name}Context(private var strategy: ${Name}Strategy) {
    fun setStrategy(s: ${Name}Strategy) { strategy = s }
    fun run(data: String): String = strategy.execute(data)
}

fun main() {
    val ctx = ${Name}Context(${Name}StrategyA())
    println(ctx.run("hello"))
    ctx.setStrategy(${Name}StrategyB())
    println(ctx.run("hello"))
}
'''),
    "java": Template('''\
package com.example.patterns;

// Interface
public interface ${Name}Strategy {
    String execute(String data);
}

// Concrete A
class ${Name}StrategyA implements ${Name}Strategy {
    public String execute(String data) { return "[StrategyA] " + data.toUpperCase(); }
}

// Concrete B
class ${Name}StrategyB implements ${Name}Strategy {
    public String execute(String data) {
        return "[StrategyB] " + new StringBuilder(data).reverse();
    }
}

// Context
class ${Name}Context {
    private ${Name}Strategy strategy;
    public ${Name}Context(${Name}Strategy s) { this.strategy = s; }
    public void setStrategy(${Name}Strategy s) { this.strategy = s; }
    public String run(String data) { return strategy.execute(data); }

    public static void main(String[] args) {
        var ctx = new ${Name}Context(new ${Name}StrategyA());
        System.out.println(ctx.run("hello"));
        ctx.setStrategy(new ${Name}StrategyB());
        System.out.println(ctx.run("hello"));
    }
}
'''),
}

# ---- OBSERVER --------------------------------------------------------------
PATTERNS["observer"] = {
    "python": Template('''\
#!/usr/bin/env python3
"""Observer pattern — ${Name}."""
from abc import ABC, abstractmethod
from typing import List


class ${Name}Observer(ABC):
    @abstractmethod
    def update(self, event: str, payload: object) -> None: ...


class ${Name}Subject:
    def __init__(self) -> None:
        self._observers: List[${Name}Observer] = []

    def subscribe(self, obs: ${Name}Observer) -> None:
        self._observers.append(obs)

    def unsubscribe(self, obs: ${Name}Observer) -> None:
        self._observers.remove(obs)

    def notify(self, event: str, payload: object = None) -> None:
        for obs in self._observers:
            obs.update(event, payload)


class ${Name}LogObserver(${Name}Observer):
    def update(self, event: str, payload: object) -> None:
        print(f"[LOG] event={event!r} payload={payload!r}")


class ${Name}MetricsObserver(${Name}Observer):
    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    def update(self, event: str, payload: object) -> None:
        self.counts[event] = self.counts.get(event, 0) + 1
        print(f"[METRICS] {event} count={self.counts[event]}")


if __name__ == "__main__":
    subject = ${Name}Subject()
    subject.subscribe(${Name}LogObserver())
    metrics = ${Name}MetricsObserver()
    subject.subscribe(metrics)
    subject.notify("created", {"id": 1})
    subject.notify("updated", {"id": 1, "field": "name"})
    subject.notify("created", {"id": 2})
'''),
    "kotlin": Template('''\
package com.example.patterns

interface ${Name}Observer {
    fun update(event: String, payload: Any?)
}

class ${Name}Subject {
    private val observers = mutableListOf<${Name}Observer>()
    fun subscribe(o: ${Name}Observer) { observers.add(o) }
    fun unsubscribe(o: ${Name}Observer) { observers.remove(o) }
    fun notify(event: String, payload: Any? = null) =
        observers.forEach { it.update(event, payload) }
}

class ${Name}LogObserver : ${Name}Observer {
    override fun update(event: String, payload: Any?) =
        println("[LOG] event=$event payload=$payload")
}

class ${Name}MetricsObserver : ${Name}Observer {
    private val counts = mutableMapOf<String, Int>()
    override fun update(event: String, payload: Any?) {
        counts[event] = (counts[event] ?: 0) + 1
        println("[METRICS] $event count=${dollar}{counts[event]}")
    }
}

fun main() {
    val subject = ${Name}Subject()
    subject.subscribe(${Name}LogObserver())
    subject.subscribe(${Name}MetricsObserver())
    subject.notify("created", mapOf("id" to 1))
    subject.notify("updated", mapOf("id" to 1))
}
'''),
    "java": Template('''\
package com.example.patterns;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public interface ${Name}Observer {
    void update(String event, Object payload);
}

class ${Name}Subject {
    private final List<${Name}Observer> observers = new ArrayList<>();
    public void subscribe(${Name}Observer o) { observers.add(o); }
    public void unsubscribe(${Name}Observer o) { observers.remove(o); }
    public void notify(String event, Object payload) {
        observers.forEach(o -> o.update(event, payload));
    }
}

class ${Name}LogObserver implements ${Name}Observer {
    public void update(String event, Object payload) {
        System.out.printf("[LOG] event=%s payload=%s%n", event, payload);
    }
}

class ${Name}MetricsObserver implements ${Name}Observer {
    private final Map<String, Integer> counts = new HashMap<>();
    public void update(String event, Object payload) {
        counts.merge(event, 1, Integer::sum);
        System.out.printf("[METRICS] %s count=%d%n", event, counts.get(event));
    }
    public static void main(String[] args) {
        var s = new ${Name}Subject();
        s.subscribe(new ${Name}LogObserver());
        s.subscribe(new ${Name}MetricsObserver());
        s.notify("created", Map.of("id", 1));
        s.notify("updated", Map.of("id", 1));
    }
}
'''),
}

# ---- FACTORY ---------------------------------------------------------------
PATTERNS["factory"] = {
    "python": Template('''\
#!/usr/bin/env python3
"""Factory Method pattern — ${Name}."""
from abc import ABC, abstractmethod


class ${Name}Product(ABC):
    @abstractmethod
    def operation(self) -> str: ...


class ${Name}ConcreteProductA(${Name}Product):
    def operation(self) -> str:
        return "${Name}ConcreteProductA result"


class ${Name}ConcreteProductB(${Name}Product):
    def operation(self) -> str:
        return "${Name}ConcreteProductB result"


class ${Name}Creator(ABC):
    @abstractmethod
    def create_product(self) -> ${Name}Product: ...

    def deliver(self) -> str:
        product = self.create_product()
        return f"Creator: {product.operation()}"


class ${Name}CreatorA(${Name}Creator):
    def create_product(self) -> ${Name}Product:
        return ${Name}ConcreteProductA()


class ${Name}CreatorB(${Name}Creator):
    def create_product(self) -> ${Name}Product:
        return ${Name}ConcreteProductB()


def client(creator: ${Name}Creator) -> None:
    print(creator.deliver())


if __name__ == "__main__":
    client(${Name}CreatorA())
    client(${Name}CreatorB())
'''),
    "kotlin": Template('''\
package com.example.patterns

interface ${Name}Product { fun operation(): String }

class ${Name}ProductA : ${Name}Product {
    override fun operation() = "${Name}ProductA result"
}
class ${Name}ProductB : ${Name}Product {
    override fun operation() = "${Name}ProductB result"
}

abstract class ${Name}Creator {
    abstract fun createProduct(): ${Name}Product
    fun deliver() = "Creator: ${dollar}{createProduct().operation()}"
}

class ${Name}CreatorA : ${Name}Creator() {
    override fun createProduct() = ${Name}ProductA()
}
class ${Name}CreatorB : ${Name}Creator() {
    override fun createProduct() = ${Name}ProductB()
}

fun main() {
    println(${Name}CreatorA().deliver())
    println(${Name}CreatorB().deliver())
}
'''),
    "java": Template('''\
package com.example.patterns;

public interface ${Name}Product { String operation(); }

class ${Name}ProductA implements ${Name}Product {
    public String operation() { return "${Name}ProductA result"; }
}
class ${Name}ProductB implements ${Name}Product {
    public String operation() { return "${Name}ProductB result"; }
}

abstract class ${Name}Creator {
    public abstract ${Name}Product createProduct();
    public String deliver() { return "Creator: " + createProduct().operation(); }
}

class ${Name}CreatorA extends ${Name}Creator {
    public ${Name}Product createProduct() { return new ${Name}ProductA(); }
}
class ${Name}CreatorB extends ${Name}Creator {
    public ${Name}Product createProduct() { return new ${Name}ProductB(); }
    public static void main(String[] args) {
        System.out.println(new ${Name}CreatorA().deliver());
        System.out.println(new ${Name}CreatorB().deliver());
    }
}
'''),
}

# ---- DECORATOR -------------------------------------------------------------
PATTERNS["decorator"] = {
    "python": Template('''\
#!/usr/bin/env python3
"""Decorator pattern — ${Name}."""
from abc import ABC, abstractmethod


class ${Name}Component(ABC):
    @abstractmethod
    def execute(self) -> str: ...


class ${Name}ConcreteComponent(${Name}Component):
    def execute(self) -> str:
        return "base-result"


class ${Name}Decorator(${Name}Component, ABC):
    def __init__(self, wrapped: ${Name}Component) -> None:
        self._wrapped = wrapped

    def execute(self) -> str:
        return self._wrapped.execute()


class ${Name}LoggingDecorator(${Name}Decorator):
    def execute(self) -> str:
        result = super().execute()
        print(f"[LOG] result={result!r}")
        return result


class ${Name}CachingDecorator(${Name}Decorator):
    def __init__(self, wrapped: ${Name}Component) -> None:
        super().__init__(wrapped)
        self._cache: str | None = None

    def execute(self) -> str:
        if self._cache is None:
            self._cache = super().execute()
            print("[CACHE] miss — computed")
        else:
            print("[CACHE] hit")
        return self._cache


if __name__ == "__main__":
    base = ${Name}ConcreteComponent()
    cached = ${Name}CachingDecorator(base)
    logged = ${Name}LoggingDecorator(cached)
    print(logged.execute())
    print(logged.execute())  # second call: cache hit
'''),
    "kotlin": Template('''\
package com.example.patterns

interface ${Name}Component { fun execute(): String }

class ${Name}ConcreteComponent : ${Name}Component {
    override fun execute() = "base-result"
}

open class ${Name}Decorator(private val wrapped: ${Name}Component) : ${Name}Component {
    override fun execute() = wrapped.execute()
}

class ${Name}LoggingDecorator(wrapped: ${Name}Component) : ${Name}Decorator(wrapped) {
    override fun execute(): String {
        val r = super.execute()
        println("[LOG] result=$r")
        return r
    }
}

class ${Name}CachingDecorator(wrapped: ${Name}Component) : ${Name}Decorator(wrapped) {
    private var cache: String? = null
    override fun execute(): String {
        if (cache == null) { cache = super.execute(); println("[CACHE] miss") }
        else println("[CACHE] hit")
        return cache!!
    }
}

fun main() {
    val comp = ${Name}LoggingDecorator(${Name}CachingDecorator(${Name}ConcreteComponent()))
    println(comp.execute())
    println(comp.execute())
}
'''),
    "java": Template('''\
package com.example.patterns;

public interface ${Name}Component { String execute(); }

class ${Name}ConcreteComponent implements ${Name}Component {
    public String execute() { return "base-result"; }
}

abstract class ${Name}Decorator implements ${Name}Component {
    protected final ${Name}Component wrapped;
    protected ${Name}Decorator(${Name}Component wrapped) { this.wrapped = wrapped; }
    public String execute() { return wrapped.execute(); }
}

class ${Name}LoggingDecorator extends ${Name}Decorator {
    ${Name}LoggingDecorator(${Name}Component w) { super(w); }
    public String execute() {
        String r = super.execute();
        System.out.println("[LOG] result=" + r);
        return r;
    }
}

class ${Name}CachingDecorator extends ${Name}Decorator {
    private String cache;
    ${Name}CachingDecorator(${Name}Component w) { super(w); }
    public String execute() {
        if (cache == null) { cache = super.execute(); System.out.println("[CACHE] miss"); }
        else System.out.println("[CACHE] hit");
        return cache;
    }
    public static void main(String[] args) {
        var c = new ${Name}LoggingDecorator(new ${Name}CachingDecorator(new ${Name}ConcreteComponent()));
        System.out.println(c.execute());
        System.out.println(c.execute());
    }
}
'''),
}

# ---- COMMAND ---------------------------------------------------------------
PATTERNS["command"] = {
    "python": Template('''\
#!/usr/bin/env python3
"""Command pattern — ${Name}."""
from abc import ABC, abstractmethod
from typing import List


class ${Name}Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


class ${Name}Receiver:
    def __init__(self) -> None:
        self.state: List[str] = []

    def add(self, item: str) -> None:
        self.state.append(item)
        print(f"Added {item!r}. State: {self.state}")

    def remove(self, item: str) -> None:
        self.state.remove(item)
        print(f"Removed {item!r}. State: {self.state}")


class ${Name}AddCommand(${Name}Command):
    def __init__(self, receiver: ${Name}Receiver, item: str) -> None:
        self._receiver = receiver
        self._item = item

    def execute(self) -> None:
        self._receiver.add(self._item)

    def undo(self) -> None:
        self._receiver.remove(self._item)


class ${Name}Invoker:
    def __init__(self) -> None:
        self._history: List[${Name}Command] = []

    def run(self, cmd: ${Name}Command) -> None:
        cmd.execute()
        self._history.append(cmd)

    def undo_last(self) -> None:
        if self._history:
            self._history.pop().undo()


if __name__ == "__main__":
    receiver = ${Name}Receiver()
    invoker = ${Name}Invoker()
    invoker.run(${Name}AddCommand(receiver, "apple"))
    invoker.run(${Name}AddCommand(receiver, "banana"))
    invoker.undo_last()
'''),
    "kotlin": Template('''\
package com.example.patterns

interface ${Name}Command { fun execute(); fun undo() }

class ${Name}Receiver {
    val state = mutableListOf<String>()
    fun add(item: String) { state.add(item); println("Added $item. State=$state") }
    fun remove(item: String) { state.remove(item); println("Removed $item. State=$state") }
}

class ${Name}AddCommand(private val r: ${Name}Receiver, private val item: String) : ${Name}Command {
    override fun execute() = r.add(item)
    override fun undo() = r.remove(item)
}

class ${Name}Invoker {
    private val history = mutableListOf<${Name}Command>()
    fun run(cmd: ${Name}Command) { cmd.execute(); history.add(cmd) }
    fun undoLast() { history.removeLastOrNull()?.undo() }
}

fun main() {
    val r = ${Name}Receiver(); val inv = ${Name}Invoker()
    inv.run(${Name}AddCommand(r, "apple"))
    inv.run(${Name}AddCommand(r, "banana"))
    inv.undoLast()
}
'''),
    "java": Template('''\
package com.example.patterns;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

public interface ${Name}Command { void execute(); void undo(); }

class ${Name}Receiver {
    List<String> state = new ArrayList<>();
    void add(String i) { state.add(i); System.out.println("Added " + i + " state=" + state); }
    void remove(String i) { state.remove(i); System.out.println("Removed " + i + " state=" + state); }
}

class ${Name}AddCommand implements ${Name}Command {
    private final ${Name}Receiver r; private final String item;
    ${Name}AddCommand(${Name}Receiver r, String item) { this.r = r; this.item = item; }
    public void execute() { r.add(item); }
    public void undo() { r.remove(item); }
}

class ${Name}Invoker {
    private final Deque<${Name}Command> history = new ArrayDeque<>();
    public void run(${Name}Command c) { c.execute(); history.push(c); }
    public void undoLast() { if (!history.isEmpty()) history.pop().undo(); }
    public static void main(String[] args) {
        var r = new ${Name}Receiver(); var inv = new ${Name}Invoker();
        inv.run(new ${Name}AddCommand(r, "apple"));
        inv.run(new ${Name}AddCommand(r, "banana"));
        inv.undoLast();
    }
}
'''),
}

# ---- SINGLETON -------------------------------------------------------------
PATTERNS["singleton"] = {
    "python": Template('''\
#!/usr/bin/env python3
"""Singleton pattern — ${Name}.

WARNING: Singleton is heavily overused. Prefer dependency injection wherever
possible. Use this pattern only for truly process-wide unique resources such
as a logging registry or a hardware interface.
"""
import threading


class ${Name}(metaclass=type):
    _instance: "${Name} | None" = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "${Name}":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._data: dict = {}

    # --- public API ---
    def set(self, key: str, value: object) -> None:
        self._data[key] = value

    def get(self, key: str) -> object:
        return self._data.get(key)


# Alternative: module-level instance (simpler, idiomatic Python)
class _${Name}Impl:
    def __init__(self) -> None:
        self._data: dict = {}
    def set(self, key: str, value: object) -> None: self._data[key] = value
    def get(self, key: str) -> object: return self._data.get(key)

# Prefer this over the class-based singleton above
${lname}_instance = _${Name}Impl()


if __name__ == "__main__":
    a = ${Name}()
    b = ${Name}()
    a.set("x", 42)
    assert b.get("x") == 42, "Must be same instance"
    assert a is b
    print("Singleton check passed — a is b:", a is b)
'''),
    "kotlin": Template('''\
package com.example.patterns

// Kotlin object declaration is the idiomatic singleton.
// WARNING: Hard to mock in tests — prefer constructor injection.
object ${Name} {
    private val data = mutableMapOf<String, Any?>()
    fun set(key: String, value: Any?) { data[key] = value }
    fun get(key: String): Any? = data[key]
}

fun main() {
    ${Name}.set("x", 42)
    println("x = ${dollar}{${Name}.get("x")}")
}
'''),
    "java": Template('''\
package com.example.patterns;
import java.util.HashMap;
import java.util.Map;

/**
 * Thread-safe lazy singleton via initialization-on-demand holder.
 * WARNING: Singleton is frequently overused; prefer dependency injection.
 */
public final class ${Name} {
    private final Map<String, Object> data = new HashMap<>();

    private ${Name}() {}

    private static final class Holder {
        private static final ${Name} INSTANCE = new ${Name}();
    }

    public static ${Name} getInstance() { return Holder.INSTANCE; }

    public void set(String key, Object value) { data.put(key, value); }
    public Object get(String key) { return data.get(key); }

    public static void main(String[] args) {
        ${Name}.getInstance().set("x", 42);
        System.out.println("x = " + ${Name}.getInstance().get("x"));
        System.out.println("same? " + (${Name}.getInstance() == ${Name}.getInstance()));
    }
}
'''),
}

SINGLETON_WARNING = """\
WARNING: You generated a Singleton. Effective Design Patterns cautions that
Singleton is the most overused pattern in the GoF catalogue. Problems include:

  - Global mutable state makes code hard to test and reason about.
  - Hidden dependencies violate the explicit-dependencies principle.
  - Concurrency issues arise when state is mutated from multiple threads.

Consider instead:
  - Dependency Injection: pass the shared object as a constructor parameter.
  - Module-level instance (Python): a single module import is naturally unique.
  - IoC containers (Spring, Guice, Hilt): manage lifetime explicitly.

Use Singleton only for truly process-wide resources with no reasonable
alternative (e.g., a hardware driver, a logging sink, an OS-level handle).
"""

EXT = {"python": "py", "kotlin": "kt", "java": "java"}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  Created: {path}")


def scaffold(pattern: str, class_name: str, lang: str, output_dir: Path) -> None:
    if pattern == "singleton":
        print("\n" + "=" * 70)
        print(SINGLETON_WARNING.strip())
        print("=" * 70 + "\n")

    lang_templates = PATTERNS[pattern]
    if lang not in lang_templates:
        print(f"ERROR: lang '{lang}' not supported for pattern '{pattern}'.", file=sys.stderr)
        sys.exit(1)

    tmpl = lang_templates[lang]
    ext = EXT[lang]
    filename = f"{class_name}_{pattern}.{ext}"
    ctx = {"Name": class_name, "lname": class_name.lower(), "dollar": "$"}
    content = tmpl.substitute(ctx)
    write(output_dir / filename, content)

    print(f"\nGenerated {pattern} pattern for '{class_name}' ({lang}): {output_dir / filename}")
    print("\nNext steps:")
    print(f"  1. Rename {class_name}Strategy/Observer/etc. to match your domain.")
    print(f"  2. Replace the placeholder execute() logic with real behaviour.")
    print(f"  3. Wire into your application via dependency injection.\n")


def main() -> None:
    supported = sorted(PATTERNS.keys())
    parser = argparse.ArgumentParser(
        description="Scaffold GoF design pattern boilerplate."
    )
    parser.add_argument("pattern", choices=supported, help=f"Pattern: {', '.join(supported)}")
    parser.add_argument("class_name", metavar="ClassName", help="Base name for generated classes")
    parser.add_argument("--lang", choices=["python", "kotlin", "java"], default="python")
    parser.add_argument("--output-dir", default=".", type=Path)
    args = parser.parse_args()

    if not args.class_name[0].isupper():
        print(f"ERROR: ClassName should be PascalCase (got '{args.class_name}').", file=sys.stderr)
        sys.exit(1)

    scaffold(args.pattern, args.class_name, args.lang, args.output_dir)


if __name__ == "__main__":
    main()
