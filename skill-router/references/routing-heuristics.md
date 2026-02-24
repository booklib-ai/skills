# Routing Heuristics

Decision rules for the skill-router. Apply these in order.

## Primary Rules (apply first)

### By Language

| Language | Primary Skill | Override Condition |
|----------|-------------|-------------------|
| Python (general) | `effective-python` | If async → `using-asyncio-python`; if scraping → `web-scraping-python` |
| Python (async/concurrent) | `using-asyncio-python` | Always wins over effective-python for async topics |
| Python (web scraping) | `web-scraping-python` | Always wins for scraping topics |
| Java | `effective-java` | If code quality focus → `clean-code-reviewer` |
| Kotlin | `effective-kotlin` | If learning Kotlin → `kotlin-in-action` |
| Any language (code quality) | `clean-code-reviewer` | Language-agnostic; always applicable for readability |
| CSS/HTML/Frontend | `refactoring-ui` | If animation → `animation-at-work` |
| Any (visualization) | `storytelling-with-data` | Must have a visual component |

### By Domain

| Domain | Primary Skill |
|--------|-------------|
| Domain modeling, DDD | `domain-driven-design` |
| Service decomposition, distributed systems | `microservices-patterns` |
| GoF design patterns | `design-patterns` |
| System scalability, estimation | `system-design-interview` |
| Storage internals, distributed data | `data-intensive-patterns` |
| Data pipelines, ETL | `data-pipelines` |
| Startup strategy, product | `lean-startup` |

## Conflict Resolution Rules

### clean-code-reviewer vs effective-java
- **Code-level review with naming/readability focus** → `clean-code-reviewer`
- **Java-specific items (generics, enums, serialization, lambdas)** → `effective-java`
- **Both applicable** → primary: `clean-code-reviewer`, secondary: `effective-java`

### effective-kotlin vs kotlin-in-action
- **User knows Kotlin, wants best practice advice** → `effective-kotlin`
- **User is learning Kotlin or asking about language features** → `kotlin-in-action`
- **Ambiguous** → ask whether they want best practices or feature explanation

### domain-driven-design vs microservices-patterns
- **Designing or reviewing a domain model** → `domain-driven-design`
- **Designing service decomposition, sagas, inter-service communication** → `microservices-patterns`
- **Designing a new microservice with rich domain** → apply both: DDD first (model), microservices-patterns second (service design)

### domain-driven-design vs clean-code-reviewer
- **Model design** → `domain-driven-design` (ignore clean code's "small functions" rule when modeling)
- **Code review** → `clean-code-reviewer` (DDD model concerns are separate from code readability)

### data-intensive-patterns vs system-design-interview
- **Internals: storage engines, replication, consistency models** → `data-intensive-patterns`
- **High-level: system components, scale, estimation** → `system-design-interview`
- **Full system design** → primary: `system-design-interview`, secondary: `data-intensive-patterns`

### effective-python vs using-asyncio-python
- **Any async/concurrent Python** → `using-asyncio-python` (always wins)
- **Non-async Python** → `effective-python`

## Work Type Rules

| Work Type | Routing Preference |
|-----------|-------------------|
| Code review | Language-specific skill OR `clean-code-reviewer` |
| Code generation | Domain-specific skill (DDD, microservices, design-patterns) |
| Migration planning | Skill with Mode 3 (clean-code-reviewer, domain-driven-design, microservices-patterns) |
| System design | `system-design-interview` + optional `microservices-patterns` |
| Learning | Language-specific learning skill (kotlin-in-action) or domain skill |

## Anti-Trigger Rules

Never route to these skills if:

| Skill | Don't route if... |
|-------|------------------|
| `domain-driven-design` | Simple CRUD, no complex domain, < 3 entity types |
| `microservices-patterns` | Single service, no decomposition intent |
| `lean-startup` | Pure technical code — this is a strategy skill only |
| `effective-java` | Code is not Java |
| `effective-kotlin` | Code is not Kotlin |
| `effective-python` | Code is not Python |
| `using-asyncio-python` | Code is not async Python |
| `web-scraping-python` | Not web scraping |
| `refactoring-ui` | No UI component |
| `storytelling-with-data` | No visualization |
| `animation-at-work` | No animation/motion concern |
| `system-design-interview` | Code-level concern, not system-level |
