# After: Routed Code Review Request

## User Message (same as before)

> "Can you review my code? I want to make it better."
>
> ```java
> public class OrderProcessor {
>     private static List<Map<String, Object>> pendingOrders = new ArrayList<>();
>     
>     public static int process(Map<String, Object> o, boolean isAdmin, boolean sendEmail) {
>         if (o == null) return -1;
>         if (o.get("status").equals("pending")) {
>             if (isAdmin) {
>                 o.put("status", "approved");
>                 pendingOrders.remove(o);
>                 if (sendEmail) {
>                     System.out.println("Sending email to: " + o.get("customerEmail"));
>                 }
>                 return 0;
>             }
>         }
>         return -2;
>     }
> }
> ```

## Skill Router Output

**Primary skill:** `clean-code-reviewer`
**Why:** The user wants general code quality improvement for a Java class. The dominant issues are language-agnostic: poor naming (`o`, `isAdmin` flag arg, magic return codes), static mutable state, nested conditionals, and multiple responsibilities — all Clean Code's territory.
**Secondary (optional):** `effective-java` — after the Clean Code review, apply Effective Java for Java-specific improvements: replace `Map<String, Object>` with a typed class (Item 64: refer to objects by their interfaces), use enums instead of int return codes (Item 34).
**Don't apply:** `domain-driven-design` — while an Order is a domain concept, applying DDD here would produce advice about Aggregates and Bounded Contexts that is premature. Fix the code quality first.

---

## What the Clean Code Review Produces

With the right skill applied, the review is sharp and specific:

### Issues Found

🔴 **Critical — F3: Flag Arguments**
`isAdmin` and `sendEmail` are boolean flags — the function does 4 different things depending on their combination. Split into `approveAsAdmin()` and keep email logic separate.

🔴 **Critical — Shared Mutable Static State (Ch. 13)**
`pendingOrders` is a static mutable list — not thread-safe and makes the class impossible to test in isolation.

🔴 **Critical — Error Codes Instead of Exceptions (Ch. 7)**
Returning `-1` and `-2` forces callers to check magic numbers. Throw `InvalidOrderException` and `UnauthorizedOperationException` instead.

🟡 **Important — N1: Poor Naming**
`o`, `process` — names reveal nothing. `o` → `order`, `process` → `approveOrder`.

🟡 **Important — G30: Function Does Multiple Things**
`process()` validates, approves, removes from list, and sends email. Each is a separate responsibility.

🟢 **Suggestion — G25: Magic Numbers**
Return codes `-1`, `-2` should be named constants at minimum, or better: exceptions.

### Result

The user gets a **focused, actionable review** from one authoritative source — not a scattered survey of four books.
