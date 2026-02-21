# After

Each payment method is extracted into its own `PaymentStrategy` implementation behind a common interface, making it trivial to add new methods without touching existing code.

```kotlin
// Strategy interface — the contract every payment method must fulfill
interface PaymentStrategy {
    fun process(order: Order): PaymentResult
}

// One class per payment method — focused, testable, replaceable
class CreditCardPaymentStrategy : PaymentStrategy {
    override fun process(order: Order): PaymentResult {
        val token = CreditCardGateway.tokenize(order.cardNumber)
        val charge = CreditCardGateway.charge(token, order.totalAmount)
        return PaymentResult(success = charge.success, transactionId = charge.id,
                             errorMessage = charge.error.takeIf { !charge.success })
    }
}

class PayPalPaymentStrategy : PaymentStrategy {
    override fun process(order: Order): PaymentResult {
        val session = PayPalClient.createSession(order.paypalEmail)
        val payment = PayPalClient.executePayment(session, order.totalAmount)
        return PaymentResult(success = payment.approved, transactionId = payment.token)
    }
}

class BankTransferPaymentStrategy : PaymentStrategy {
    override fun process(order: Order): PaymentResult {
        val ref = BankTransferService.initiate(order.iban, order.totalAmount)
        return PaymentResult(success = ref != null, transactionId = ref,
                             errorMessage = "Bank transfer initiation failed".takeIf { ref == null })
    }
}

// Context: delegates entirely to the injected strategy
class PaymentProcessor(private val strategy: PaymentStrategy) {
    fun process(order: Order): PaymentResult = strategy.process(order)
}

// Usage — caller selects strategy; PaymentProcessor is unaware of the type
val processor = PaymentProcessor(CreditCardPaymentStrategy())
val result = processor.process(order)
```

Key improvements:
- If/else chain replaced with Strategy pattern — adding a new payment method requires a new class only, no changes to `PaymentProcessor` (Open-Closed Principle)
- Each strategy is independently testable with a mock `Order`
- `PaymentProcessor` depends on the `PaymentStrategy` abstraction, not concrete gateway classes (Dependency Inversion Principle)
- Responsibility for "how to pay" is encapsulated inside each strategy class (Encapsulate What Varies)
- Caller selects strategy through constructor injection, enabling runtime switching and easy testing
