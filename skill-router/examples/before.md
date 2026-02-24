# Before: Unrouted Code Review Request

## User Message

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

## What Happens Without Routing

The AI must guess which lens to apply:

- Does the user want **Java-specific** advice (Effective Java)? → Bloch would focus on generics, raw types, and static factory methods
- Do they want **code quality** advice (Clean Code)? → Martin would focus on naming, flag arguments, static mutable state
- Do they want **design pattern** advice (Design Patterns)? → Gang of Four would examine whether a Command or Strategy pattern fits
- Do they want **domain modeling** advice (DDD)? → Evans would ask about Aggregates and Value Objects

**Result:** The AI either picks one arbitrarily, tries to cover all four superficially, or asks a clarifying question that could have been avoided.

The user gets a scattered review that's 40% relevant from four different books instead of a sharp, deep review from the right one.
