# Web Scraping with Python — Scraper Review Checklist

Systematic checklist for reviewing web scrapers against the 18 chapters
from *Web Scraping with Python* by Ryan Mitchell.

---

## 1. Fetching & Connection (Chapters 1, 10–11)

### HTTP Requests
- [ ] **Ch 1 — Error handling** — Are HTTP errors (4xx, 5xx), connection errors, and timeouts caught and handled?
- [ ] **Ch 1 — Response validation** — Is status code checked before parsing? Are non-200 responses handled?
- [ ] **Ch 1 — Timeout configuration** — Are request timeouts set to avoid hanging on unresponsive servers?
- [ ] **Ch 10 — Session usage** — Is `requests.Session()` used for cookie persistence and connection pooling?

### Authentication
- [ ] **Ch 10 — Login handling** — Is login implemented correctly with CSRF tokens and proper POST data?
- [ ] **Ch 10 — Session persistence** — Are cookies maintained across requests for authenticated scraping?
- [ ] **Ch 10 — Credential security** — Are login credentials stored in environment variables, not hardcoded?
- [ ] **Ch 10 — Session expiry** — Is session expiry detected and handled with automatic re-authentication?

### JavaScript Rendering
- [ ] **Ch 11 — Rendering need** — Is JavaScript rendering actually needed, or does the data exist in raw HTML or an API?
- [ ] **Ch 11 — Headless mode** — Is the browser running headless for server/production use?
- [ ] **Ch 11 — Explicit waits** — Are `WebDriverWait` with `expected_conditions` used instead of `time.sleep()`?
- [ ] **Ch 11 — Resource cleanup** — Is `driver.quit()` called in a finally block or context manager?
- [ ] **Ch 11 — Page load strategy** — Is the page load strategy appropriate (normal, eager, none)?

---

## 2. Parsing & Extraction (Chapters 2, 7)

### HTML Parsing
- [ ] **Ch 2 — Parser choice** — Is an appropriate parser used (html.parser, lxml, html5lib)?
- [ ] **Ch 2 — Selector quality** — Are selectors specific enough to avoid false matches but flexible enough to survive minor changes?
- [ ] **Ch 2 — None checking** — Is `find()` result checked for None before accessing attributes or text?
- [ ] **Ch 2 — Multiple strategies** — Are fallback selectors used in case the primary selector fails?
- [ ] **Ch 2 — CSS selectors vs find** — Is `select()` used for complex hierarchical selection where appropriate?

### Data Extraction
- [ ] **Ch 2 — Attribute access** — Is `tag.get('href')` used instead of `tag['href']` to avoid KeyError?
- [ ] **Ch 2 — Text extraction** — Is `get_text(strip=True)` used for clean text content?
- [ ] **Ch 2 — Regex usage** — Are regex patterns compiled and used appropriately (not for HTML parsing)?
- [ ] **Ch 7 — Document handling** — Are non-HTML documents (PDF, Word) handled with appropriate libraries?
- [ ] **Ch 7 — Encoding** — Is character encoding handled correctly? Is UTF-8 enforced?

---

## 3. Crawling & Navigation (Chapters 3–5)

### URL Management
- [ ] **Ch 3 — URL normalization** — Are URLs normalized (resolve relative, strip fragments, handle trailing slashes)?
- [ ] **Ch 3 — Deduplication** — Is a visited set maintained? Are URLs checked before adding to queue?
- [ ] **Ch 3 — Scope control** — Is crawl scope defined (same domain, specific paths, depth limit)?
- [ ] **Ch 3 — Relative URL resolution** — Is `urljoin` used to resolve relative links against the base URL?

### Crawl Strategy
- [ ] **Ch 3 — Traversal order** — Is the right traversal used (BFS for breadth, DFS for depth)?
- [ ] **Ch 4 — Layout handling** — Are different page layouts detected and parsed appropriately?
- [ ] **Ch 4 — Data normalization** — Is extracted data normalized to a consistent schema across pages?
- [ ] **Ch 3 — Pagination** — Is pagination handled correctly (next links, page numbers, cursor)?

### Scrapy-Specific
- [ ] **Ch 5 — Item definitions** — Are Scrapy Items defined for structured data extraction?
- [ ] **Ch 5 — Pipeline usage** — Are item pipelines used for validation, cleaning, and storage?
- [ ] **Ch 5 — Rules configuration** — Are CrawlSpider rules properly configured with LinkExtractor?
- [ ] **Ch 5 — Settings tuning** — Are CONCURRENT_REQUESTS, DOWNLOAD_DELAY, and AUTOTHROTTLE configured?
- [ ] **Ch 5 — Logging** — Is logging configured at the appropriate level for production?

---

## 4. Data Storage (Chapter 6)

### Storage Patterns
- [ ] **Ch 6 — Format choice** — Is the right storage format used (CSV for simple, database for relational, JSON for nested)?
- [ ] **Ch 6 — Duplicate prevention** — Are duplicates detected and handled (UPSERT, unique constraints)?
- [ ] **Ch 6 — Batch operations** — Are database writes batched instead of per-row for efficiency?
- [ ] **Ch 6 — Connection management** — Are database connections properly opened, pooled, and closed?

### Data Integrity
- [ ] **Ch 6 — Schema enforcement** — Is extracted data validated against expected schema before storage?
- [ ] **Ch 6 — Raw preservation** — Is raw HTML/response stored alongside extracted data for re-parsing?
- [ ] **Ch 6 — Encoding handling** — Are files written with explicit UTF-8 encoding?
- [ ] **Ch 6 — Error on write** — Are storage errors caught and handled (disk full, DB connection lost)?

---

## 5. Data Quality (Chapters 8, 9, 15)

### Cleaning
- [ ] **Ch 8 — Whitespace normalization** — Is whitespace stripped and normalized in extracted text?
- [ ] **Ch 8 — Unicode normalization** — Is Unicode text normalized (NFKD or NFC) for consistency?
- [ ] **Ch 8 — Type conversion** — Are strings converted to appropriate types (int, float, date) with error handling?
- [ ] **Ch 8 — Pattern cleaning** — Are regex patterns used to extract clean data from messy strings?

### Testing
- [ ] **Ch 15 — Parser unit tests** — Are parsing functions tested with saved HTML fixtures?
- [ ] **Ch 15 — Edge case tests** — Are missing elements, empty pages, and malformed HTML tested?
- [ ] **Ch 15 — Integration tests** — Is the full pipeline tested end-to-end?
- [ ] **Ch 15 — Change detection** — Is there monitoring for when the target site changes structure?
- [ ] **Ch 15 — CI integration** — Are scraper tests automated in a CI pipeline?

---

## 6. Resilience & Performance (Chapters 14, 16)

### Anti-Detection
- [ ] **Ch 14 — User-Agent** — Is a realistic User-Agent header set? Is rotation implemented for scale?
- [ ] **Ch 14 — Request headers** — Are Accept, Accept-Language, and other standard headers included?
- [ ] **Ch 14 — Request delays** — Are random delays added between requests (not fixed intervals)?
- [ ] **Ch 14 — Cookie handling** — Are cookies accepted and maintained properly?
- [ ] **Ch 14 — Honeypot avoidance** — Are hidden links (display:none, visibility:hidden) detected and avoided?

### Performance
- [ ] **Ch 16 — Parallelism** — Is parallel scraping used for large-scale jobs (threading or multiprocessing)?
- [ ] **Ch 16 — Thread safety** — Are shared data structures properly protected with locks or queues?
- [ ] **Ch 16 — Per-domain limits** — Are concurrent requests limited per domain even with parallel scraping?
- [ ] **Ch 16 — Graceful shutdown** — Can the scraper shut down cleanly, saving state for resumption?

### Error Recovery
- [ ] **Ch 14 — Retry logic** — Are transient errors retried with backoff? Are permanent errors skipped?
- [ ] **Ch 14 — Block detection** — Are 403/captcha responses detected as potential blocks?
- [ ] **Ch 16 — Worker isolation** — Does one worker's failure not crash the entire scraper?
- [ ] **Ch 14 — State persistence** — Can the scraper resume from where it left off after a crash?

---

## 7. Ethics & Legal (Chapters 17–18)

### Compliance
- [ ] **Ch 18 — robots.txt** — Is robots.txt fetched and respected before crawling?
- [ ] **Ch 18 — Terms of Service** — Has the target site's ToS been reviewed for scraping restrictions?
- [ ] **Ch 18 — Rate respect** — Is the scraping rate respectful of server resources?
- [ ] **Ch 18 — Data rights** — Is scraped data handled in compliance with copyright and privacy laws?
- [ ] **Ch 18 — GDPR compliance** — If scraping personal data, are GDPR obligations met?

### Anonymity & Infrastructure
- [ ] **Ch 17 — Proxy usage** — Are proxies used appropriately when needed for scale or anonymity?
- [ ] **Ch 17 — Tor appropriateness** — Is Tor used only when genuinely needed, not as a default?
- [ ] **Ch 17 — IP verification** — Is proxy/Tor IP verified before scraping sensitive targets?
- [ ] **Ch 14 — Identification** — Does the User-Agent identify the scraper and provide contact info?

---

## Quick Review Workflow

1. **Fetching pass** — Verify request handling, error handling, session usage, JS rendering needs
2. **Parsing pass** — Check selector quality, None handling, defensive parsing, fallback strategies
3. **Crawling pass** — Verify URL management, deduplication, pagination, scope control
4. **Storage pass** — Check data format, duplicate handling, raw preservation, encoding
5. **Quality pass** — Verify data cleaning, testing coverage, change detection
6. **Resilience pass** — Check rate limiting, parallelism, retry logic, anti-detection
7. **Ethics pass** — Verify robots.txt compliance, legal awareness, respectful crawling
8. **Prioritize findings** — Rank by severity: legal risk > data loss > reliability > performance > best practices

## Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Legal risk, data loss, or server harm | Ignoring robots.txt, no rate limiting (hammering server), hardcoded credentials, GDPR violations |
| **High** | Reliability or data quality issues | No error handling, missing None checks, no session management, no deduplication |
| **Medium** | Performance, maintainability, or operational gaps | No parallel scraping for large jobs, no testing, fixed delays instead of random, no logging |
| **Low** | Best practice improvements | Missing User-Agent rotation, no raw HTML storage, no change detection, minor code organization |
