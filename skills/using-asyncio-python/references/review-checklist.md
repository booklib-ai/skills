# Using Asyncio in Python — Async Code Review Checklist

Systematic checklist for reviewing async Python code against the chapters
from *Using Asyncio in Python* by Caleb Hattingh.

---

## 1. Concurrency Model (Chapters 1–2)

### Workload Fit
- [ ] **Ch 1 — Asyncio appropriateness** — Is asyncio used for I/O-bound work? Is CPU-bound work offloaded to executors?
- [ ] **Ch 1 — Single-threaded awareness** — Does the code respect that asyncio runs on a single thread?
- [ ] **Ch 2 — Thread avoidance** — Are threads avoided where asyncio coroutines would suffice?
- [ ] **Ch 2 — Executor usage** — Is run_in_executor() used for blocking calls instead of calling them directly?

### Thread Integration
- [ ] **Ch 2 — ThreadPoolExecutor bounds** — Is max_workers set to prevent unbounded thread creation?
- [ ] **Ch 2 — ProcessPoolExecutor for CPU** — Is ProcessPoolExecutor used instead of ThreadPoolExecutor for CPU-bound work?
- [ ] **Ch 2 — Executor shutdown** — Is the executor properly shut down on application exit?
- [ ] **Ch 2 — No shared mutable state** — Is shared state between threads protected or avoided?

---

## 2. Coroutines & Tasks (Chapter 3)

### Coroutine Basics
- [ ] **Ch 3 — async def/await** — Are coroutines properly defined with async def and awaited?
- [ ] **Ch 3 — No unawaited coroutines** — Are all coroutine calls awaited or wrapped in create_task()?
- [ ] **Ch 3 — asyncio.run() entry** — Is asyncio.run() used as the entry point instead of manual loop management?
- [ ] **Ch 3 — No nested asyncio.run()** — Is asyncio.run() never called from within async code?

### Task Management
- [ ] **Ch 3 — create_task() usage** — Is create_task() used instead of ensure_future() for coroutines?
- [ ] **Ch 3 — Task references kept** — Are created tasks stored in variables or collections to prevent GC and silent exceptions?
- [ ] **Ch 3 — Named tasks** — Are tasks named for debugging: `create_task(coro, name="descriptive-name")`?
- [ ] **Ch 3 — Concurrent when possible** — Are independent I/O operations run concurrently via gather() or create_task(), not sequentially?

### gather() and wait()
- [ ] **Ch 3 — return_exceptions=True** — Is gather() called with return_exceptions=True to prevent one failure from cancelling all?
- [ ] **Ch 3 — Result checking** — Are gather() results checked for exceptions when return_exceptions=True?
- [ ] **Ch 3 — wait() for flexibility** — Is asyncio.wait() used when FIRST_COMPLETED or FIRST_EXCEPTION semantics are needed?
- [ ] **Ch 3 — as_completed() for streaming** — Is as_completed() used when results should be processed as they arrive?

### Cancellation & Timeouts
- [ ] **Ch 3 — CancelledError handling** — Is CancelledError caught in coroutines for cleanup, then re-raised or allowed to propagate?
- [ ] **Ch 3 — Timeouts set** — Are asyncio.wait_for() or asyncio.timeout() used for operations that could hang?
- [ ] **Ch 3 — Cancellation propagation** — Does task.cancel() properly propagate through the task tree?
- [ ] **Ch 3 — No bare except catching CancelledError** — Does `except Exception` not accidentally catch CancelledError (Python <3.9)?

---

## 3. Async Patterns (Chapter 3)

### Async Context Managers
- [ ] **Ch 3 — async with for resources** — Are connections, sessions, files, and pools managed with async with?
- [ ] **Ch 3 — __aenter__/__aexit__** — Do custom async context managers implement proper cleanup in __aexit__?
- [ ] **Ch 3 — @asynccontextmanager** — Is the contextlib decorator used for simple async context managers?

### Async Iteration
- [ ] **Ch 3 — async for usage** — Is async for used for iterating over async generators and streams?
- [ ] **Ch 3 — Async generator cleanup** — Are async generators properly finalized on shutdown?
- [ ] **Ch 3 — Async comprehensions** — Are async comprehensions used for concise async collection building?

---

## 4. Startup & Shutdown (Chapter 3)

### Startup
- [ ] **Ch 3 — Resource initialization** — Are database pools, HTTP sessions, and connections created in the main coroutine?
- [ ] **Ch 3 — Task creation** — Are long-running tasks created with create_task() after resource initialization?
- [ ] **Ch 3 — Context manager lifecycle** — Are resources wrapped in async with to ensure cleanup?

### Shutdown (Critical)
- [ ] **Ch 3 — Signal handling** — Are SIGTERM and SIGINT handlers registered with loop.add_signal_handler()?
- [ ] **Ch 3 — Task cancellation** — Are all pending tasks cancelled on shutdown?
- [ ] **Ch 3 — Cancellation awaited** — Is gather(*tasks, return_exceptions=True) used to wait for cancelled tasks?
- [ ] **Ch 3 — Async generator shutdown** — Is loop.shutdown_asyncgens() called?
- [ ] **Ch 3 — Executor shutdown** — Is loop.shutdown_default_executor() called (Python 3.9+)?
- [ ] **Ch 3 — Loop closed** — Is loop.close() called as the final step?
- [ ] **Ch 3 — No resource leaks** — Are all connections, sessions, and file handles closed on shutdown?

---

## 5. Blocking Prevention (Chapters 2–3)

### Event Loop Protection
- [ ] **Ch 2 — No time.sleep()** — Is asyncio.sleep() used instead of time.sleep()?
- [ ] **Ch 2 — No blocking HTTP** — Is aiohttp used instead of requests/urllib?
- [ ] **Ch 2 — No blocking file I/O** — Is aiofiles or run_in_executor() used instead of open()/read()/write()?
- [ ] **Ch 2 — No blocking database** — Are async database drivers (asyncpg, aiomysql) used instead of sync ones?
- [ ] **Ch 3 — Executor for legacy** — Is run_in_executor() used for any unavoidable blocking calls?
- [ ] **Ch 3 — Debug mode testing** — Has the code been tested with asyncio debug mode to detect slow callbacks?

---

## 6. Library Usage (Chapter 4)

### aiohttp
- [ ] **Ch 4 — ClientSession reuse** — Is a single ClientSession reused across requests, not created per-request?
- [ ] **Ch 4 — Session as context manager** — Is ClientSession used with async with for proper cleanup?
- [ ] **Ch 4 — Connection limits** — Is TCPConnector configured with appropriate connection limits?
- [ ] **Ch 4 — Response consumed** — Are response bodies read (json/text/read) before the response context exits?

### aiofiles
- [ ] **Ch 4 — Async file ops** — Is aiofiles used for file I/O in async contexts?
- [ ] **Ch 4 — Context manager** — Are file handles managed with async with?

### Database Clients
- [ ] **Ch 4 — Connection pooling** — Are database connections pooled (asyncpg.create_pool, etc.)?
- [ ] **Ch 4 — Pool cleanup** — Is the connection pool closed on shutdown?
- [ ] **Ch 4 — Transaction management** — Are transactions used with async with for atomicity?
- [ ] **Ch 4 — Prepared statements** — Are prepared statements used for repeated queries?

---

## 7. Error Handling & Resilience

### Exception Management
- [ ] **Ch 3 — Per-task error handling** — Does each task have its own try/except for error isolation?
- [ ] **Ch 3 — Exception logging** — Are task exceptions logged, not silently swallowed?
- [ ] **Ch 3 — Retry logic** — Are transient errors (network, timeout) retried with exponential backoff?
- [ ] **Ch 3 — Graceful degradation** — Does one task's failure not crash the entire application?

### Concurrency Limits
- [ ] **Ch 3 — Semaphore usage** — Is asyncio.Semaphore used to limit concurrent operations?
- [ ] **Ch 3 — Queue backpressure** — Is asyncio.Queue with maxsize used for producer-consumer backpressure?
- [ ] **Ch 4 — Connection pool limits** — Are HTTP/database connection pools properly sized?

---

## Quick Review Workflow

1. **Concurrency pass** — Verify asyncio is the right choice; check thread/executor integration
2. **Coroutine pass** — Check async def/await correctness, task creation, gather/wait patterns
3. **Resource pass** — Verify async context managers, session management, connection pooling
4. **Shutdown pass** — Check signal handling, task cancellation, cleanup, executor shutdown
5. **Blocking pass** — Scan for any blocking calls on the event loop; verify executor usage
6. **Library pass** — Check correct usage of aiohttp, aiofiles, asyncpg, etc.
7. **Error pass** — Verify cancellation handling, timeouts, retry logic, error isolation
8. **Prioritize findings** — Rank by severity: blocking event loop > resource leaks > missing cancellation > missing timeouts > best practices

## Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Blocks event loop or causes resource leaks | Calling requests.get() or time.sleep() directly, never closing sessions, no shutdown handling |
| **High** | Reliability or correctness issues | Missing CancelledError handling, no timeouts, unawaited coroutines, fire-and-forget tasks |
| **Medium** | Performance or maintainability gaps | Sequential awaits when concurrent possible, no connection pooling, no semaphore limiting, no logging |
| **Low** | Best practice improvements | Missing task names, no debug mode testing, ensure_future instead of create_task, no async comprehensions |
