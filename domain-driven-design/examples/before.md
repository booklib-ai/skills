# Before

An anemic domain model where the `Order` class is a passive data container with no behavior, and all business logic is scattered across `OrderService`.

```java
// Anemic entity — just a data bag
public class Order {
    public Long id;
    public List<OrderLine> lines;
    public String status;
    public BigDecimal totalAmount;
    public String customerId;
}

// All logic lives in the service
public class OrderService {

    public void addItem(Order order, Product product, int quantity) {
        OrderLine line = new OrderLine();
        line.productId = product.id;
        line.quantity = quantity;
        line.unitPrice = product.price;
        order.lines.add(line);
        order.totalAmount = order.lines.stream()
            .map(l -> l.unitPrice.multiply(BigDecimal.valueOf(l.quantity)))
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    public void cancel(Order order) {
        if (!order.status.equals("PENDING") && !order.status.equals("CONFIRMED")) {
            throw new IllegalStateException("Cannot cancel");
        }
        order.status = "CANCELLED";
    }

    public void confirm(Order order) {
        if (order.lines == null || order.lines.isEmpty()) {
            throw new IllegalStateException("Cannot confirm empty order");
        }
        order.status = "CONFIRMED";
    }
}
```
