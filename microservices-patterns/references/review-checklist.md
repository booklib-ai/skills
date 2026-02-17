# Microservices Code Review Checklist

Use this checklist when reviewing microservices code. Work through each section
and flag any violations. Not every section applies to every review — skip sections
that aren't relevant to the code under review.

---

## 1. Service Decomposition

- [ ] Service boundaries align with business capabilities or DDD bounded contexts
- [ ] No "god service" doing too much — each service has a focused responsibility
- [ ] Services can be deployed independently
- [ ] No shared domain logic libraries that couple services at the code level
- [ ] Team ownership is clear — ideally one team owns one or a few related services

**Red flags**: A service that imports domain models from another service. A change
in one service requiring simultaneous deployment of another service.

---

## 2. Data Ownership

- [ ] Each service has its own private database/schema
- [ ] No shared database tables between services
- [ ] Services never directly query another service's database
- [ ] Data duplication (where it exists) is managed via events, not shared writes

**Red flags**: SQL joins across tables owned by different services. Connection strings
pointing to another service's database. Multiple services with write access to the same table.

---

## 3. Inter-Service Communication

- [ ] Communication style (sync vs async) matches the use case
- [ ] Synchronous calls have timeouts configured
- [ ] Circuit breakers protect against cascading failures
- [ ] No long synchronous call chains (A -> B -> C -> D)
- [ ] Async messaging uses transactional outbox or event sourcing for reliability
- [ ] Message consumers are idempotent
- [ ] Service discovery is in place (not hardcoded URLs)

**Red flags**: HTTP calls without timeouts. Retry loops without backoff. Direct
database writes as a "faster alternative" to messaging.

---

## 4. API Design

- [ ] APIs are versioned or use backward-compatible evolution
- [ ] API contracts are defined (OpenAPI, Proto files, AsyncAPI)
- [ ] Error responses follow a consistent format
- [ ] APIs return only what the client needs (no over-fetching)
- [ ] Consumer-driven contract tests exist for key API consumers

**Red flags**: Breaking API changes without versioning. No API documentation or contract.
Internal implementation details leaking through the API.

---

## 5. Transaction Management (Sagas)

- [ ] Cross-service operations use sagas, not distributed transactions (no 2PC)
- [ ] Each saga step has a compensating transaction defined
- [ ] Compensating transactions are idempotent
- [ ] Saga state is persisted (not just in-memory)
- [ ] Semantic locks or other countermeasures handle isolation concerns
- [ ] Saga orchestrator (if used) doesn't contain business logic — only coordinates

**Red flags**: Try/catch blocks attempting to rollback across service boundaries without
a saga. Services directly calling another service's "undo" endpoint without saga coordination.
Missing compensating transactions.

---

## 6. Business Logic & Domain Model

- [ ] Business logic lives in domain objects (aggregates), not in service/controller classes
- [ ] Aggregates enforce their own invariants
- [ ] One transaction modifies exactly one aggregate
- [ ] Aggregates reference other aggregates by ID, not by object reference
- [ ] Domain events are published after aggregate state changes
- [ ] Value objects are used where identity isn't needed

**Red flags**: Anemic domain model (entities are just data holders, all logic in services).
Transactions that modify multiple aggregates. Direct object references between aggregates.

---

## 7. Event Handling

- [ ] Events are named in past tense (OrderCreated, not CreateOrder)
- [ ] Events contain sufficient data for consumers to act without callbacks
- [ ] Event schema versioning strategy exists
- [ ] Event handlers are idempotent
- [ ] Ordering is preserved where needed (partition by aggregate ID)
- [ ] If using event sourcing: snapshots exist for aggregates with many events

**Red flags**: Events named as commands. Event handlers that call back to the
publishing service for more data. No strategy for event schema evolution.

---

## 8. Query Implementation

- [ ] Cross-service queries use API Composition or CQRS — not direct DB access
- [ ] API Composition: composer handles partial failures gracefully
- [ ] CQRS views: event handlers maintain denormalized read models
- [ ] CQRS views: eventual consistency is acceptable for the use case
- [ ] Query performance is adequate for the access patterns

**Red flags**: Queries that join data from multiple services' databases. N+1 query
patterns in API composition. CQRS view that falls too far behind event stream.

---

## 9. Testing

- [ ] Unit tests cover domain logic (aggregates, value objects, saga orchestrators)
- [ ] Integration tests verify infrastructure interactions (DB, messaging, HTTP clients)
- [ ] Component tests exercise the service end-to-end with stubbed dependencies
- [ ] Consumer-driven contract tests protect API compatibility
- [ ] End-to-end tests are minimal and focused on critical paths
- [ ] Tests use containers (Testcontainers) for realistic infrastructure testing

**Red flags**: Only end-to-end tests (slow, brittle). No contract tests between
services that communicate. Mocks that hide real integration issues.

---

## 10. Observability

- [ ] Health check endpoint exists (GET /health or /actuator/health)
- [ ] Structured logging with correlation/trace IDs
- [ ] Distributed tracing is instrumented (OpenTelemetry or equivalent)
- [ ] Key metrics are exposed (request rate, latency, error rate)
- [ ] Alerts are configured for critical failure conditions

**Red flags**: Console.log as the only logging. No health endpoint. No way to
trace a request across service boundaries.

---

## 11. Configuration & Security

- [ ] Configuration is externalized (not hardcoded)
- [ ] Secrets are managed securely (not in source code or env files in repo)
- [ ] Service-to-service communication is authenticated (mTLS or API keys)
- [ ] Input validation exists at service boundaries
- [ ] Principle of least privilege for database access

**Red flags**: Database passwords in source code. Services accepting unauthenticated
internal requests. Configuration values baked into artifacts.

---

## Severity Classification

When reporting issues, classify them:

- **Critical**: Data loss risk, security vulnerability, or correctness issue
  (e.g., shared database, missing compensating transactions, no auth)
- **Major**: Architectural debt that will cause scaling/maintenance problems
  (e.g., synchronous chains, god service, anemic domain model)
- **Minor**: Best practice deviation with limited immediate impact
  (e.g., missing health check, no structured logging)
- **Suggestion**: Improvement that would be nice but isn't urgent
  (e.g., could benefit from CQRS in the future, consider event sourcing)
