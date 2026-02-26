# Microservices Patterns Catalog

Comprehensive reference of patterns from Chris Richardson's *Microservices Patterns*.
Organized by problem category. Read the section relevant to the code you're generating.

---

## Table of Contents

1. [Decomposition Patterns](#decomposition-patterns)
2. [Communication Patterns](#communication-patterns)
3. [API Gateway Patterns](#api-gateway-patterns)
4. [Transaction Management — Sagas](#transaction-management--sagas)
5. [Business Logic Patterns](#business-logic-patterns)
6. [Event Sourcing](#event-sourcing)
7. [Query Patterns](#query-patterns)
8. [Testing Patterns](#testing-patterns)
9. [Deployment Patterns](#deployment-patterns)
10. [Observability Patterns](#observability-patterns)

---

## Decomposition Patterns

### Decompose by Business Capability

Map services to what the organization *does*. Business capabilities are stable
over time even as org structure changes.

- Identify top-level capabilities (Order Management, Delivery, Billing, etc.)
- Each capability becomes a candidate service
- Services own the data for their capability

**When to use**: Starting a new microservices project or breaking up a monolith.

### Decompose by Subdomain (DDD)

Use Domain-Driven Design to identify bounded contexts. Each bounded context
becomes a service.

- Core subdomains: the competitive advantage (invest the most here)
- Supporting subdomains: necessary but not differentiating
- Generic subdomains: solved problems (use off-the-shelf solutions)

**When to use**: Complex domain where business capability mapping isn't granular enough.

### Strangler Fig Pattern

Incrementally migrate from monolith to microservices by building new functionality
as services and gradually routing traffic away from the monolith.

- Stand up new service alongside monolith
- Route specific requests to new service
- Gradually migrate functionality
- Eventually decommission monolith component

**When to use**: Migrating an existing monolith without a big-bang rewrite.

---

## Communication Patterns

### Synchronous — REST

- Use for simple request/response interactions
- Design APIs using the Richardson Maturity Model (ideally Level 2+)
- Define IDL: OpenAPI/Swagger for REST
- Handle partial failure: timeouts, retries, circuit breakers

### Synchronous — gRPC

- Binary protocol, strongly typed via Protocol Buffers
- More efficient than REST for inter-service calls
- Supports streaming (server, client, bidirectional)
- Good for polyglot environments (code generation for many languages)

### Asynchronous — Messaging

- Services communicate via message broker (Kafka, RabbitMQ, etc.)
- Message types: **Document** (carries data), **Command** (request action), **Event** (notification of change)
- Channels: **Point-to-point** (one consumer) or **Publish-subscribe** (many consumers)

Key implementation concerns:

- **Message ordering**: Use partitioned channels (e.g., Kafka partitions keyed by aggregate ID)
- **Duplicate handling**: Make consumers idempotent (track processed message IDs, or make operations naturally idempotent)
- **Transactional outbox**: Write events to an OUTBOX table in the same transaction as business data, then relay to broker — ensures atomicity without distributed transactions
- **Polling publisher or Transaction log tailing**: Two strategies for relaying outbox messages to the broker

### Circuit Breaker

Wrap remote calls in a circuit breaker to handle downstream failures gracefully:

- **Closed**: Requests pass through normally
- **Open**: Requests fail immediately (after failure threshold exceeded)
- **Half-open**: Periodically try a request; if it succeeds, close the circuit

Use libraries like Resilience4j (Java) or Polly (.NET).

### Service Discovery

Services need to locate each other. Two approaches:

- **Client-side discovery**: Client queries a registry (e.g., Eureka) and load-balances
- **Server-side discovery**: Client calls a router/load balancer that queries the registry (e.g., Kubernetes services, AWS ELB)

---

## API Gateway Patterns

### API Gateway

Single entry point for external clients. Responsibilities:

- Request routing to appropriate microservice
- API composition (aggregate responses from multiple services)
- Protocol translation (external REST to internal gRPC/messaging)
- Authentication and rate limiting
- Edge functions (caching, monitoring, etc.)

### Backend for Frontend (BFF)

Separate API gateway per client type (web, mobile, third-party). Each BFF:

- Tailors the API to its client's needs
- Handles client-specific data aggregation
- Is owned by the client team
- Reduces coupling between client and backend service evolution

**When to use BFF over single gateway**: When different clients have significantly different API needs.

---

## Transaction Management — Sagas

### The Problem

Microservices use Database per Service, so you cannot use ACID transactions
across services. Sagas maintain data consistency using a sequence of local
transactions with compensating transactions for rollback.

### Choreography-based Saga

Services publish events and subscribe to each other's events:

```
OrderService -> OrderCreated event
  -> PaymentService listens, processes payment, publishes PaymentAuthorized
    -> KitchenService listens, creates ticket, publishes TicketCreated
      -> OrderService listens, approves order
```

- Pros: Simple, no central coordinator, loose coupling
- Cons: Hard to understand the flow, cyclic dependencies possible

### Orchestration-based Saga

A central saga orchestrator tells participants what to do:

```
CreateOrderSaga:
  1. OrderService.createOrder(PENDING)
  2. PaymentService.authorize() -> fail? -> OrderService.rejectOrder()
  3. KitchenService.createTicket() -> fail? -> PaymentService.reverseAuth(), OrderService.rejectOrder()
  4. OrderService.approveOrder()
```

- Pros: Clear flow, easy to understand, avoids cyclic dependencies
- Cons: Risk of centralizing too much logic in orchestrator

### Saga Design Rules

- Each saga step modifies one aggregate in one service
- Every forward step needs a compensating transaction (undo/rollback action)
- Compensating transactions must be idempotent (safe to retry)
- Use semantic locks — mark records as "pending" during saga execution
- Countermeasures for lack of isolation: semantic locks, commutative updates, pessimistic/optimistic views, re-reading values

---

## Business Logic Patterns

### Aggregate Pattern (DDD)

An aggregate is a cluster of domain objects treated as a unit for data changes.

- **Aggregate root**: Top-level entity through which all external access occurs
- **Invariants**: Business rules enforced within the aggregate
- **Transaction boundary**: One transaction = one aggregate update
- **References between aggregates**: Use IDs, not object references

Design rules:
- Keep aggregates small — reference other aggregates by identity
- Business logic lives in the aggregate, not in service classes
- Aggregates publish domain events when their state changes

### Domain Events

Events represent something meaningful that happened in the domain:

- Named in past tense: OrderCreated, PaymentAuthorized, TicketAccepted
- Contain relevant data (IDs, state at time of event)
- Published by aggregates after state changes
- Consumed by other services for integration

### Domain Event Publishing

Two approaches to reliably publish events:

1. **Transactional outbox**: Store events in an outbox table in the same DB transaction as business data, then asynchronously publish to message broker
2. **Event sourcing**: Events are the primary store (see below)

---

## Event Sourcing

Instead of storing current state, store a sequence of state-changing events.
Reconstruct current state by replaying events.

### How It Works

- Each aggregate stored as a sequence of events in an event store
- To load: fetch all events, replay to reconstruct state
- To save: append new events to the store
- Event store is append-only (never update, never delete)

### Benefits

- Reliable event publishing (events ARE the data — no outbox needed)
- Complete audit trail
- Temporal queries (reconstruct state at any point in time)
- Enables CQRS naturally

### Challenges

- Learning curve; different way of thinking
- Querying the event store is hard (need CQRS for queries)
- Event schema evolution — events are immutable, so versioning matters
- Deleting data (e.g., GDPR) requires special handling like encryption with deletable keys

### Snapshots

For aggregates with many events, periodically save a snapshot of current state
to avoid replaying the entire history. Load: last snapshot + events after snapshot.

---

## Query Patterns

### API Composition

For queries spanning multiple services, an API composer calls each service
and combines results in memory.

```
API Composer (or API Gateway):
  1. Call OrderService.getOrders(customerId)
  2. Call DeliveryService.getDeliveries(orderIds)
  3. Call RestaurantService.getRestaurants(restaurantIds)
  4. Join results in memory, return to client
```

- Pros: Simple to implement
- Cons: Increased latency, no efficient join/filter across services, reduced availability

**When to use**: Simple queries where data from 2-3 services needs combining.

### CQRS (Command Query Responsibility Segregation)

Separate the write model (commands) from the read model (queries):

- **Command side**: Services handle commands, publish domain events
- **Query side**: A separate view service subscribes to events and maintains denormalized read-optimized database

```
OrderService publishes OrderCreated ->
DeliveryService publishes DeliveryStatusUpdated ->
  OrderHistoryViewService subscribes to both,
  maintains denormalized OrderHistoryView table,
  serves GET /order-history queries
```

- Pros: Efficient queries, scales reads independently, supports complex cross-service queries
- Cons: Extra complexity, eventual consistency, additional infrastructure

**When to use**: Complex queries spanning many services, or when read performance is critical.

---

## Testing Patterns

### Consumer-Driven Contract Testing

Each consumer defines a contract: "I expect your API to behave like X."
Provider runs these contracts as tests to ensure compatibility.

- Tools: Spring Cloud Contract, Pact
- Catches breaking changes before deployment

### Service Component Testing

Test a service in isolation by stubbing its dependencies:

- In-memory stubs for downstream services
- In-memory or containerized database
- Verify behavior end-to-end through the service's API

### Integration Testing

Test interaction between a service and its infrastructure:

- Database integration tests (verify SQL, schema migrations)
- Messaging integration tests (verify event publishing/consuming)
- REST client integration tests (verify HTTP calls)
- Use Docker (Testcontainers) for realistic infrastructure

### Testing Pyramid for Microservices

From bottom (fast, many) to top (slow, few):

1. Unit tests — domain logic, aggregates, sagas
2. Integration tests — persistence, messaging, REST clients
3. Component tests — single service end-to-end with stubs
4. Contract tests — API compatibility between consumer and provider
5. End-to-end tests — full system (keep these minimal)

---

## Deployment Patterns

### Service per Container

Package each service as a Docker container image:

- Encapsulates service and dependencies
- Consistent across environments
- Use multi-stage builds to keep images small

### Kubernetes Orchestration

- Deployment: Manages replicas and rolling updates
- Service: Stable network endpoint for service discovery
- ConfigMap/Secret: Externalized configuration
- Probes: Liveness and readiness health checks

### Service Mesh

Infrastructure layer handling service-to-service communication:

- Automatic mTLS between services
- Traffic management (retries, timeouts, circuit breaking)
- Observability (distributed tracing, metrics)
- Tools: Istio, Linkerd

### Externalized Configuration

- Environment variables, config servers (Spring Cloud Config), Kubernetes ConfigMaps
- Secrets managed separately (Vault, Kubernetes Secrets)
- Same artifact runs in different environments

---

## Observability Patterns

### Health Check API

Every service exposes a health endpoint (GET /health) reporting:
- Service status (UP/DOWN)
- Dependency status (database, message broker)
- Used by orchestrators and load balancers

### Distributed Tracing

Assign unique trace ID to each external request, propagate through all service calls.
- Tools: Zipkin, Jaeger, AWS X-Ray
- Instrument with OpenTelemetry

### Log Aggregation

Centralize logs from all services:
- Include trace IDs for correlation
- Structured logging (JSON format)
- Tools: ELK Stack, Fluentd, Datadog

### Application Metrics

Collect and expose metrics from each service:
- Request rate, latency, error rate (RED method)
- Resource utilization
- Business metrics
- Tools: Prometheus + Grafana, Datadog, CloudWatch
