# Before

An `InventoryService` that directly queries the `orders` database table owned by another service, creating tight coupling and a shared-database anti-pattern.

```java
@RestController
@RequestMapping("/inventory")
public class InventoryController {

    @Autowired
    private DataSource sharedDataSource; // connected to the orders DB

    @GetMapping("/reorder-candidates")
    public List<ReorderItem> getReorderCandidates() {
        List<ReorderItem> candidates = new ArrayList<>();

        // Directly querying the Order Service's database table
        try (Connection conn = sharedDataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(
                 "SELECT product_id, SUM(quantity) as sold_qty " +
                 "FROM orders.order_lines " +
                 "WHERE created_at > NOW() - INTERVAL 7 DAY " +
                 "GROUP BY product_id")) {

            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                String productId = rs.getString("product_id");
                int soldQty = rs.getInt("sold_qty");
                int stockLevel = getStockLevel(productId);
                if (stockLevel < soldQty * 2) {
                    candidates.add(new ReorderItem(productId, soldQty * 3 - stockLevel));
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        return candidates;
    }
}
```
