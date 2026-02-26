# Before

Kotlin payment processing code that uses a brittle if/else chain to select behavior, violating the Open-Closed Principle and making it hard to add new payment methods.

```kotlin
class PaymentProcessor {

    fun process(order: Order, method: String): PaymentResult {
        return if (method == "CREDIT_CARD") {
            val token = CreditCardGateway.tokenize(order.cardNumber)
            val charge = CreditCardGateway.charge(token, order.totalAmount)
            if (charge.success) {
                PaymentResult(success = true, transactionId = charge.id)
            } else {
                PaymentResult(success = false, errorMessage = charge.error)
            }
        } else if (method == "PAYPAL") {
            val session = PayPalClient.createSession(order.paypalEmail)
            val payment = PayPalClient.executePayment(session, order.totalAmount)
            PaymentResult(success = payment.approved, transactionId = payment.token)
        } else if (method == "BANK_TRANSFER") {
            val ref = BankTransferService.initiate(order.iban, order.totalAmount)
            PaymentResult(success = ref != null, transactionId = ref)
        } else {
            PaymentResult(success = false, errorMessage = "Unknown payment method: $method")
        }
    }
}
```
