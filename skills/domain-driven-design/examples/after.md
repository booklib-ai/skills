# After

`Order` becomes a rich aggregate root that owns its invariants and exposes domain-language behavior; `OrderService` becomes a thin application-layer coordinator.

```java
// Rich aggregate root — enforces all invariants internally
public class Order {
    private final OrderId id;
    private final List<OrderLine> lines = new ArrayList<>();
    private OrderStatus status;
    private Money total;

    private Order(OrderId id, CustomerId customerId) {
        this.id = id;
        this.status = OrderStatus.PENDING;
        this.total = Money.ZERO;
    }

    public static Order place(OrderId id, CustomerId customerId) {
        return new Order(id, customerId);
    }

    public void addItem(Product product, int quantity) {
        Validate.isTrue(quantity > 0, "Quantity must be positive");
        Validate.isTrue(status == OrderStatus.PENDING, "Cannot modify a non-pending order");
        lines.add(OrderLine.of(product.getId(), product.getPrice(), quantity));
        recalculateTotal();
    }

    public void confirm() {
        if (lines.isEmpty()) {
            throw new DomainException("Cannot confirm an order with no items");
        }
        this.status = OrderStatus.CONFIRMED;
    }

    public void cancel() {
        if (!status.isCancellable()) {
            throw new DomainException("Order in status " + status + " cannot be cancelled");
        }
        this.status = OrderStatus.CANCELLED;
    }

    private void recalculateTotal() {
        this.total = lines.stream()
            .map(OrderLine::lineTotal)
            .reduce(Money.ZERO, Money::add);
    }

    // Getters return immutable views only
    public List<OrderLine> lines() { return Collections.unmodifiableList(lines); }
    public Money total()           { return total; }
    public OrderStatus status()    { return status; }
}

// Application service is thin — orchestrates, does not contain business rules
public class PlaceOrderUseCase {
    private final OrderRepository orderRepository;
    private final ProductRepository productRepository;

    public OrderId execute(PlaceOrderCommand cmd) {
        Order order = Order.place(OrderId.generate(), cmd.customerId());
        for (var item : cmd.requestedItems()) {
            Product product = productRepository.findById(item.productId())
                .orElseThrow(() -> new ProductNotFoundException(item.productId()));
            order.addItem(product, item.quantity());
        }
        order.confirm();
        orderRepository.save(order);
        return order.getId();
    }
}
```

Key improvements:
- Business rules (`confirm`, `cancel`, `addItem`) live inside `Order` — the anemic model anti-pattern is eliminated
- `Order.status.isCancellable()` encapsulates the cancellation-eligibility rule in an enum method rather than in a service
- External code cannot corrupt the aggregate: `lines` is returned as an unmodifiable view; `total` is always recalculated internally
- `OrderService` is renamed to `PlaceOrderUseCase` per the Ubiquitous Language (application command, not a generic "service")
- `Money` is a Value Object, preventing `double` arithmetic errors on financial amounts (Primitive Obsession eliminated)
