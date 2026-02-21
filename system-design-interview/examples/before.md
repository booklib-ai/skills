# Before

A system design proposal for a URL shortener that jumps straight to implementation details without any capacity estimation, API definition, or structured component breakdown.

```
DESIGN PROPOSAL: URL Shortener Service

Let's just use a database with two columns: short_code and original_url.
When someone hits our endpoint, we look up the short_code and redirect.

We can use MySQL. The table will look like:

  CREATE TABLE urls (
    short_code VARCHAR(8) PRIMARY KEY,
    original_url TEXT NOT NULL
  );

For generating short codes, we'll use UUID and take the first 8 characters.
If there's a collision, just retry.

For the web layer, we'll run a Flask app on a single server. If it gets slow
we can add more Flask instances behind a load balancer later.

Caching: we could add Redis if needed.

That should work fine for our use case. Let's start coding.
```
