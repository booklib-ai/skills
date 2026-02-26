# Before

A Java method that handles order discount calculation with poor naming, deep nesting, and multiple responsibilities mixed together.

```java
public double calc(Order o, String t, boolean f) {
    double r = 0;
    if (o != null) {
        if (o.getItems() != null && o.getItems().size() > 0) {
            for (Item i : o.getItems()) {
                if (i.getQty() > 0) {
                    double p = i.getPrice() * i.getQty();
                    if (t.equals("PREMIUM")) {
                        p = p * 0.85;
                    } else if (t.equals("MEMBER")) {
                        p = p * 0.90;
                    } else {
                        p = p * 1.0;
                    }
                    if (f) {
                        // free shipping promo
                        if (p > 100) {
                            p = p - 5.99;
                        }
                    }
                    r = r + p;
                }
            }
        }
    }
    return r;
}
```
