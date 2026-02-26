# Web Scraping with Python — Practices Catalog

Chapter-by-chapter catalog of practices from *Web Scraping with Python*
by Ryan Mitchell for scraper building.

---

## Chapter 1: Your First Web Scraper

### Basic Fetching
- **urllib.request** — `urlopen(url)` returns an HTTPResponse object; read `.read()` for HTML bytes
- **requests library** — Preferred over urllib; `requests.get(url)` with headers, params, timeout support
- **Error handling** — Catch `HTTPError` (4xx/5xx), `URLError` (server not found), and connection timeouts
- **Response checking** — Always check `response.status_code`; handle 403 (forbidden), 404 (not found), 500 (server error)

### BeautifulSoup Basics
- **Creating soup** — `BeautifulSoup(html, 'html.parser')` or use `'lxml'` for speed
- **Direct tag access** — `soup.h1`, `soup.title` returns first matching tag
- **Tag attributes** — `tag.attrs` returns dict; `tag['href']` for specific attribute; `tag.get_text()` for text content
- **None checking** — Always check if `soup.find()` returns None before accessing attributes

---

## Chapter 2: Advanced HTML Parsing

### find and findAll
- **`find(tag, attributes, recursive, text, keywords)`** — Returns first matching element
- **`findAll(tag, attributes, recursive, text, limit, keywords)`** — Returns list of all matches
- **Attribute filtering** — `find('div', {'class': 'price'})`, `find('span', {'id': 'result'})`
- **Multiple tags** — `findAll(['h1', 'h2', 'h3'])` matches any of the listed tags
- **Text search** — `findAll(text='exact match')` or `findAll(text=re.compile('pattern'))`

### CSS Selectors
- **`select(selector)`** — Use CSS selectors: `soup.select('div.content > p')`, `soup.select('#main .item')`
- **Common selectors** — `tag`, `.class`, `#id`, `tag.class`, `parent > child`, `ancestor descendant`, `tag[attr=val]`
- **Pseudo-selectors** — `:nth-of-type()`, `:first-child`, etc. for positional selection

### Navigating the DOM Tree
- **Children** — `tag.children` (direct children iterator), `tag.descendants` (all descendants)
- **Siblings** — `tag.next_sibling`, `tag.previous_sibling`, `tag.next_siblings` (iterator)
- **Parents** — `tag.parent`, `tag.parents` (iterator up to document root)
- **Navigation tip** — NavigableString objects (text nodes) count as siblings; use `.find_next_sibling('tag')` to skip

### Regular Expressions with BeautifulSoup
- **Regex in find** — `soup.find('img', {'src': re.compile(r'\.jpg$')})` matches pattern against attribute
- **Regex in findAll** — `soup.findAll('a', {'href': re.compile(r'^/wiki/')})` for link patterns
- **Text regex** — `soup.findAll(text=re.compile(r'\$[\d,]+'))` for finding price patterns

### Lambda Functions
- **Lambda filters** — `soup.find_all(lambda tag: len(tag.attrs) == 2)` for custom tag filtering
- **Complex conditions** — Combine tag name, attributes, text content in lambda for precise selection

---

## Chapter 3: Writing Web Crawlers

### Single-Domain Crawling
- **Internal link collection** — Find all `<a>` tags; filter for same-domain links using `urlparse`
- **URL normalization** — Resolve relative URLs with `urljoin`; strip fragments and query strings for dedup
- **Visited tracking** — Maintain a `set()` of visited URLs; check before fetching
- **Breadth-first** — Use a queue (collections.deque) for BFS traversal of site
- **Depth-first** — Use a stack (list) for DFS; useful for deep hierarchical sites

### Building Robust Crawlers
- **Recursive crawling** — Function that fetches page, extracts links, recurses on unvisited links
- **Data extraction during crawl** — Extract target data while crawling; don't just collect URLs
- **Depth limiting** — Set maximum crawl depth to prevent infinite recursion
- **URL deduplication** — Normalize URLs before adding to visited set; handle trailing slashes, www prefix

---

## Chapter 4: Web Crawling Models

### Planning a Crawl
- **Site mapping** — Understand site structure before coding; identify URL patterns, pagination, categories
- **Crawl scope** — Define which pages/sections to include or exclude
- **Data schema** — Define what to extract before building; normalize across different page layouts

### Handling Different Layouts
- **Template detection** — Sites may use different templates for different content types
- **Conditional parsing** — Check page type (product vs category vs article) and apply appropriate parser
- **Data normalization** — Map different field names/formats from different layouts to a unified schema

### Cross-Site Crawling
- **Multi-domain** — Maintain per-domain settings (delays, selectors, credentials)
- **Link following policies** — Decide which external links to follow; whitelist/blacklist domains
- **Politeness per domain** — Track per-domain request timing; respect each site's robots.txt

---

## Chapter 5: Scrapy

### Scrapy Architecture
- **Spider** — Defines how to crawl and parse; subclass `scrapy.Spider`; implement `parse()` method
- **Items** — Structured data containers; define fields with `scrapy.Item` and `scrapy.Field()`
- **Pipelines** — Process items after extraction; validate, clean, store to database/file
- **Middleware** — Hook into request/response processing; add headers, proxy rotation, retry logic
- **Settings** — Configure concurrency (`CONCURRENT_REQUESTS`), delays (`DOWNLOAD_DELAY`), user agent, etc.

### CrawlSpider
- **Rules** — Define `Rule(LinkExtractor(...), callback=...)` for automatic link following
- **LinkExtractor** — Filter links by `allow` (regex), `deny`, `restrict_css`, `restrict_xpaths`
- **Callback** — Assign parse methods to different URL patterns; `follow=True` for recursive crawling

### Scrapy Best Practices
- **Item loaders** — Use `ItemLoader` for cleaner extraction with input/output processors
- **Logging** — Configure log levels (`LOG_LEVEL = 'INFO'`); log to file for production runs
- **Autothrottle** — Enable `AUTOTHROTTLE_ENABLED` for adaptive request pacing
- **Feed exports** — Built-in export to JSON, CSV, XML via `-o output.json`
- **Contracts** — Add docstring-based contracts for spider testing

---

## Chapter 6: Storing Data

### File Storage
- **CSV** — Use `csv.writer` or `csv.DictWriter`; handle encoding with `encoding='utf-8'`
- **JSON** — Use `json.dump()` for structured data; JSON Lines for streaming/appending
- **Raw files** — Download images, PDFs with `urllib.request.urlretrieve()` or `requests.get()` with streaming

### Database Storage
- **MySQL** — Use `pymysql` connector; parameterized queries to prevent SQL injection
- **PostgreSQL** — Use `psycopg2`; connection pooling for concurrent scrapers
- **SQLite** — Use built-in `sqlite3` for lightweight local storage; good for prototyping
- **Schema design** — Design tables to match extracted data; use appropriate types; add indexes on lookup columns

### Email Integration
- **smtplib** — Send scraped data or alerts via email; useful for monitoring scraper results
- **Notifications** — Alert on scraper failures, unusual data patterns, or completion

### Storage Best Practices
- **Idempotent storage** — Check for duplicates before inserting; use UPSERT patterns
- **Raw preservation** — Store raw HTML alongside extracted data for re-parsing capability
- **Batch operations** — Use bulk inserts for efficiency; commit in batches, not per-row
- **Connection management** — Use context managers; close connections properly; handle reconnection

---

## Chapter 7: Reading Documents

### PDF Extraction
- **PDFMiner** — Extract text from PDFs; handle multi-column layouts and tables
- **Page-by-page** — Process PDFs page by page for memory efficiency
- **Tables in PDFs** — Use tabula-py or camelot for structured table extraction

### Word Documents
- **python-docx** — Read `.docx` files; extract paragraphs, tables, headers
- **Older formats** — Handle `.doc` files with antiword or textract

### Encoding
- **Character detection** — Use `chardet` to detect file encoding when unknown
- **UTF-8 normalization** — Convert all text to UTF-8; handle BOM (Byte Order Mark)
- **HTML encoding** — Read `<meta charset>` tag; handle entity references (`&amp;`, `&lt;`)

---

## Chapter 8: Cleaning Dirty Data

### String Normalization
- **Whitespace** — Strip leading/trailing whitespace; normalize internal whitespace (multiple spaces to one)
- **Unicode normalization** — Use `unicodedata.normalize('NFKD', text)` for consistent Unicode representation
- **Case normalization** — Lowercase for comparison; preserve original for display

### Regex Cleaning
- **Pattern extraction** — Use regex groups to extract structured data from messy text (prices, dates, phone numbers)
- **Substitution** — `re.sub()` to remove or replace unwanted characters and patterns
- **Compiled patterns** — Pre-compile frequently used patterns with `re.compile()` for performance

### Data Normalization
- **Date formats** — Parse various date formats with `dateutil.parser`; store in ISO 8601
- **Number formats** — Handle commas, currency symbols, percentage signs; convert to numeric types
- **Address normalization** — Standardize address components; handle abbreviations

### OpenRefine
- **Faceting** — Group similar values to find inconsistencies
- **Clustering** — Automatically find and merge similar values (fingerprint, n-gram, etc.)
- **GREL expressions** — Transform data with OpenRefine's expression language

---

## Chapter 9: Natural Language Processing

### Text Analysis
- **N-grams** — Extract sequences of N words; useful for finding common phrases and patterns
- **Frequency analysis** — Count word/phrase frequencies; identify key topics in scraped text
- **Stop words** — Filter common words (the, is, at) to focus on meaningful content

### Markov Models
- **Text generation** — Build Markov chains from scraped text; generate similar-style text
- **Chain order** — Higher order (2-gram, 3-gram) produces more coherent but less varied output

### NLTK
- **Tokenization** — Split text into words and sentences with NLTK tokenizers
- **Part-of-speech tagging** — Tag words as nouns, verbs, etc. for structured extraction
- **Named entity recognition** — Extract names, organizations, locations from text
- **Stemming/lemmatization** — Reduce words to base forms for better matching and analysis

---

## Chapter 10: Crawling Through Forms and Logins

### Form Submission
- **POST requests** — `requests.post(url, data={'field': 'value'})` for form submission
- **CSRF tokens** — Extract hidden CSRF token from form HTML; include in POST data
- **Form fields** — Inspect form with browser DevTools; identify all required fields including hidden ones
- **File uploads** — Use `files` parameter in `requests.post()` for multipart form data

### Session Management
- **requests.Session()** — Maintains cookies across requests; handles redirects; connection pooling
- **Cookie persistence** — Session object automatically stores and sends cookies
- **Login flow** — GET login page → extract CSRF → POST credentials → use session for authenticated pages

### Authentication
- **HTTP Basic Auth** — `requests.get(url, auth=('user', 'pass'))` for Basic authentication
- **Token-based** — Extract auth token from login response; send in headers for subsequent requests
- **OAuth** — Use `requests-oauthlib` for OAuth-protected APIs
- **Session expiry** — Detect expired sessions (redirects to login); re-authenticate automatically

---

## Chapter 11: Scraping JavaScript

### Selenium WebDriver
- **Setup** — `webdriver.Chrome()` or `webdriver.Firefox()`; requires matching driver binary
- **Headless mode** — `options.add_argument('--headless')` for browser without GUI; essential for servers
- **Navigation** — `driver.get(url)`; `driver.find_element(By.CSS_SELECTOR, selector)`
- **Interaction** — `.click()`, `.send_keys()`, `.clear()` on elements; simulate user behavior

### Waiting for Content
- **Implicit waits** — `driver.implicitly_wait(10)` sets default wait for element finding
- **Explicit waits** — `WebDriverWait(driver, 10).until(EC.presence_of_element_located(...))` for specific conditions
- **Expected conditions** — `element_to_be_clickable`, `visibility_of_element_located`, `text_to_be_present_in_element`
- **Custom waits** — Write lambda conditions for complex wait scenarios

### JavaScript Execution
- **Execute script** — `driver.execute_script('return document.title')` runs JS in page context
- **Scroll page** — `driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')` for infinite scroll
- **Extract data** — Execute JS to extract data from page variables, localStorage, or DOM

### Ajax Handling
- **Wait for Ajax** — Wait for specific elements that load asynchronously
- **Network monitoring** — Intercept XHR requests to find underlying API endpoints
- **Alternative approach** — If you can identify the API endpoint, use `requests` directly instead of Selenium

---

## Chapter 12: Crawling Through APIs

### REST API Basics
- **HTTP methods** — GET (read), POST (create), PUT (update), DELETE (remove)
- **JSON responses** — `response.json()` for parsing; handle nested objects and arrays
- **Headers** — Set `Accept: application/json`, `Authorization: Bearer token`
- **Query parameters** — `requests.get(url, params={'key': 'value'})` for clean URL building

### Undocumented APIs
- **Browser DevTools** — Use Network tab to discover API calls made by JavaScript
- **XHR filtering** — Filter network requests to XHR/Fetch to find data endpoints
- **Request replication** — Copy request headers, cookies, parameters from DevTools to Python
- **API reverse engineering** — Study request patterns to understand pagination, filtering, authentication

### API Best Practices
- **Rate limiting** — Respect rate limit headers; implement backoff on 429 responses
- **Pagination** — Handle cursor-based, offset-based, and link-header pagination
- **Error handling** — Retry on 5xx errors with exponential backoff; don't retry on 4xx
- **Authentication** — Store API keys securely; handle token refresh for OAuth

---

## Chapter 13: Image Processing and OCR

### Pillow (PIL)
- **Image loading** — `Image.open(path)` or from URL response content
- **Manipulation** — Resize, crop, rotate, filter for preprocessing before OCR
- **Thresholding** — Convert to grayscale; apply threshold for clean black/white text

### Tesseract OCR
- **pytesseract** — `pytesseract.image_to_string(image)` for text extraction from images
- **Preprocessing** — Clean images before OCR: denoise, deskew, threshold, resize
- **Language support** — Specify language with `lang='eng'`; install language packs as needed
- **Confidence** — Use `image_to_data()` for per-word confidence scores; filter low confidence

### CAPTCHA Handling
- **Simple CAPTCHAs** — Preprocessing + OCR may solve simple text CAPTCHAs
- **Complex CAPTCHAs** — Consider CAPTCHA-solving services or rethink approach (use API instead)
- **Ethical note** — CAPTCHAs exist to prevent automated access; respect their purpose

---

## Chapter 14: Avoiding Scraping Traps

### Headers and Identity
- **User-Agent** — Set a realistic browser User-Agent string; rotate for large-scale scraping
- **Accept headers** — Include Accept, Accept-Language, Accept-Encoding to mimic real browsers
- **Referer** — Set appropriate Referer header when navigating between pages
- **Cookie handling** — Accept and send cookies; use sessions for automatic management

### Behavioral Patterns
- **Request timing** — Add random delays between requests (1-5 seconds); avoid perfectly regular intervals
- **Navigation patterns** — Don't jump straight to data pages; mimic human browsing (home → category → product)
- **Click patterns** — With Selenium, click through pages naturally rather than jumping directly to URLs

### Honeypot Detection
- **Hidden links** — Check for CSS `display:none` or `visibility:hidden` links; avoid following them
- **Hidden form fields** — Pre-filled hidden fields may be traps; don't submit unexpected values
- **Link patterns** — Suspicious URL patterns or link text may indicate honeypots

### IP and Session Management
- **Proxy rotation** — Rotate IP addresses for large-scale scraping; use proxy services
- **Session rotation** — Create new sessions periodically; don't use same cookies indefinitely
- **Fingerprint diversity** — Vary headers, timing, and behavior to avoid fingerprinting

---

## Chapter 15: Testing Scrapers

### Unit Testing
- **Parse function tests** — Test parsing functions with saved HTML files; verify extracted data
- **Fixture files** — Save representative HTML pages as test fixtures; don't hit live sites in tests
- **Edge cases** — Test with missing elements, empty pages, different layouts, malformed HTML

### Integration Testing
- **End-to-end** — Test full scrape pipeline from fetch to storage with known target pages
- **Selenium tests** — Use Selenium for testing JavaScript-heavy scraping flows
- **Mock responses** — Use `responses` or `requests-mock` libraries for HTTP mocking in tests

### Testing Best Practices
- **Site change detection** — Periodically check if site structure has changed; alert on selector failures
- **Regression testing** — Compare current results against known-good baselines
- **CI integration** — Run scraper tests in CI pipeline; catch issues before deployment

---

## Chapter 16: Parallel Web Scraping

### Threading
- **threading module** — Use for I/O-bound scraping; GIL doesn't block network operations
- **Thread pool** — `concurrent.futures.ThreadPoolExecutor` for managed thread pools
- **Thread safety** — Use locks for shared state (counters, result lists); prefer queues for task distribution

### Multiprocessing
- **multiprocessing module** — Use for CPU-bound processing (parsing, cleaning); bypasses GIL
- **Process pool** — `concurrent.futures.ProcessPoolExecutor` for managed process pools
- **Inter-process communication** — Use Queue for task distribution; Pipe for point-to-point

### Queue-Based Architecture
- **Producer-consumer** — Producer adds URLs to queue; consumers fetch and parse in parallel
- **URL frontier** — Priority queue for managing which URLs to crawl next
- **Result aggregation** — Collect results from workers into shared storage

### Parallel Best Practices
- **Per-domain limits** — Limit concurrent requests per domain even with parallel scraping
- **Graceful shutdown** — Handle KeyboardInterrupt; drain queues cleanly on shutdown
- **Error isolation** — One worker's failure shouldn't crash the entire scraping operation
- **Progress tracking** — Log completed/remaining tasks; monitor worker health

---

## Chapter 17: Remote Scraping

### Tor
- **Tor proxy** — Route requests through Tor network for anonymity; `socks5://127.0.0.1:9150`
- **IP verification** — Check IP with a service like httpbin.org/ip to verify Tor is active
- **Performance** — Tor is slow; use only when anonymity is required
- **Circuit rotation** — Signal Tor to create new circuit for fresh IP; don't rotate too frequently

### Proxy Services
- **Rotating proxies** — Commercial proxy services provide rotating IP pools
- **Proxy types** — HTTP/HTTPS proxies, SOCKS proxies; understand the difference
- **Proxy configuration** — `requests.get(url, proxies={'http': proxy_url})`; or configure in Scrapy settings

### Cloud-Based Scraping
- **Headless instances** — Run scrapers on cloud VMs (AWS, GCP, DigitalOcean) for scale
- **Containerization** — Docker containers for consistent scraper environments
- **Scheduling** — Use cron, cloud schedulers, or orchestration tools for recurring scrapes
- **Cost management** — Right-size instances; use spot/preemptible instances for batch scraping

---

## Chapter 18: Legalities and Ethics

### Legal Framework
- **robots.txt** — Machine-readable file at `/robots.txt`; specifies which paths are allowed/disallowed
- **Terms of Service** — Many sites prohibit scraping in ToS; understand the legal weight
- **CFAA** — Computer Fraud and Abuse Act (US); accessing computers "without authorization" is a federal crime
- **Copyright** — Scraped data may be copyrighted; fair use depends on purpose and amount
- **GDPR** — If scraping personal data of EU citizens, GDPR obligations apply

### Ethical Scraping
- **Respect the site** — Don't overload servers; honor rate limits; scrape during off-peak hours
- **Identify yourself** — Use a descriptive User-Agent; provide contact email for site administrators
- **Minimize footprint** — Only scrape what you need; don't archive entire sites unnecessarily
- **Data handling** — Handle scraped personal data responsibly; minimize collection and storage
- **Give back** — If possible, contribute to the site or community; don't just extract value
