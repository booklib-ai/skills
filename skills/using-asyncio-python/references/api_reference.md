# Using Asyncio in Python — Practices Catalog

Complete chapter-by-chapter catalog of practices from *Using Asyncio in Python*
by Caleb Hattingh.

---

## Chapter 1: Introducing Asyncio

### What Asyncio Is
- **Single-threaded concurrency** — Asyncio uses a single thread with an event loop to handle many I/O operations concurrently
- **I/O-bound focus** — Designed for network programming, database access, file I/O — not CPU-bound computation
- **Cooperative multitasking** — Coroutines voluntarily yield control at await points; no preemptive switching
- **Event loop at the core** — The loop monitors I/O readiness and schedules coroutines to run when their I/O is ready

### When to Use Asyncio
- **Network servers** — Handle thousands of concurrent connections without thousands of threads
- **API clients** — Fetch from multiple endpoints concurrently without threading overhead
- **Database access** — Run multiple queries concurrently with async database drivers
- **Microservices** — Async is natural for services that call other services over HTTP/gRPC
- **NOT for CPU-bound work** — Use multiprocessing or ProcessPoolExecutor for computation

### Key Insight
- Asyncio makes concurrent I/O code look sequential — easier to read and reason about than callbacks or threads
- The main cost is that the entire ecosystem must be async-aware; mixing sync and async requires care

---

## Chapter 2: The Truth About Threads

### Thread Drawbacks
- **Race conditions** — Shared mutable state plus preemptive scheduling creates hard-to-find bugs
- **Resource consumption** — Each thread costs ~8MB of stack memory; thousands of threads are impractical
- **Difficult debugging** — Thread bugs are non-deterministic and may not reproduce
- **GIL limitation** — Python's Global Interpreter Lock means threads don't provide true parallelism for CPU-bound code
- **Complexity** — Locks, semaphores, and condition variables add complexity and potential deadlocks

### When Threads Are Still Useful
- **CPU-bound in executor** — ThreadPoolExecutor or ProcessPoolExecutor for blocking operations called from async code
- **Legacy library integration** — When async alternatives don't exist, wrap blocking calls in run_in_executor()
- **Simple scripts** — For quick scripts with few concurrent operations, threads may be simpler

### ThreadPoolExecutor Pattern
- Use `loop.run_in_executor(executor, blocking_func, *args)` to offload blocking calls
- Set max_workers to bound resource usage: `ThreadPoolExecutor(max_workers=5)`
- For CPU-bound work, prefer ProcessPoolExecutor over ThreadPoolExecutor
- Always shut down the executor on application exit

### The Case for Asyncio Over Threads
- **No race conditions by default** — Single-threaded means no shared state issues between await points
- **Lower resource usage** — Coroutines are lightweight; thousands cost almost nothing
- **Explicit yield points** — You know exactly where context switches happen (at every await)
- **Simpler reasoning** — Code between awaits runs atomically; no locks needed

---

## Chapter 3: Asyncio Walk-Through

### Quickstart: asyncio.run()
- **Entry point** — `asyncio.run(main())` is the recommended way to start async code (Python 3.7+)
- **Creates and destroys loop** — It creates a new event loop, runs the coroutine, then closes the loop
- **Call once at top level** — Don't call asyncio.run() from within async code; use create_task() instead
- **Handles cleanup** — Cancels remaining tasks and shuts down async generators on exit

### The Event Loop
- **Heart of asyncio** — Monitors I/O file descriptors and schedules callbacks/coroutines
- **loop.run_until_complete(coro)** — Runs a single coroutine to completion (low-level; prefer asyncio.run())
- **loop.run_forever()** — Runs the loop until stop() is called; useful for long-running servers
- **loop.stop()** — Stops the loop; typically called from a signal handler or callback
- **loop.close()** — Final cleanup; must be called after the loop is stopped
- **Debug mode** — `asyncio.run(main(), debug=True)` enables slow-callback warnings and extra checks

### Coroutines (async def / await)
- **async def** — Defines a coroutine function; calling it returns a coroutine object (doesn't execute it)
- **await** — Suspends the current coroutine until the awaited coroutine/future completes
- **Coroutine vs function** — A coroutine runs to the first await, then yields control back to the loop
- **Must be awaited** — A coroutine that is called but never awaited will never execute (common bug)
- **Chaining** — Coroutines can await other coroutines for composition

### Tasks
- **asyncio.create_task(coro)** — Wraps a coroutine in a Task and schedules it on the event loop (Python 3.7+)
- **Concurrent execution** — Tasks run concurrently; the event loop switches between them at await points
- **Task is a Future** — Tasks are a subclass of Future; you can await them and get results
- **Name tasks** — `create_task(coro, name="fetch-user")` for better debugging and logging
- **Keep references** — Store task references; orphaned tasks may silently swallow exceptions
- **task.cancel()** — Requests cancellation; raises CancelledError at the next await point in the task
- **task.result()** — Gets the result after the task completes; raises the exception if the task failed

### asyncio.ensure_future() vs create_task()
- **create_task()** — Preferred for coroutines; explicitly creates a Task
- **ensure_future()** — Accepts both coroutines and futures; wraps coroutines in Tasks
- **Recommendation** — Use create_task() for coroutines; ensure_future() only when handling generic awaitables

### Futures
- **Low-level construct** — Represents a result that will be available in the future
- **Rarely used directly** — Tasks and coroutines are higher-level and preferred
- **future.set_result(value)** — Sets the result; wakes up anyone awaiting the future
- **future.set_exception(exc)** — Sets an exception; awaiting the future will raise it
- **Callback based** — `future.add_done_callback(fn)` for callback-style programming

### gather() and wait()
- **asyncio.gather(*coros)** — Run multiple coroutines concurrently and collect all results
  - Returns results in the same order as the input coroutines
  - `return_exceptions=True` — Returns exceptions as results instead of raising; prevents one failure from cancelling all
  - Without return_exceptions, first exception cancels remaining tasks
- **asyncio.wait(tasks, return_when=...)** — More flexible; returns (done, pending) sets
  - `FIRST_COMPLETED` — Returns when any task finishes
  - `FIRST_EXCEPTION` — Returns when any task raises an exception
  - `ALL_COMPLETED` — Returns when all tasks complete (default)
- **asyncio.as_completed(coros)** — Iterator yielding futures as they complete; process results as they arrive

### Timeouts
- **asyncio.wait_for(coro, timeout=seconds)** — Cancels the coroutine if it exceeds the timeout
- **asyncio.timeout(seconds)** — Context manager for timeouts (Python 3.11+): `async with asyncio.timeout(5):`
- **Always set timeouts** — Network operations without timeouts can hang indefinitely

### Async Context Managers (async with)
- **__aenter__ / __aexit__** — Async versions of context manager protocols
- **Resource cleanup** — Ensures connections, sessions, and files are properly closed
- **aiohttp example** — `async with aiohttp.ClientSession() as session:` ensures session cleanup
- **Database pools** — `async with pool.acquire() as conn:` borrows and returns connections
- **@asynccontextmanager** — Decorator from contextlib for creating async context managers with yield

### Async Generators (async for)
- **async def with yield** — Async generator function; produces values asynchronously
- **async for** — Iterates over an async generator or any async iterable
- **Use cases** — Streaming data from network, paginated API results, database cursors
- **Cleanup** — Async generators are finalized when the loop shuts down (athrow GeneratorExit)

### Async Comprehensions
- **List** — `[x async for x in aiter]` — Async list comprehension
- **Set** — `{x async for x in aiter}` — Async set comprehension
- **Dict** — `{k: v async for k, v in aiter}` — Async dict comprehension
- **Filtering** — `[x async for x in aiter if await predicate(x)]`
- **Concise** — Combines async iteration with comprehension syntax

### Starting Up and Shutting Down

#### Startup Pattern
- Use asyncio.run() as the entry point
- Initialize resources (database pools, HTTP sessions) in the main coroutine
- Create long-running tasks with create_task()
- Use async context managers for resource lifecycle

#### Shutdown Pattern (Critical)
1. **Signal handling** — Register signal handlers for SIGTERM and SIGINT:
   ```
   loop.add_signal_handler(signal.SIGTERM, handler)
   loop.add_signal_handler(signal.SIGINT, handler)
   ```
2. **Cancel pending tasks** — Get all tasks and cancel them:
   ```
   tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
   for task in tasks:
       task.cancel()
   await asyncio.gather(*tasks, return_exceptions=True)
   ```
3. **Shutdown async generators** — `await loop.shutdown_asyncgens()`
4. **Shutdown default executor** — `await loop.shutdown_default_executor()` (Python 3.9+)
5. **Close the loop** — `loop.close()`

#### Executor Integration
- **run_in_executor(executor, func, *args)** — Run blocking function in a thread/process pool
- **Default executor** — If executor is None, uses the default ThreadPoolExecutor
- **Custom executor** — Pass a custom ThreadPoolExecutor or ProcessPoolExecutor
- **Shutdown executor** — Call `executor.shutdown(wait=True)` or `loop.shutdown_default_executor()`

---

## Chapter 4: 20 Libraries You Aren't Using (But Oh, You Should)

### aiohttp — Async HTTP Client and Server
- **ClientSession** — Always use session for connection pooling: `async with aiohttp.ClientSession() as session:`
- **GET/POST** — `async with session.get(url) as resp:` — async context manager for response
- **Response methods** — `await resp.json()`, `await resp.text()`, `await resp.read()` for different formats
- **Server** — `aiohttp.web.Application()` for building async web servers
- **WebSockets** — Built-in WebSocket support for both client and server
- **Middleware** — Add middleware for logging, auth, error handling
- **Connection limits** — `TCPConnector(limit=100)` to control connection pool size

### aiofiles — Async File I/O
- **Non-blocking file ops** — `async with aiofiles.open('file.txt', 'r') as f:` — doesn't block the event loop
- **Same API as built-in open** — read(), write(), readline(), etc., all async
- **When to use** — When file I/O would block the event loop; especially in servers handling many requests
- **Under the hood** — Uses ThreadPoolExecutor internally; overhead is small but present

### Sanic — Async Web Framework
- **Flask-like API** — Familiar decorator-based routing: `@app.route('/')`
- **Async handlers** — Route handlers are async def; can use await freely
- **High performance** — Built on uvloop for faster event loop; designed for speed
- **Middleware** — Request and response middleware for cross-cutting concerns
- **WebSockets** — Built-in WebSocket support

### aioredis — Async Redis Client
- **Connection pooling** — `await aioredis.create_redis_pool('redis://localhost')`
- **Commands** — `await redis.get('key')`, `await redis.set('key', 'value')`
- **Pub/Sub** — Async pub/sub for real-time messaging: channel iteration with async for
- **Pipeline** — Batch multiple commands for efficiency

### asyncpg — Async PostgreSQL Client
- **High performance** — Pure Python async PostgreSQL driver; significantly faster than psycopg2
- **Connection pool** — `pool = await asyncpg.create_pool(dsn=...)`
- **Prepared statements** — `stmt = await conn.prepare('SELECT ...')` for repeated queries
- **Transactions** — `async with conn.transaction():` for atomic operations
- **Binary protocol** — Uses PostgreSQL binary protocol for better performance

### Other Notable Libraries
- **uvloop** — Drop-in replacement for asyncio event loop; 2-4x faster; `asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())`
- **aiodns** — Async DNS resolution
- **aiosmtplib** — Async SMTP client for sending emails
- **aiomysql** — Async MySQL client
- **motor** — Async MongoDB driver

---

## Chapter 5: Concluding Thoughts

### Key Takeaways
- Asyncio is the future of Python I/O-bound concurrency
- The ecosystem is maturing; most major libraries have async versions
- Start simple and add complexity as needed
- Graceful shutdown is the hardest part to get right; invest time in it
- Testing async code requires async-aware test frameworks (pytest-asyncio)

---

## Appendix A: A Short History of Async Support in Python

### Evolution Timeline
- **Generators (PEP 255)** — yield keyword enables lazy iteration
- **Generator-based coroutines (PEP 342)** — send(), throw(), close() turn generators into coroutines
- **yield from (PEP 380)** — Delegate to sub-generators; enables coroutine composition
- **asyncio module (PEP 3156)** — stdlib event loop and coroutine infrastructure (Python 3.4)
- **async/await syntax (PEP 492)** — Native coroutine syntax replaces @asyncio.coroutine and yield from (Python 3.5)
- **Async generators (PEP 525)** — async def with yield for async iteration (Python 3.6)
- **Async comprehensions (PEP 530)** — [x async for x in aiter] syntax (Python 3.6)
- **asyncio.run() (Python 3.7)** — Simplified entry point; no more manual loop management
- **TaskGroups (Python 3.11)** — Structured concurrency with automatic cancellation on failure

### Why This History Matters
- Understanding the evolution helps read older codebases that use yield from or @asyncio.coroutine
- Modern code should always use async/await syntax (Python 3.5+)
- asyncio.run() should always be the entry point (Python 3.7+)
- TaskGroups provide the safest concurrency model (Python 3.11+)

---

## Appendix B: Supplementary Material

### Debug Mode
- `asyncio.run(main(), debug=True)` — Enables extra checks
- Warns about coroutines that were never awaited
- Warns about callbacks that take too long (>100ms by default)
- Logs all exceptions in callbacks

### Common Patterns Summary

| Pattern | Implementation |
|---------|---------------|
| Concurrent fan-out | `results = await asyncio.gather(*tasks, return_exceptions=True)` |
| Rate limiting | `sem = asyncio.Semaphore(10); async with sem: await work()` |
| Timeout | `await asyncio.wait_for(coro, timeout=5.0)` |
| Producer-consumer | `queue = asyncio.Queue(); create_task(producer); create_task(consumer)` |
| Blocking integration | `await loop.run_in_executor(executor, blocking_func)` |
| Graceful shutdown | Signal handler → cancel tasks → gather with return_exceptions → close |
| Connection pool | `async with aiohttp.ClientSession() as session:` |
| Retry with backoff | try/except in loop with asyncio.sleep(delay * 2**attempt) |
