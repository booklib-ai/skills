#!/usr/bin/env python3
"""
Microservice Scaffold — generates a new microservice skeleton with proper boundaries.

Usage: python new_service.py <ServiceName> [--lang python|java|kotlin] [--output-dir ./]

Generates a service with:
  - Its own domain model (no shared DB)
  - Event publishing stub
  - Health endpoint
  - README with responsibility and run instructions
"""

import argparse
import re
import sys
from pathlib import Path
from string import Template

# ---------------------------------------------------------------------------
# Name helpers
# ---------------------------------------------------------------------------

def to_snake(name: str) -> str:
    """PascalCase -> snake_case, e.g. OrderService -> order_service"""
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    return s.lower()


def to_kebab(name: str) -> str:
    return to_snake(name).replace("_", "-")


def strip_service(name: str) -> str:
    """Remove trailing 'Service' suffix for entity naming."""
    return re.sub(r"Service$", "", name, flags=re.IGNORECASE)


# ---------------------------------------------------------------------------
# Python templates
# ---------------------------------------------------------------------------

PY_MAIN = Template("""\
#!/usr/bin/env python3
\"\"\"Entry point for the $service_name microservice.\"\"\"
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api.routes:app", host="0.0.0.0", port=8000, reload=False)
""")

PY_ROUTES = Template("""\
\"\"\"FastAPI routes for $service_name.\"\"\"
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ..domain.${entity_snake} import ${Entity}, ${Entity}Id
from ..domain.${entity_snake}_repository import ${Entity}Repository
from ..infrastructure.in_memory_repository import InMemory${Entity}Repository
from ..infrastructure.event_publisher import EventPublisher

app = FastAPI(title="$service_name", version="0.1.0")

# In production replace with real DI / IOC.
_repo: ${Entity}Repository = InMemory${Entity}Repository()
_publisher = EventPublisher()


class Create${Entity}Request(BaseModel):
    name: str


class ${Entity}Response(BaseModel):
    id: str
    name: str


@app.get("/healthz")
def health() -> dict:
    return {"status": "ok", "service": "$service_name"}


@app.post("/${entity_kebab}s", response_model=${Entity}Response, status_code=201)
def create_${entity_snake}(req: Create${Entity}Request) -> ${Entity}Response:
    entity = ${Entity}.create(name=req.name)
    _repo.save(entity)
    for event in entity.pull_events():
        _publisher.publish(event)
    return ${Entity}Response(id=str(entity.id), name=entity.name)


@app.get("/${entity_kebab}s/{id}", response_model=${Entity}Response)
def get_${entity_snake}(id: str) -> ${Entity}Response:
    entity = _repo.find_by_id(${Entity}Id(id))
    if entity is None:
        raise HTTPException(status_code=404, detail="${Entity} not found")
    return ${Entity}Response(id=str(entity.id), name=entity.name)
""")

PY_ENTITY = Template("""\
\"\"\"Domain entity for $Entity — $service_name aggregate root.\"\"\"
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import uuid


@dataclass(frozen=True)
class ${Entity}Id:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("${Entity}Id must not be blank.")

    @classmethod
    def generate(cls) -> "${Entity}Id":
        return cls(str(uuid.uuid4()))

    def __str__(self) -> str:
        return self.value


@dataclass
class ${Entity}Event:
    event_type: str
    payload: dict


@dataclass
class ${Entity}:
    id: ${Entity}Id
    name: str
    _events: List[${Entity}Event] = field(default_factory=list, init=False, repr=False)

    @classmethod
    def create(cls, name: str) -> "${Entity}":
        if not name or not name.strip():
            raise ValueError("name must not be blank.")
        entity = cls(id=${Entity}Id.generate(), name=name)
        entity._events.append(${Entity}Event("${Entity}Created", {"id": str(entity.id), "name": name}))
        return entity

    def pull_events(self) -> List[${Entity}Event]:
        events, self._events = self._events, []
        return events
""")

PY_REPOSITORY = Template("""\
\"\"\"Repository interface (port) for ${Entity}.\"\"\"
from abc import ABC, abstractmethod
from typing import Optional
from .${entity_snake} import ${Entity}, ${Entity}Id


class ${Entity}Repository(ABC):
    @abstractmethod
    def find_by_id(self, id: ${Entity}Id) -> Optional[${Entity}]: ...

    @abstractmethod
    def save(self, entity: ${Entity}) -> None: ...

    @abstractmethod
    def delete(self, id: ${Entity}Id) -> None: ...
""")

PY_IN_MEMORY_REPO = Template("""\
\"\"\"In-memory repository for development and testing.\"\"\"
from typing import Dict, Optional
from ..domain.${entity_snake} import ${Entity}, ${Entity}Id
from ..domain.${entity_snake}_repository import ${Entity}Repository


class InMemory${Entity}Repository(${Entity}Repository):
    def __init__(self) -> None:
        self._store: Dict[str, ${Entity}] = {}

    def find_by_id(self, id: ${Entity}Id) -> Optional[${Entity}]:
        return self._store.get(id.value)

    def save(self, entity: ${Entity}) -> None:
        self._store[entity.id.value] = entity

    def delete(self, id: ${Entity}Id) -> None:
        self._store.pop(id.value, None)
""")

PY_EVENT_PUBLISHER = Template("""\
\"\"\"Event publisher stub — replace with real broker integration (Kafka, SNS, etc.).\"\"\"
import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


class EventPublisher:
    \"\"\"Publishes domain events to a message broker.

    In production, swap this stub with a Kafka producer, AWS SNS client,
    RabbitMQ publisher, or similar. The interface intentionally stays simple.
    \"\"\"

    def publish(self, event: Any) -> None:
        payload = {
            "event_type": getattr(event, "event_type", type(event).__name__),
            "payload": getattr(event, "payload", {}),
        }
        logger.info("EVENT PUBLISHED: %s", json.dumps(payload))
        # TODO: replace with real broker call, e.g.:
        # self._producer.produce(topic="$service_kebab-events", value=json.dumps(payload))
""")

PY_REQUIREMENTS = Template("""\
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
pydantic>=2.0.0
""")

PY_DOCKERFILE = Template("""\
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
""")

PY_INIT = """\
"""

# ---------------------------------------------------------------------------
# Java templates (single-file for brevity; split in real project)
# ---------------------------------------------------------------------------

JAVA_ENTITY = Template("""\
package com.example.${entity_lower};

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public final class ${Entity} {
    private final ${Entity}Id id;
    private String name;
    private final List<${Entity}Event> events = new ArrayList<>();

    private ${Entity}(${Entity}Id id, String name) {
        this.id = id;
        this.name = name;
    }

    public static ${Entity} create(String name) {
        if (name == null || name.isBlank()) throw new IllegalArgumentException("name must not be blank");
        var e = new ${Entity}(${Entity}Id.generate(), name);
        e.events.add(new ${Entity}Event("${Entity}Created", java.util.Map.of("id", e.id.value(), "name", name)));
        return e;
    }

    public ${Entity}Id getId() { return id; }
    public String getName() { return name; }

    public List<${Entity}Event> pullEvents() {
        var copy = List.copyOf(events);
        events.clear();
        return copy;
    }
}
""")

JAVA_ID = Template("""\
package com.example.${entity_lower};
import java.util.UUID;

public record ${Entity}Id(String value) {
    public ${Entity}Id { if (value == null || value.isBlank()) throw new IllegalArgumentException("blank id"); }
    public static ${Entity}Id generate() { return new ${Entity}Id(UUID.randomUUID().toString()); }
    public static ${Entity}Id of(String s) { return new ${Entity}Id(s); }
    @Override public String toString() { return value; }
}
""")

JAVA_EVENT = Template("""\
package com.example.${entity_lower};
import java.util.Map;

public record ${Entity}Event(String eventType, Map<String, Object> payload) {}
""")

JAVA_REPOSITORY = Template("""\
package com.example.${entity_lower};
import java.util.Optional;

public interface ${Entity}Repository {
    Optional<${Entity}> findById(${Entity}Id id);
    void save(${Entity} entity);
    void delete(${Entity}Id id);
}
""")

JAVA_PUBLISHER = Template("""\
package com.example.${entity_lower};

public class EventPublisher {
    /** Replace with Kafka / SNS / RabbitMQ integration in production. */
    public void publish(${Entity}Event event) {
        System.out.printf("[EVENT] type=%s payload=%s%n", event.eventType(), event.payload());
    }
}
""")

JAVA_MAIN = Template("""\
package com.example.${entity_lower};

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * Minimal HTTP entry point — wire up Spring Boot / Micronaut / Quarkus in production.
 * This stub demonstrates domain wiring only.
 */
public class Main {

    // In-memory repo for the stub
    static Map<String, ${Entity}> store = new HashMap<>();
    static ${Entity}Repository repo = new ${Entity}Repository() {
        public Optional<${Entity}> findById(${Entity}Id id) { return Optional.ofNullable(store.get(id.value())); }
        public void save(${Entity} e) { store.put(e.getId().value(), e); }
        public void delete(${Entity}Id id) { store.remove(id.value()); }
    };
    static EventPublisher publisher = new EventPublisher();

    public static void main(String[] args) {
        var entity = ${Entity}.create("Example");
        repo.save(entity);
        entity.pullEvents().forEach(publisher::publish);
        System.out.println("Created: " + entity.getId());

        var found = repo.findById(entity.getId());
        found.ifPresent(e -> System.out.println("Found: " + e.getName()));
    }
}
""")

# ---------------------------------------------------------------------------
# Kotlin templates
# ---------------------------------------------------------------------------

KT_ENTITY = Template("""\
package com.example.${entity_lower}

import java.util.UUID

data class ${Entity}Id(val value: String) {
    init { require(value.isNotBlank()) { "blank id" } }
    companion object {
        fun generate() = ${Entity}Id(UUID.randomUUID().toString())
        fun of(s: String) = ${Entity}Id(s)
    }
    override fun toString() = value
}

data class ${Entity}Event(val eventType: String, val payload: Map<String, Any>)

class ${Entity} private constructor(val id: ${Entity}Id, val name: String) {
    private val _events = mutableListOf<${Entity}Event>()

    companion object {
        fun create(name: String): ${Entity} {
            require(name.isNotBlank()) { "name must not be blank" }
            val e = ${Entity}(${Entity}Id.generate(), name)
            e._events.add(${Entity}Event("${Entity}Created", mapOf("id" to e.id.value, "name" to name)))
            return e
        }
    }

    fun pullEvents(): List<${Entity}Event> {
        val copy = _events.toList(); _events.clear(); return copy
    }
}
""")

KT_REPOSITORY = Template("""\
package com.example.${entity_lower}

interface ${Entity}Repository {
    fun findById(id: ${Entity}Id): ${Entity}?
    fun save(entity: ${Entity})
    fun delete(id: ${Entity}Id)
}

class InMemory${Entity}Repository : ${Entity}Repository {
    private val store = mutableMapOf<String, ${Entity}>()
    override fun findById(id: ${Entity}Id) = store[id.value]
    override fun save(entity: ${Entity}) { store[entity.id.value] = entity }
    override fun delete(id: ${Entity}Id) { store.remove(id.value) }
}
""")

KT_PUBLISHER = Template("""\
package com.example.${entity_lower}

class EventPublisher {
    /** Replace with Kafka / SNS / RabbitMQ integration in production. */
    fun publish(event: ${Entity}Event) {
        println("[EVENT] type=${dollar}{event.eventType} payload=${dollar}{event.payload}")
    }
}
""")

KT_MAIN = Template("""\
package com.example.${entity_lower}

fun main() {
    val repo: ${Entity}Repository = InMemory${Entity}Repository()
    val publisher = EventPublisher()

    val entity = ${Entity}.create("Example")
    repo.save(entity)
    entity.pullEvents().forEach { publisher.publish(it) }

    println("Created: ${dollar}{entity.id}")
    println("Found:   ${dollar}{repo.findById(entity.id)?.name}")
}
""")

README = Template("""\
# $service_name

## Responsibility

> **$service_name** is responsible for managing the lifecycle of `$Entity` resources.
> It owns its own data store and publishes domain events when state changes occur.

This service follows the microservices pattern of **one service, one bounded context**.
It does **not** share a database with any other service.

## Structure

```
$service_dir/
├── app/
│   ├── api/          # HTTP layer (routes, request/response models)
│   ├── domain/       # Entities, value objects, repository interfaces
│   └── infrastructure/   # Concrete adapters (DB, cache, event broker)
├── main.py           # Entry point
├── requirements.txt
├── Dockerfile
└── README.md
```

## Running Locally

```bash
pip install -r requirements.txt
python main.py
# or:
uvicorn app.api.routes:app --reload
```

Open http://localhost:8000/docs for the interactive API documentation.

## Events Published

| Event | Trigger | Payload |
|-------|---------|---------|
| `${Entity}Created` | POST /${entity_kebab}s | `{id, name}` |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | HTTP listen port |
| `DATABASE_URL` | in-memory | Connection string for the DB adapter |
| `BROKER_URL` | stdout | Event broker endpoint |

## Design Decisions

- **No shared database**: Other services must call this service's API or consume its events.
- **Event publishing**: Every state change emits a domain event for downstream consumers.
- **Repository pattern**: The domain layer depends on an interface; the infrastructure layer provides the adapter.
""")


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------

def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  Created: {path}")


def scaffold_python(service_dir: Path, ctx: dict) -> None:
    base = service_dir
    write(base / "main.py", PY_MAIN.substitute(ctx))
    write(base / "requirements.txt", PY_REQUIREMENTS.substitute(ctx))
    write(base / "Dockerfile", PY_DOCKERFILE.substitute(ctx))
    write(base / "app" / "__init__.py", PY_INIT)
    write(base / "app" / "api" / "__init__.py", PY_INIT)
    write(base / "app" / "api" / "routes.py", PY_ROUTES.substitute(ctx))
    write(base / "app" / "domain" / "__init__.py", PY_INIT)
    write(base / "app" / "domain" / f"{ctx['entity_snake']}.py", PY_ENTITY.substitute(ctx))
    write(base / "app" / "domain" / f"{ctx['entity_snake']}_repository.py", PY_REPOSITORY.substitute(ctx))
    write(base / "app" / "infrastructure" / "__init__.py", PY_INIT)
    write(base / "app" / "infrastructure" / "in_memory_repository.py", PY_IN_MEMORY_REPO.substitute(ctx))
    write(base / "app" / "infrastructure" / "event_publisher.py", PY_EVENT_PUBLISHER.substitute(ctx))


def scaffold_java(service_dir: Path, ctx: dict) -> None:
    pkg = service_dir / "src" / "main" / "java" / "com" / "example" / ctx["entity_lower"]
    write(pkg / f"{ctx['Entity']}.java", JAVA_ENTITY.substitute(ctx))
    write(pkg / f"{ctx['Entity']}Id.java", JAVA_ID.substitute(ctx))
    write(pkg / f"{ctx['Entity']}Event.java", JAVA_EVENT.substitute(ctx))
    write(pkg / f"{ctx['Entity']}Repository.java", JAVA_REPOSITORY.substitute(ctx))
    write(pkg / "EventPublisher.java", JAVA_PUBLISHER.substitute(ctx))
    write(pkg / "Main.java", JAVA_MAIN.substitute(ctx))


def scaffold_kotlin(service_dir: Path, ctx: dict) -> None:
    pkg = service_dir / "src" / "main" / "kotlin" / "com" / "example" / ctx["entity_lower"]
    write(pkg / f"{ctx['Entity']}.kt", KT_ENTITY.substitute(ctx))
    write(pkg / f"{ctx['Entity']}Repository.kt", KT_REPOSITORY.substitute(ctx))
    write(pkg / "EventPublisher.kt", KT_PUBLISHER.substitute(ctx))
    write(pkg / "Main.kt", KT_MAIN.substitute(ctx))


SCAFFOLDERS = {"python": scaffold_python, "java": scaffold_java, "kotlin": scaffold_kotlin}


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a microservice skeleton.")
    parser.add_argument("service_name", metavar="ServiceName",
                        help="Service name in PascalCase, e.g. OrderService")
    parser.add_argument("--lang", choices=["python", "java", "kotlin"], default="python")
    parser.add_argument("--output-dir", default=".", type=Path)
    args = parser.parse_args()

    name = args.service_name
    entity = strip_service(name)
    service_dir = args.output_dir / to_kebab(name)

    ctx = {
        "service_name": name,
        "service_kebab": to_kebab(name),
        "service_dir": to_kebab(name),
        "Entity": entity,
        "entity_snake": to_snake(entity),
        "entity_lower": entity.lower(),
        "entity_kebab": to_kebab(entity),
        "dollar": "$",
    }

    print(f"\nScaffolding microservice '{name}' ({args.lang}) in {service_dir}/\n")
    SCAFFOLDERS[args.lang](service_dir, ctx)
    write(service_dir / "README.md", README.substitute(ctx))

    print(f"\nDone. Next steps:")
    if args.lang == "python":
        print(f"  cd {service_dir}")
        print(f"  pip install -r requirements.txt")
        print(f"  python main.py")
        print(f"  # API docs: http://localhost:8000/docs")
    elif args.lang == "java":
        print(f"  cd {service_dir}")
        print(f"  # Add to a Maven/Gradle project, then: mvn compile exec:java -Dexec.mainClass=com.example.{entity.lower()}.Main")
    elif args.lang == "kotlin":
        print(f"  cd {service_dir}")
        print(f"  # Add to a Gradle project, then: ./gradlew run")
    print(f"\n  Replace InMemory{entity}Repository with a real DB adapter.")
    print(f"  Replace EventPublisher stub with a Kafka/SNS producer.\n")


if __name__ == "__main__":
    main()
