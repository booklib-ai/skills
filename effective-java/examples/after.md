# After

An immutable `ShippingAddress` value class built with a fluent Builder, validated at construction time so that no corrupt instance can ever exist.

```java
public final class ShippingAddress {
    private final String recipientName;
    private final String streetLine1;
    private final String streetLine2;   // nullable — optional field
    private final String city;
    private final String stateCode;
    private final String postalCode;
    private final String countryCode;
    private final boolean residential;

    private ShippingAddress(Builder builder) {
        this.recipientName = builder.recipientName;
        this.streetLine1   = builder.streetLine1;
        this.streetLine2   = builder.streetLine2;
        this.city          = builder.city;
        this.stateCode     = builder.stateCode;
        this.postalCode    = builder.postalCode;
        this.countryCode   = builder.countryCode;
        this.residential   = builder.residential;
    }

    public static Builder builder(String recipientName, String streetLine1,
                                  String city, String postalCode, String countryCode) {
        return new Builder(recipientName, streetLine1, city, postalCode, countryCode);
    }

    // Accessors only — no setters
    public String recipientName() { return recipientName; }
    public String streetLine1()   { return streetLine1; }
    public Optional<String> streetLine2() { return Optional.ofNullable(streetLine2); }
    public String city()          { return city; }
    public String stateCode()     { return stateCode; }
    public String postalCode()    { return postalCode; }
    public String countryCode()   { return countryCode; }
    public boolean isResidential(){ return residential; }

    public static final class Builder {
        // Required fields set via constructor
        private final String recipientName;
        private final String streetLine1;
        private final String city;
        private final String postalCode;
        private final String countryCode;
        // Optional fields
        private String streetLine2;
        private String stateCode = "";
        private boolean residential = true;

        private Builder(String recipientName, String streetLine1,
                        String city, String postalCode, String countryCode) {
            this.recipientName = Objects.requireNonNull(recipientName, "recipientName");
            this.streetLine1   = Objects.requireNonNull(streetLine1,   "streetLine1");
            this.city          = Objects.requireNonNull(city,           "city");
            this.postalCode    = Objects.requireNonNull(postalCode,     "postalCode");
            this.countryCode   = Objects.requireNonNull(countryCode,    "countryCode");
        }

        public Builder streetLine2(String val) { this.streetLine2 = val; return this; }
        public Builder stateCode(String val)   { this.stateCode = val;   return this; }
        public Builder commercial()            { this.residential = false; return this; }
        public ShippingAddress build()         { return new ShippingAddress(this); }
    }
}

// Usage — required fields enforced; optional fields have readable names
ShippingAddress addr = ShippingAddress
    .builder("Jane Doe", "742 Evergreen Terrace", "Springfield", "62701", "US")
    .stateCode("IL")
    .commercial()
    .build();
```

Key improvements:
- Builder pattern eliminates the telescoping constructor problem — required fields are in the builder constructor, optional fields use fluent setters (Item 2: Builder when many parameters)
- All fields are `private final` — the class is immutable after construction (Item 17: Minimize mutability)
- `Objects.requireNonNull` validates all required fields at construction time — corrupt objects are impossible to create (Item 49: Validate parameters)
- `Optional<String>` return type for `streetLine2` explicitly signals to callers that this value may be absent (Item 55: Return Optional judiciously)
- `final` class prevents subclasses from breaking immutability guarantees (Item 17)
