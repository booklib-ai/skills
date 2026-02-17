# System Design Interview — Chapter-by-Chapter Reference

Complete catalog of system design concepts, patterns, and techniques from all 16 chapters.

---

## Ch 1: Scale From Zero To Millions of Users

### Single Server Setup
- Web app, database, cache all on one server
- DNS resolves domain to IP; HTTP request/response cycle

### Database
- **Relational (SQL)**: MySQL, PostgreSQL — structured data, joins, ACID
- **NoSQL**: Key-value (Redis, DynamoDB), Document (MongoDB), Column (Cassandra), Graph (Neo4j)
- Choose NoSQL when: super-low latency, unstructured data, massive scale, no relational needs

### Scaling
- **Vertical scaling** (scale up): bigger machine; simple but has hard limits and no failover
- **Horizontal scaling** (scale out): more machines; preferred for large-scale apps

### Load Balancer
- Distributes traffic across web servers
- Users connect to LB's public IP; servers use private IPs
- Enables: failover (reroute if server dies), horizontal scaling (add more servers)

### Database Replication
- **Master-slave model**: Master handles writes; slaves handle reads
- Read/write ratio typically high → multiple read replicas
- Failover: slave promoted to master if master fails; new slave replaces old one
- Benefits: performance (parallel reads), reliability (data replicated), availability (failover)

### Cache
- Temporary storage for frequently accessed data (in-memory, much faster than DB)
- **Read-through cache**: Check cache → if miss, read from DB → store in cache → return
- **Considerations**: Use when reads >> writes; expiration policy; consistency; eviction (LRU, LFU, FIFO); single point of failure (multiple cache servers)

### CDN (Content Delivery Network)
- Geographically distributed servers for static content (images, CSS, JS, videos)
- User requests asset → CDN returns cached copy or fetches from origin → caches with TTL
- **Considerations**: Cost (cache only frequently accessed), TTL, CDN fallback, invalidation (API or versioning)

### Stateless Web Tier
- Move session data out of web servers into shared storage (Redis, Memcached, NoSQL)
- Any web server can handle any request → easy horizontal scaling
- Session data stored in persistent shared data store

### Data Centers
- Multiple data centers for geo-routing (users routed to nearest DC)
- **Challenges**: Traffic redirection (GeoDNS), data synchronization, test/deployment across DCs

### Message Queue
- Durable component for async communication (producers → queue → consumers)
- Decouples components: producer and consumer scale independently
- Use when: tasks are time-consuming, components should be loosely coupled

### Logging, Metrics, Automation
- **Logging**: Per-server or aggregated (centralized tools)
- **Metrics**: Host-level (CPU, memory), aggregated (DB tier performance), business (DAU, retention)
- **Automation**: CI/CD, build automation, testing automation

### Database Sharding
- Split data across multiple databases by shard key
- **Shard key selection**: Choose key that distributes data evenly
- **Challenges**: Resharding (consistent hashing), celebrity/hotspot problem, join/denormalization
- **Techniques**: Consistent hashing for distribution; denormalize to avoid cross-shard joins

---

## Ch 2: Back-of-the-Envelope Estimation

### Powers of 2
- 10 = 1 Thousand (1 KB), 20 = 1 Million (1 MB), 30 = 1 Billion (1 GB)
- 40 = 1 Trillion (1 TB), 50 = 1 Quadrillion (1 PB)

### Latency Numbers Every Programmer Should Know
- L1 cache: 0.5 ns
- Branch mispredict: 5 ns
- L2 cache: 7 ns
- Mutex lock/unlock: 100 ns
- Main memory: 100 ns
- Compress 1KB with Zippy: 10,000 ns (10 μs)
- Send 2KB over 1 Gbps network: 20,000 ns (20 μs)
- SSD random read: 150,000 ns (150 μs)
- Read 1MB sequentially from memory: 250,000 ns (250 μs)
- Round trip within same datacenter: 500,000 ns (500 μs)
- Read 1MB sequentially from SSD: 1,000,000 ns (1 ms)
- Disk seek: 10,000,000 ns (10 ms)
- Read 1MB sequentially from disk: 30,000,000 ns (30 ms)
- Packet CA→Netherlands→CA: 150,000,000 ns (150 ms)

### Key Takeaways
- Memory is fast, disk is slow
- Avoid disk seeks if possible
- Simple compression algorithms are fast
- Compress data before sending over network
- Data centers are far; inter-DC round trips are expensive

### Availability Numbers
- 99% = 3.65 days/year downtime
- 99.9% = 8.77 hours/year
- 99.99% = 52.60 minutes/year
- 99.999% = 5.26 minutes/year

### Estimation Tips
- Round and approximate; precision not needed
- Write down assumptions
- Label units clearly
- Common estimates: QPS, peak QPS (2–5× average), storage, bandwidth, cache memory

---

## Ch 3: A Framework For System Design Interviews

### The 4-Step Process

**Step 1 — Understand the problem and establish design scope (3–10 min)**
- Ask clarifying questions: What features? How many users? Scale trajectory?
- Define functional requirements (what the system does)
- Define non-functional requirements (scale, latency, availability, consistency)
- Make back-of-envelope estimates

**Step 2 — Propose high-level design and get buy-in (10–15 min)**
- Draw component diagram: clients, servers, databases, caches, CDN, load balancers
- Define API endpoints (REST or similar)
- Sketch data flow through the system
- Get agreement before diving deeper

**Step 3 — Design deep dive (10–25 min)**
- Focus on 2–3 most critical/interesting components
- Discuss trade-offs for each design decision
- Address non-functional requirements (scalability, consistency, availability)

**Step 4 — Wrap up (3–5 min)**
- Summarize the design
- Discuss error handling and edge cases
- Operational considerations: metrics, monitoring, alerts
- Future scaling and improvements

### Dos and Don'ts
- DO: ask for clarification, communicate approach, suggest multiple approaches, design with interviewer
- DON'T: jump into solution, think in silence, ignore non-functional requirements

---

## Ch 4: Design A Rate Limiter

### Algorithms

**Token bucket**
- Bucket with fixed capacity; tokens added at fixed rate; request consumes a token
- Pros: easy to implement, memory efficient, allows burst traffic
- Cons: tuning bucket size and refill rate can be challenging

**Leaking bucket**
- Queue with fixed size; requests processed at fixed rate; overflow rejected
- Pros: memory efficient, stable outflow rate
- Cons: burst of traffic fills queue; old requests may starve new ones

**Fixed window counter**
- Divide timeline into fixed windows; counter per window; reject when counter > threshold
- Pros: memory efficient, simple
- Cons: spike at window edges can allow 2× rate

**Sliding window log**
- Keep timestamp log of each request; count requests in sliding window
- Pros: very accurate
- Cons: consumes lots of memory (stores all timestamps)

**Sliding window counter**
- Hybrid: fixed window counters + sliding window calculation
- Formula: requests in current window + requests in previous window × overlap percentage
- Pros: smooths traffic spikes, memory efficient
- Cons: approximation (assumes even distribution in previous window)

### Architecture
- Rate limiting rules stored in configuration (usually on disk, cached in memory)
- Redis used for counters: INCR (increment) and EXPIRE (set TTL)
- Rate limiter middleware sits between client and API servers
- HTTP 429 (Too Many Requests) returned when rate exceeded
- Headers: X-Ratelimit-Remaining, X-Ratelimit-Limit, X-Ratelimit-Retry-After

### Distributed Challenges
- **Race condition**: Use Redis Lua script or sorted set for atomic operations
- **Synchronization**: Centralized Redis store; or sticky sessions (not recommended)

---

## Ch 5: Design Consistent Hashing

### Problem
- Simple hash (key % N servers) causes massive redistribution when servers added/removed

### Hash Ring
- Map servers and keys onto a circular hash space (0 to 2^160 - 1 for SHA-1)
- Key assigned to first server encountered going clockwise on the ring
- Adding/removing server only affects keys in adjacent segment

### Virtual Nodes
- Each real server maps to multiple virtual nodes on the ring
- Benefits: more even distribution, handles heterogeneous servers (more vnodes for powerful servers)
- Trade-off: more vnodes = better balance but more metadata to store

### Benefits
- Minimized key redistribution when servers change
- Horizontal scaling is straightforward
- Mitigates hotspot problem with virtual nodes

---

## Ch 6: Design A Key-Value Store

### CAP Theorem
- **Consistency**: All nodes see same data at same time
- **Availability**: Every request gets a response
- **Partition tolerance**: System works despite network partitions
- Must choose 2 of 3: CP (consistency + partition tolerance), AP (availability + partition tolerance)
- In real distributed systems, partition tolerance is mandatory → choose between C and A

### Core Techniques

**Data Partitioning**
- Consistent hashing (Ch 5) to distribute data across nodes

**Data Replication**
- Replicate to N nodes (first N unique servers clockwise on hash ring)
- N = 3 is typical

**Quorum Consensus**
- N = number of replicas, W = write quorum, R = read quorum
- W + R > N guarantees strong consistency (overlap ensures latest value read)
- W = 1, R = N → fast write, slow read
- W = N, R = 1 → slow write, fast read
- Typical: N=3, W=2, R=2

**Consistency Models**
- Strong: client always sees most recent write
- Weak: subsequent reads may not see most recent write
- Eventual: given enough time, all replicas converge

**Vector Clocks**
- [server, version] pairs to detect conflicts and causality
- Downside: complexity grows with many servers; prune based on threshold

**Handling Failures**
- **Failure detection**: Gossip protocol — each node periodically sends heartbeat list to random nodes; if no heartbeat for threshold period, node marked down
- **Sloppy quorum**: When not enough healthy nodes, use temporary nodes (hinted handoff)
- **Anti-entropy**: Merkle trees for efficient inconsistency detection and repair
- **Merkle tree**: Hash tree where leaves are hashes of data blocks; only differing branches need sync

### Write Path
- Write request → commit log → memory cache (memtable) → when memtable full, flush to SSTable on disk

### Read Path
- Check memtable → if not found, check Bloom filter → read from SSTables

---

## Ch 7: Design A Unique ID Generator In Distributed Systems

### Approaches

**Multi-master replication**
- Auto-increment by k (number of servers): server 1 generates 1,3,5...; server 2 generates 2,4,6...
- Cons: hard to scale, IDs don't go up across servers, adding/removing servers breaks scheme

**UUID**
- 128-bit number, extremely low collision probability
- Pros: simple, no coordination, scales independently per server
- Cons: 128 bits is long, not sortable by time, non-numeric

**Ticket server**
- Centralized auto-increment DB (Flickr approach)
- Pros: numeric, easy to implement, works for small/medium scale
- Cons: single point of failure (can use multiple but adds sync complexity)

**Twitter snowflake**
- 64-bit ID: 1 bit sign + 41 bits timestamp + 5 bits datacenter + 5 bits machine + 12 bits sequence
- Timestamp: milliseconds since custom epoch; sortable by time
- Sequence: reset to 0 every millisecond; 4096 IDs per machine per millisecond
- Pros: 64-bit, time-sorted, distributed, high throughput
- This is the recommended approach for most use cases

---

## Ch 8: Design A URL Shortener

### API Design
- POST api/v1/data/shorten (longUrl) → shortUrl
- GET api/v1/shortUrl → 301/302 redirect to longUrl

### Redirect
- **301 (Permanent)**: Browser caches; reduces server load; less analytics
- **302 (Temporary)**: Every request hits server; better for analytics/tracking

### Hash Approaches

**Hash + collision resolution**
- Apply hash (CRC32, MD5, SHA-1) → take first 7 characters → check DB for collision → append predefined string if collision → recheck
- Bloom filter can speed up collision detection

**Base-62 conversion**
- Map auto-increment ID to base-62 (0-9, a-z, A-Z)
- 7 characters = 62^7 ≈ 3.5 trillion URLs
- Pros: no collision, short URL length predictable from ID
- Cons: next URL is predictable; depends on unique ID generator

### URL Shortening Flow
- Input longURL → check if exists in DB → if yes, return existing shortURL → if no, generate new ID → convert to base-62 → store in DB → return shortURL

---

## Ch 9: Design A Web Crawler

### Components
- **Seed URLs**: Starting point; choose by topic locality or domain diversity
- **URL Frontier**: Queue managing which URLs to crawl next; handles politeness and priority
- **HTML Downloader**: Fetches page content; checks robots.txt (cached)
- **Content Parser**: Validates and parses HTML
- **Content Seen?**: Dedup with hash comparison (content fingerprint)
- **URL Seen?**: Bloom filter or hash table to avoid recrawling
- **URL Storage**: Already-visited URLs stored
- **Link Extractor**: Extracts URLs from HTML; converts relative to absolute

### URL Frontier Design
- **Politeness**: Separate queue per host; only one worker per host; download delay between requests
- **Priority**: URL prioritizer ranks URLs by PageRank, update frequency, freshness; feeds into priority queues
- **Freshness**: Recrawl based on update history and page importance
- **Storage**: Mostly on disk with in-memory buffer for enqueue/dequeue

### Robustness
- Consistent hashing to distribute load across crawlers
- Save crawl state for recovery
- Exception handling for malformed HTML
- Anti-spam: blacklists, content validation

### Problematic Content
- Redundant content: dedup via content hashing
- Spider traps: set max URL depth
- Data noise: exclude ads, spam, etc.

---

## Ch 10: Design A Notification System

### Notification Types
- **iOS Push**: Provider → APNs (Apple Push Notification Service) → iOS device
- **Android Push**: Provider → FCM (Firebase Cloud Messaging) → Android device
- **SMS**: Provider → SMS service (Twilio, Nexmo) → phone
- **Email**: Provider → email service (Mailchimp, SendGrid) → email

### Contact Info Gathering
- Collect device tokens, phone numbers, email addresses during signup/app install
- Store in contact_info table linked to user_id

### High-Level Design
- Services (1 to N) → Notification system → Third-party services → Devices
- Components: notification servers, cache, DB, message queues (one per notification type), workers

### Reliability
- **Notification log**: Persist notifications in DB for retry on failure
- **Deduplication**: Check event_id before sending to avoid duplicates
- **Retry mechanism**: Workers retry failed notifications with exponential backoff

### Additional Features
- **Notification template**: Reusable templates with parameters for consistency
- **Rate limiting**: Cap notifications per user to prevent overload
- **Monitoring**: Track queued notifications count; set alerts for anomalies
- **Analytics service**: Track open rate, click rate, engagement per notification type
- **User settings**: Opt-in/opt-out per notification channel; settings stored in DB

---

## Ch 11: Design A News Feed System

### Two Sub-Problems
1. **Feed publishing**: User posts content → system stores and distributes to friends' feeds
2. **Newsfeed building**: Aggregate friends' posts in reverse chronological order

### Feed Publishing
- Web servers: authentication, rate limiting
- Fanout service: distribute post to friends' news feeds
- Notification service: inform friends of new content

### Fanout Models

**Fanout on write (push model)**
- Post → immediately write to all friends' caches
- Pros: real-time, fast read (pre-computed)
- Cons: slow for users with many friends (celebrity problem); wasted resources for inactive users

**Fanout on read (pull model)**
- News feed built on-the-fly when user requests it
- Pros: no wasted writes for inactive users; no celebrity problem
- Cons: slow reads (fetch and merge at read time)

**Hybrid approach (recommended)**
- Push for normal users (fast); pull for celebrities (avoid fan-out explosion)
- Reduces write amplification while keeping reads fast for most users

### Cache Architecture (5 tiers)
- **News Feed**: pre-computed feed per user (feed IDs)
- **Content**: post data, indexed by post ID
- **Social Graph**: follower/following relationships
- **Action**: liked, replied, shared status per post per user
- **Counters**: likes count, replies count, followers count

---

## Ch 12: Design A Chat System

### Communication Protocols
- **Polling**: Client periodically asks server for new messages; wasteful if no new messages
- **Long polling**: Client holds connection open until server has new message or timeout; server may not know which server holds the connection
- **WebSocket**: Full-duplex persistent connection; client and server send messages anytime; ideal for chat

### High-Level Design
- **Stateless services**: Login, signup, user profile (behind load balancer)
- **Stateful service**: Chat servers maintain persistent WebSocket connections
- **Third-party integration**: Push notifications for offline users
- **Service discovery**: Apache Zookeeper recommends best chat server based on criteria (geo, capacity)

### Storage
- Generic data (user profiles, settings): relational DB with replication/sharding
- Chat history: key-value store (HBase recommended) — write-heavy, sequential access, no random access needed
- **Message table (1-on-1)**: message_id (bigint), message_from (bigint), message_to (bigint), content (text), created_at (timestamp)
- **Message table (group)**: channel_id + message_id as composite key; channel_id is partition key

### Message ID
- Must be unique, sortable by time, within same group/channel
- Approach: local auto-increment per channel (using key-value store's increment); or snowflake-like

### Message Flows
- **1-on-1 send**: User A → Chat server 1 → Message sync queue → Chat server 2 → User B
- **Message sync**: Each device has cur_max_message_id; fetch messages where id > cur_max_message_id
- **Small group**: Message copied to each member's message sync queue
- **Large group**: On-demand pull (fanout on read)

### Online Presence
- **Login**: Set status to online in presence servers (via WebSocket)
- **Logout**: Set status to offline
- **Disconnection**: Heartbeat mechanism; if no heartbeat for X seconds → offline
- **Status fanout**: Presence change → publish to channel → friends subscribed to channel receive update
- For large groups, fetch presence only when user opens group or manually refreshes

---

## Ch 13: Design A Search Autocomplete System

### Trie Data Structure
- Tree structure where each node stores a character; path from root = prefix
- Nodes store: character, children map, frequency/popularity counter, top-k cached queries
- **Search**: traverse trie by prefix → collect all descendants → sort by frequency → return top k
- **Optimization**: Cache top k results at each node to avoid traversal

### Data Gathering Service
- **Analytics logs**: Record every search query with timestamp
- **Aggregators**: Aggregate query frequency (weekly or real-time depending on use case)
- **Workers**: Build/update trie from aggregated data
- **Trie cache**: In-memory trie for fast lookups; weekly snapshot
- **Trie DB**: Persistent storage — document store (serialize trie) or key-value (each prefix = key)

### Query Service
- User types → request sent to query service → trie cache lookup → return top suggestions
- **Optimizations**: AJAX requests (no full page reload), browser caching (autocomplete suggestions cached with TTL ~1 hour), data sampling (log only 1 in N queries to reduce volume)

### Trie Operations
- **Create**: Build from aggregated data (offline, weekly)
- **Update**: Option 1: Rebuild weekly (recommended); Option 2: Update individual nodes in place
- **Delete**: Filter layer removes hateful, violent, explicit, or dangerous suggestions before returning results (don't modify trie directly)

### Scaling
- **Sharding**: By first character (uneven — 's' much larger than 'z'); smarter: shard by frequency-based analysis for even distribution
- **Multi-language**: Unicode support in trie nodes; separate tries per language or unified with locale metadata

---

## Ch 14: Design YouTube

### Requirements
- Upload videos, smooth streaming, quality change, low infrastructure cost, mobile + web
- Estimated: 5M DAU, 10% upload daily, average video 300MB → 150TB new storage/day

### Video Uploading Flow
1. User uploads via parallel chunking to original storage (S3-like)
2. Transcoding servers process video (multiple resolutions, codecs)
3. Transcoded videos stored in transcoded storage
4. CDN caches and serves popular videos
5. Completion queue + handler updates metadata DB and cache
6. Metadata API servers handle title, description, comments, etc.

### Streaming Protocols
- **MPEG-DASH** (Dynamic Adaptive Streaming over HTTP)
- **Apple HLS** (HTTP Live Streaming)
- **Microsoft Smooth Streaming**
- **Adobe HTTP Dynamic Streaming**
- All use adaptive bitrate: client monitors bandwidth → requests appropriate quality segment

### Video Transcoding
- **Why**: Compatibility (different devices/codecs), bandwidth adaptation (mobile vs. desktop), multiple resolutions
- **Bitrate types**: Constant bitrate (CBR), Variable bitrate (VBR)
- **DAG model**: Video split into video/audio streams → parallel processing → encoded → merged

### Transcoding Architecture
- **Preprocessor**: Video splitting, DAG generation, cache check
- **DAG scheduler**: Splits DAG into stages, puts tasks in task queue
- **Resource manager**: Manages task queue, worker queue, running queue; optimal task-worker assignment
- **Task workers**: Execute encoding tasks (defined in DAG)
- **Temporary storage**: Metadata in memory, video/audio in blob storage; freed after encoding
- **Encoded video**: Final output sent to CDN

### System Optimizations
- **Speed**: Parallel uploading (split video into chunks), upload centers close to users, parallelism in transcoding pipeline, pre-signed upload URLs
- **Safety**: Pre-signed URLs (only authorized users upload), DRM, AES encryption, visual watermarking
- **Cost**: Serve popular from CDN; less popular from high-capacity storage servers; short/unpopular videos encoded on-demand; some regions don't need CDN (serve from origin); partner with ISPs

### Error Handling
- **Recoverable errors**: Retry with exponential backoff (e.g., transcode segment failure)
- **Non-recoverable errors**: Stop task, return error code, log for investigation (e.g., malformed video)

---

## Ch 15: Design Google Drive

### Features
- File upload/download, file sync across devices, notifications, reliability, fast sync, low bandwidth, high scalability/availability

### APIs
- **Upload**: Simple upload (small files), Resumable upload (large files — init → get resumable URI → upload chunks → resume on failure)
- **Download**: GET by file path
- **Get revisions**: GET revision history by file path and limit

### High-Level Design
- **Block servers**: Split files into blocks, delta sync (only changed blocks), compression (gzip)
- **Cloud storage**: S3 or equivalent for file blocks
- **Cold storage**: For inactive/archived files (Amazon Glacier)
- **Load balancer**: Distribute requests across API servers
- **API servers**: User/auth management, file metadata CRUD
- **Metadata DB**: File metadata, user info, block info, versioning
- **Metadata cache**: Cache frequently accessed metadata
- **Notification service**: Long polling — client holds connection, notified of changes; eventbus for internal change distribution
- **Offline backup queue**: Queue sync changes for when clients come back online

### Block Server Design
- File split into blocks (e.g., Dropbox max 4MB blocks)
- **Delta sync**: Only sync changed blocks (not entire file)
- **Deduplication**: Hash each block; skip upload if hash already exists
- **Compression**: gzip or bzip2 to reduce transfer size

### Metadata Database Schema
- **User**: name, email, profile_photo
- **Device**: device_id, user_id, last_logged_in
- **Namespace** (workspace/root folder): id, account_id, email
- **File**: id, filename, path, namespace_id, latest_version, is_directory
- **File_version**: id, file_id, device_id, version_number, last_modified
- **Block**: id, file_version_id, block_order, block_hash, s3_object_key

### Sync Flows
- **Upload**: Client → Block servers (delta sync) → Cloud storage; Client → API servers → Metadata DB; Notification service informs other clients
- **Download**: Client notified of change (long polling) → Request metadata → Download changed blocks from cloud storage
- **Conflict resolution**: First version wins; later version saved as conflict copy for manual merge

### Failure Handling
- **Load balancer**: Heartbeat monitoring; redirect traffic if one fails
- **Block server**: Other servers pick up unfinished jobs
- **Cloud storage**: S3 multi-region replication
- **API server**: Stateless; LB redirects to healthy instances
- **Metadata cache**: Replica servers; new server replaces failed one
- **Metadata DB**: Master-slave; promote slave if master fails
- **Notification service**: Long polling → client reconnects to different server
- **Offline backup queue**: Multiple replicas for durability

---

## Ch 16: The Learning Continues

### Key Takeaways
- Real-world systems are far more complex than interview designs
- Learn from real-world systems by studying company engineering blogs
- Focus on fundamentals: scaling, caching, replication, partitioning, consistency models
- Practice estimation and trade-off analysis regularly
- Study company engineering blogs: Facebook, Google, Netflix, Uber, Twitter, Airbnb, etc.
