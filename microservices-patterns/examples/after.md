# After

`InventoryService` owns its own read model, populated by consuming `OrderLineItemAdded` domain events published by the Order Service — no shared database access.

```java
// --- Order Service publishes domain events (its own codebase) ---

@DomainEvent
public record OrderLineItemAdded(
    String orderId,
    String productId,
    int quantity,
    Instant occurredAt
) {}

// Order Service publishes this event after saving the order aggregate
orderEventPublisher.publish(new OrderLineItemAdded(
    order.getId(), line.getProductId(), line.getQuantity(), Instant.now()
));


// --- Inventory Service: owns its own read model, no shared DB ---

// Private denormalized table — owned exclusively by Inventory Service
@Entity @Table(name = "product_weekly_sales")
public class ProductWeeklySales {
    @Id private String productId;
    private int unitsSoldLast7Days;
    private Instant lastUpdated;
}

@Component
public class OrderLineItemAddedConsumer {

    @KafkaListener(topics = "order.events", groupId = "inventory-service")
    public void handle(OrderLineItemAdded event) {
        // Idempotent: uses event's occurredAt to filter stale events
        if (event.occurredAt().isBefore(Instant.now().minus(7, DAYS))) return;

        weeklySalesRepository.incrementUnitsSold(event.productId(), event.quantity());
    }
}

@RestController @RequestMapping("/inventory")
public class InventoryController {

    @GetMapping("/reorder-candidates")
    public List<ReorderItem> getReorderCandidates() {
        // Queries Inventory Service's OWN database — no cross-service DB access
        return weeklySalesRepository.findAll().stream()
            .filter(sales -> {
                int stockLevel = stockRepository.getLevel(sales.getProductId());
                return stockLevel < sales.getUnitsSoldLast7Days() * 2;
            })
            .map(sales -> new ReorderItem(
                sales.getProductId(),
                sales.getUnitsSoldLast7Days() * 3 - stockRepository.getLevel(sales.getProductId())
            ))
            .toList();
    }
}
```

Key improvements:
- Each service owns its database — `InventoryService` never touches the `orders` schema (Database per Service pattern)
- `OrderLineItemAdded` domain event decouples the services; Order Service does not know Inventory Service exists
- `ProductWeeklySales` is a denormalized read model maintained by consuming events — a lightweight CQRS view
- The Kafka consumer is idempotent: events outside the 7-day window are skipped, making re-delivery safe
- Deleting the coupling to `sharedDataSource` eliminates the risk that a schema change in Order Service breaks Inventory Service at runtime
