# Before

Kotlin code written with Java-style null checks, no extension functions, and no use of sealed classes or safe-call operators.

```kotlin
class NotificationService(
    private val emailSender: EmailSender,
    private val smsSender: SmsSender
) {

    fun sendNotification(user: User?, message: String?, channel: String) {
        if (user == null) {
            println("User is null")
            return
        }
        if (message == null || message.isEmpty()) {
            println("Message is empty")
            return
        }

        if (channel == "EMAIL") {
            if (user.email != null) {
                val subject = "Notification for " + user.firstName + " " + user.lastName
                emailSender.send(user.email, subject, message)
            } else {
                println("No email for user " + user.id)
            }
        } else if (channel == "SMS") {
            if (user.phoneNumber != null) {
                smsSender.send(user.phoneNumber, message)
            } else {
                println("No phone for user " + user.id)
            }
        } else {
            println("Unknown channel: " + channel)
        }
    }
}
```
