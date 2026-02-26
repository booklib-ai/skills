# After

The discount calculation is split into single-responsibility methods with intention-revealing names, guard clauses replacing nesting, and constants replacing magic numbers.

```java
private static final double PREMIUM_DISCOUNT = 0.85;
private static final double MEMBER_DISCOUNT  = 0.90;
private static final double SHIPPING_CREDIT  = 5.99;
private static final double FREE_SHIPPING_THRESHOLD = 100.00;

public double calculateOrderTotal(Order order, CustomerTier tier, boolean freeShippingPromo) {
    if (order == null || order.getItems() == null) {
        return 0;
    }
    return order.getItems().stream()
            .filter(item -> item.getQty() > 0)
            .mapToDouble(item -> calculateLineTotal(item, tier, freeShippingPromo))
            .sum();
}

private double calculateLineTotal(Item item, CustomerTier tier, boolean freeShippingPromo) {
    double subtotal = item.getPrice() * item.getQty();
    double discounted = applyTierDiscount(subtotal, tier);
    return applyShippingCredit(discounted, freeShippingPromo);
}

private double applyTierDiscount(double subtotal, CustomerTier tier) {
    return switch (tier) {
        case PREMIUM -> subtotal * PREMIUM_DISCOUNT;
        case MEMBER  -> subtotal * MEMBER_DISCOUNT;
        default      -> subtotal;
    };
}

private double applyShippingCredit(double amount, boolean freeShippingPromo) {
    if (!freeShippingPromo || amount <= FREE_SHIPPING_THRESHOLD) {
        return amount;
    }
    return amount - SHIPPING_CREDIT;
}
```

Key improvements:
- Descriptive name `calculateOrderTotal` states exactly what the method does (G20: Function Names Should Say What They Do)
- Guard clause at the top of the public method eliminates two levels of nesting (G28: Encapsulate Conditionals)
- Each private method does exactly one thing: calculate, discount, or apply credit (G30: Functions Should Do One Thing)
- Magic numbers `0.85`, `0.90`, `5.99`, `100` extracted to named constants (G25: Replace Magic Numbers with Named Constants)
- `String` tier replaced with `CustomerTier` enum, enabling exhaustive `switch` (J3: Constants versus Enums)
