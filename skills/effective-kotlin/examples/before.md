# Before

Kotlin code written in Java style with `var` everywhere, misused nullability, and index-based loops that ignore idiomatic Kotlin features.

```kotlin
class UserReportGenerator {

    var users: MutableList<User>? = null
    var reportTitle: String? = null
    var includeInactive: Boolean = false

    fun generateSummary(): String? {
        var result = ""
        if (users == null) {
            return null
        }
        result = result + reportTitle + "\n"
        var i = 0
        while (i < users!!.size) {
            val user = users!![i]
            if (includeInactive == false) {
                if (user.active == false) {
                    i++
                    continue
                }
            }
            var line = ""
            line = line + user.name + " (" + user.email + ")"
            if (user.role != null) {
                line = line + " - " + user.role
            }
            result = result + line + "\n"
            i++
        }
        return result
    }
}
```
