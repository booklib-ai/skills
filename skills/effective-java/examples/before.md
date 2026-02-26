# Before

A Java class representing a shipping address with public mutable fields, no validation, and no safe construction — making it trivial to create corrupt objects.

```java
public class ShippingAddress {
    public String recipientName;
    public String streetLine1;
    public String streetLine2;
    public String city;
    public String stateCode;
    public String postalCode;
    public String countryCode;
    public boolean isResidential;

    public ShippingAddress() {}

    public ShippingAddress(String recipientName, String streetLine1,
                           String streetLine2, String city, String stateCode,
                           String postalCode, String countryCode,
                           boolean isResidential) {
        this.recipientName = recipientName;
        this.streetLine1 = streetLine1;
        this.streetLine2 = streetLine2;
        this.city = city;
        this.stateCode = stateCode;
        this.postalCode = postalCode;
        this.countryCode = countryCode;
        this.isResidential = isResidential;
    }
}

// Usage — nothing prevents corrupt construction
ShippingAddress addr = new ShippingAddress();
addr.city = "Austin";
// postalCode, countryCode, recipientName all null — silently broken
```
