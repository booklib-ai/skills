#!/usr/bin/env python3
"""
DDD Scaffold — generates aggregate building blocks for a bounded context.
Usage: python scaffold.py <AggregateName> [--lang python|kotlin|java] [--output-dir ./]
"""

import argparse
import sys
from pathlib import Path
from string import Template

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

PYTHON_AGGREGATE = Template('''\
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from .${name}Id import ${name}Id
from .${name}Events import ${name}Created, ${name}Event


@dataclass
class ${name}:
    """Aggregate root for ${name}."""

    id: ${name}Id
    _events: List[${name}Event] = field(default_factory=list, init=False, repr=False)

    # ------------------------------------------------------------------
    # Factory method — the only sanctioned way to create a ${name}.
    # ------------------------------------------------------------------
    @classmethod
    def create(cls, id: ${name}Id, **kwargs) -> "${name}":
        instance = cls(id=id)
        instance._check_invariants()
        instance._record(${name}Created(aggregate_id=id))
        return instance

    # ------------------------------------------------------------------
    # Commands — each mutates state and records an event.
    # ------------------------------------------------------------------

    # def rename(self, new_name: str) -> None:
    #     if not new_name.strip():
    #         raise ValueError("Name must not be blank.")
    #     self.name = new_name
    #     self._record(${name}Renamed(aggregate_id=self.id, name=new_name))

    # ------------------------------------------------------------------
    # Domain events
    # ------------------------------------------------------------------
    def pull_events(self) -> List[${name}Event]:
        """Return and clear pending domain events."""
        events, self._events = self._events, []
        return events

    def _record(self, event: ${name}Event) -> None:
        self._events.append(event)

    # ------------------------------------------------------------------
    # Invariants
    # ------------------------------------------------------------------
    def _check_invariants(self) -> None:
        """Raise if the aggregate is in an invalid state."""
        if self.id is None:
            raise ValueError("${name} must have an ID.")
''')

PYTHON_ID = Template('''\
from __future__ import annotations
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class ${name}Id:
    """Value Object — identity of a ${name} aggregate."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("${name}Id must not be blank.")

    @classmethod
    def generate(cls) -> "${name}Id":
        return cls(value=str(uuid.uuid4()))

    @classmethod
    def from_string(cls, raw: str) -> "${name}Id":
        return cls(value=raw)

    def __str__(self) -> str:
        return self.value
''')

PYTHON_REPOSITORY = Template('''\
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from .${name}Id import ${name}Id
from .${name} import ${name}


class ${name}Repository(ABC):
    """Port (interface) for ${name} persistence.

    Concrete adapters live in the infrastructure layer.
    """

    @abstractmethod
    def find_by_id(self, id: ${name}Id) -> Optional[${name}]:
        """Return the aggregate or None if not found."""

    @abstractmethod
    def save(self, aggregate: ${name}) -> None:
        """Persist all state changes."""

    @abstractmethod
    def delete(self, id: ${name}Id) -> None:
        """Remove the aggregate."""

    @abstractmethod
    def exists(self, id: ${name}Id) -> bool:
        """Check existence without loading the aggregate."""
''')

PYTHON_EVENTS = Template('''\
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import ClassVar
from .${name}Id import ${name}Id


@dataclass(frozen=True)
class ${name}Event:
    """Base class for all ${name} domain events."""

    event_type: ClassVar[str]
    aggregate_id: ${name}Id
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )


@dataclass(frozen=True)
class ${name}Created(${name}Event):
    """Raised when a new ${name} is created."""

    event_type: ClassVar[str] = "${name}Created"


# Add more events below as your domain grows, for example:
# @dataclass(frozen=True)
# class ${name}Renamed(${name}Event):
#     event_type: ClassVar[str] = "${name}Renamed"
#     name: str = ""
''')

# ---------------------------------------------------------------------------
# Kotlin templates
# ---------------------------------------------------------------------------

KOTLIN_AGGREGATE = Template('''\
package com.example.${lname}

import java.time.Instant

class ${name}(val id: ${name}Id) {

    private val _events: MutableList<${name}Event> = mutableListOf()
    val events: List<${name}Event> get() = _events.toList()

    companion object {
        /** Factory — the only way to create a valid ${name}. */
        fun create(id: ${name}Id): ${name} {
            val agg = ${name}(id)
            agg.checkInvariants()
            agg.record(${name}Created(aggregateId = id))
            return agg
        }
    }

    /** Pull and clear pending domain events. */
    fun pullEvents(): List<${name}Event> {
        val copy = _events.toList()
        _events.clear()
        return copy
    }

    private fun record(event: ${name}Event) { _events.add(event) }

    private fun checkInvariants() {
        // Add invariant assertions here.
    }
}
''')

KOTLIN_ID = Template('''\
package com.example.${lname}

import java.util.UUID

@JvmInline
value class ${name}Id(val value: String) {
    init {
        require(value.isNotBlank()) { "${name}Id must not be blank." }
    }

    companion object {
        fun generate(): ${name}Id = ${name}Id(UUID.randomUUID().toString())
        fun of(raw: String): ${name}Id = ${name}Id(raw)
    }

    override fun toString(): String = value
}
''')

KOTLIN_REPOSITORY = Template('''\
package com.example.${lname}

interface ${name}Repository {
    fun findById(id: ${name}Id): ${name}?
    fun save(aggregate: ${name})
    fun delete(id: ${name}Id)
    fun exists(id: ${name}Id): Boolean
}
''')

KOTLIN_EVENTS = Template('''\
package com.example.${lname}

import java.time.Instant

sealed class ${name}Event {
    abstract val aggregateId: ${name}Id
    abstract val occurredAt: Instant
}

data class ${name}Created(
    override val aggregateId: ${name}Id,
    override val occurredAt: Instant = Instant.now()
) : ${name}Event()

// Add more events as the domain grows:
// data class ${name}Renamed(
//     override val aggregateId: ${name}Id,
//     val name: String,
//     override val occurredAt: Instant = Instant.now()
// ) : ${name}Event()
''')

# ---------------------------------------------------------------------------
# Java templates
# ---------------------------------------------------------------------------

JAVA_AGGREGATE = Template('''\
package com.example.${lname};

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

public final class ${name} {

    private final ${name}Id id;
    private final List<${name}Event> events = new ArrayList<>();

    private ${name}(${name}Id id) {
        this.id = Objects.requireNonNull(id, "id must not be null");
    }

    /** Factory — the only way to create a valid ${name}. */
    public static ${name} create(${name}Id id) {
        var agg = new ${name}(id);
        agg.checkInvariants();
        agg.record(new ${name}Created(id));
        return agg;
    }

    public ${name}Id getId() { return id; }

    /** Pull and clear pending domain events. */
    public List<${name}Event> pullEvents() {
        var copy = List.copyOf(events);
        events.clear();
        return copy;
    }

    private void record(${name}Event event) { events.add(event); }

    private void checkInvariants() {
        // Add invariant assertions here.
    }
}
''')

JAVA_ID = Template('''\
package com.example.${lname};

import java.util.Objects;
import java.util.UUID;

public record ${name}Id(String value) {

    public ${name}Id {
        Objects.requireNonNull(value, "value must not be null");
        if (value.isBlank()) throw new IllegalArgumentException("${name}Id must not be blank.");
    }

    public static ${name}Id generate() { return new ${name}Id(UUID.randomUUID().toString()); }
    public static ${name}Id of(String raw) { return new ${name}Id(raw); }

    @Override public String toString() { return value; }
}
''')

JAVA_REPOSITORY = Template('''\
package com.example.${lname};

import java.util.Optional;

public interface ${name}Repository {
    Optional<${name}> findById(${name}Id id);
    void save(${name} aggregate);
    void delete(${name}Id id);
    boolean exists(${name}Id id);
}
''')

JAVA_EVENTS = Template('''\
package com.example.${lname};

import java.time.Instant;

public sealed interface ${name}Event permits ${name}Created {
    ${name}Id aggregateId();
    Instant occurredAt();
}

record ${name}Created(${name}Id aggregateId, Instant occurredAt) implements ${name}Event {
    ${name}Created(${name}Id aggregateId) { this(aggregateId, Instant.now()); }
}

// Add more events as the domain grows:
// record ${name}Renamed(${name}Id aggregateId, String name, Instant occurredAt)
//     implements ${name}Event { ... }
''')

TEMPLATES = {
    "python": {
        "ext": "py",
        "aggregate": PYTHON_AGGREGATE,
        "id": PYTHON_ID,
        "repository": PYTHON_REPOSITORY,
        "events": PYTHON_EVENTS,
    },
    "kotlin": {
        "ext": "kt",
        "aggregate": KOTLIN_AGGREGATE,
        "id": KOTLIN_ID,
        "repository": KOTLIN_REPOSITORY,
        "events": KOTLIN_EVENTS,
    },
    "java": {
        "ext": "java",
        "aggregate": JAVA_AGGREGATE,
        "id": JAVA_ID,
        "repository": JAVA_REPOSITORY,
        "events": JAVA_EVENTS,
    },
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  Created: {path}")


def scaffold(name: str, lang: str, output_dir: Path) -> None:
    t = TEMPLATES[lang]
    ext = t["ext"]
    ctx = {"name": name, "lname": name.lower()}
    files = {
        f"{name}.{ext}": t["aggregate"],
        f"{name}Id.{ext}": t["id"],
        f"{name}Repository.{ext}": t["repository"],
        f"{name}Events.{ext}": t["events"],
    }
    print(f"\nScaffolding DDD aggregate '{name}' ({lang}) in {output_dir}/\n")
    for filename, tmpl in files.items():
        write(output_dir / filename, tmpl.substitute(ctx))

    print("\nNext steps:")
    print(f"  1. Implement your domain commands inside {name}.{ext}")
    print(f"  2. Add concrete repository in infrastructure/ (implements {name}Repository)")
    print(f"  3. Publish events from {name}Events.{ext} via a message broker")
    print(f"  4. Keep the aggregate free of infrastructure concerns\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold DDD aggregate building blocks.")
    parser.add_argument("name", help="Aggregate name (PascalCase), e.g. Order")
    parser.add_argument("--lang", choices=["python", "kotlin", "java"], default="python")
    parser.add_argument("--output-dir", default=".", type=Path)
    args = parser.parse_args()

    if not args.name[0].isupper():
        print(f"ERROR: AggregateName should be PascalCase (got '{args.name}').", file=sys.stderr)
        sys.exit(1)

    scaffold(args.name, args.lang, args.output_dir)


if __name__ == "__main__":
    main()
