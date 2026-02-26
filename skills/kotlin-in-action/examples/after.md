# After

Idiomatic Kotlin using a sealed interface for channels, safe-call operators, named parameters, and extension functions — eliminating all manual null checks and string comparisons.

```kotlin
// Sealed interface models exactly the valid channels — exhaustive when is enforced
sealed interface NotificationChannel {
    data class Email(val address: String) : NotificationChannel
    data class Sms(val phoneNumber: String) : NotificationChannel
}

// Extension function resolves the preferred channel from a User
fun User.preferredChannel(): NotificationChannel? = when {
    email != null       -> NotificationChannel.Email(email)
    phoneNumber != null -> NotificationChannel.Sms(phoneNumber)
    else                -> null
}

class NotificationService(
    private val emailSender: EmailSender,
    private val smsSender: SmsSender,
) {

    fun sendNotification(user: User, message: String, channel: NotificationChannel) {
        require(message.isNotBlank()) { "Notification message must not be blank" }

        when (channel) {
            is NotificationChannel.Email -> {
                val subject = "Notification for ${user.firstName} ${user.lastName}"
                emailSender.send(to = channel.address, subject = subject, body = message)
            }
            is NotificationChannel.Sms -> {
                smsSender.send(to = channel.phoneNumber, body = message)
            }
        }
    }
}

// Usage — caller resolves channel; service focuses on delivery
fun notifyUser(user: User, message: String, service: NotificationService) {
    user.preferredChannel()
        ?.let { channel -> service.sendNotification(user, message, channel) }
        ?: logger.warn("No notification channel available for user ${user.id}")
}
```

Key improvements:
- `sealed interface NotificationChannel` replaces the `String` channel parameter — the compiler enforces exhaustive `when` and eliminates the "Unknown channel" else branch (Ch 4: Sealed classes)
- `User?` parameter becomes non-null `User` — the caller is responsible for ensuring a valid user exists; null-safety is pushed to the boundary (Ch 7: Null safety)
- `user.preferredChannel()` extension function encapsulates the channel-resolution logic outside the service class (Ch 3: Extension functions)
- `require(message.isNotBlank())` replaces silent println for invalid input (Effective Kotlin Item 5: Specify your expectations on arguments)
- Named parameters `to =`, `subject =`, `body =` make the send calls self-documenting (Ch 3: Named arguments)
- String template `"${user.firstName} ${user.lastName}"` replaces concatenation (Ch 2: String templates)
