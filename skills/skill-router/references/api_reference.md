# API Reference: Skill Quick-Lookup

Quick-lookup table for all 17 skills.

| Skill | Domain | Works Well With | Conflicts With |
|-------|--------|-----------------|----------------|
| `animation-at-work` | Web animation, motion | `refactoring-ui` | None |
| `clean-code-reviewer` | Code quality (any language) | `effective-java`, `effective-python`, `effective-kotlin` | `domain-driven-design` (model design context) |
| `data-intensive-patterns` | Storage internals, distributed data | `system-design-interview` | `system-design-interview` (different altitude) |
| `data-pipelines` | ETL, data ingestion, orchestration | `data-intensive-patterns`, `effective-python` | `microservices-patterns` |
| `design-patterns` | GoF OO patterns | `clean-code-reviewer`, `effective-java` | `domain-driven-design` |
| `domain-driven-design` | Domain modeling, DDD patterns | `microservices-patterns`, `clean-code-reviewer` | `clean-code-reviewer` (code review context) |
| `effective-java` | Java idioms and best practices | `clean-code-reviewer`, `design-patterns` | `clean-code-reviewer` (Java-specific vs general) |
| `effective-kotlin` | Kotlin best practices | `kotlin-in-action`, `clean-code-reviewer` | `kotlin-in-action` |
| `effective-python` | Python idioms and best practices | `clean-code-reviewer`, `using-asyncio-python` | `using-asyncio-python` (async topics) |
| `kotlin-in-action` | Kotlin language features | `effective-kotlin` | `effective-kotlin` |
| `lean-startup` | Startup strategy, MVP, pivots | None (strategy only) | All technical skills |
| `microservices-patterns` | Service decomposition, sagas, CQRS | `domain-driven-design`, `system-design-interview` | `domain-driven-design` (service vs model) |
| `refactoring-ui` | UI design, visual hierarchy | `animation-at-work` | None |
| `skill-router` | Skill selection and routing | All skills | None |
| `storytelling-with-data` | Data visualization, charts | `data-pipelines` | None |
| `system-design-interview` | System scalability, high-level design | `microservices-patterns`, `data-intensive-patterns` | `data-intensive-patterns` (altitude) |
| `using-asyncio-python` | Python asyncio, concurrency | `effective-python` | `effective-python` (async topics) |
| `web-scraping-python` | Web scraping, crawling | `effective-python`, `data-pipelines` | None |
