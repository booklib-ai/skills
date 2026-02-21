# After

Idiomatic Kotlin with `val` properties, non-null types where absence is not meaningful, and a functional pipeline replacing the manual while loop.

```kotlin
class UserReportGenerator(
    private val users: List<User>,
    private val reportTitle: String,
    private val includeInactive: Boolean = false,
) {

    fun generateSummary(): String {
        val activeUsers = if (includeInactive) users else users.filter { it.active }

        val lines = activeUsers.map { user ->
            buildString {
                append("${user.name} (${user.email})")
                user.role?.let { append(" - $it") }
            }
        }

        return buildString {
            appendLine(reportTitle)
            lines.forEach(::appendLine)
        }
    }
}
```

Key improvements:
- Constructor parameters replace mutable properties (Item 1: Limit Mutability) — the generator is now immutable after construction
- `users: List<User>` and `reportTitle: String` are non-null types; nullability would only be meaningful if absence were valid (Item 8: Handle Nulls Properly)
- `filter`, `map`, and `buildString` replace the manual `while` index loop — idiomatic stdlib use (Item 20: Use stdlib algorithms)
- `user.role?.let { append(" - $it") }` replaces the null-check `if` block with a safe-call chain (Item 8)
- `includeInactive = false` as a default parameter eliminates the need for an overloaded constructor (Item 34: Consider named and optional args)
- `generateSummary()` returns `String` (non-null) — the empty report is a valid empty string, not `null` (Item 7: Prefer null or Failure over exceptions for expected failures)
