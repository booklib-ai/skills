# Chapter 7: Concurrency and Parallelism (Items 52-64)

## Item 52: Use subprocess to Manage Child Processes
```python
import subprocess

# Run a command and capture output
result = subprocess.run(
    ['echo', 'Hello from subprocess'],
    capture_output=True,
    text=True
)
print(result.stdout)

# Set timeout
result = subprocess.run(
    ['sleep', '10'],
    timeout=5  # raises TimeoutExpired after 5 seconds
)

# Pipe data to child process
result = subprocess.run(
    ['openssl', 'enc', '-aes-256-cbc', '-pass', 'pass:key'],
    input=b'data to encrypt',
    capture_output=True
)

# Run parallel child processes
procs = [subprocess.Popen(['cmd', arg]) for arg in args]
for proc in procs:
    proc.communicate()  # wait for each
```

- Use `subprocess.run` for simple command execution
- Use `subprocess.Popen` for parallel or streaming processes
- Always set timeouts to prevent hanging

## Item 53: Use Threads for Blocking I/O, Avoid for Parallelism
```python
import threading

# Threads for I/O parallelism — GOOD
def download(url):
    resp = urllib.request.urlopen(url)
    return resp.read()

threads = [threading.Thread(target=download, args=(url,)) for url in urls]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

- The GIL prevents true CPU parallelism with threads
- Threads ARE useful for blocking I/O (network, file system, etc.)
- For CPU-bound work, use `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`
- Never use threads for CPU-intensive computation

## Item 54: Use Lock to Prevent Data Races in Threads
```python
from threading import Lock

class Counter:
    def __init__(self):
        self.count = 0
        self.lock = Lock()

    def increment(self):
        with self.lock:  # context manager is cleanest
            self.count += 1
```

- The GIL does NOT prevent data races on Python objects
- Operations like `+=` are not atomic — they involve read + modify + write
- Always use `Lock` when multiple threads modify shared state
- Use `with lock:` context manager for clean acquire/release

## Item 55: Use Queue to Coordinate Work Between Threads
```python
from queue import Queue
from threading import Thread

def producer(queue):
    for item in generate_items():
        queue.put(item)
    queue.put(None)  # sentinel to signal done

def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        process(item)
        queue.task_done()

queue = Queue(maxsize=10)  # bounded for backpressure
Thread(target=producer, args=(queue,)).start()
Thread(target=consumer, args=(queue,)).start()
queue.join()  # wait for all items to be processed
```

- `Queue` provides thread-safe FIFO communication
- Use `maxsize` for backpressure (producer blocks when full)
- Use `task_done()` + `join()` for completion tracking
- Use sentinel values (None) to signal shutdown

## Item 56: Know How to Recognize When Concurrency Is Necessary
- Concurrency is needed when you have fan-out (one task spawning many) and fan-in (collecting results)
- Signs you need concurrency: I/O-bound waits, independent tasks, pipeline processing
- Start simple (sequential), then add concurrency only when needed

## Item 57: Avoid Creating New Thread Instances for On-demand Fan-out
- Creating a thread per task doesn't scale (thread creation overhead, memory)
- Use thread pools instead (Item 58/59)

## Item 58: Understand How Using Queue for Concurrency Requires Refactoring
- Queue-based pipelines require significant refactoring
- Consider `concurrent.futures` for simpler patterns

## Item 59: Consider ThreadPoolExecutor When Threads Are Necessary for Concurrency
```python
from concurrent.futures import ThreadPoolExecutor

def fetch_url(url):
    return urllib.request.urlopen(url).read()

with ThreadPoolExecutor(max_workers=5) as executor:
    # Submit individual tasks
    future = executor.submit(fetch_url, 'https://example.com')
    result = future.result()

    # Map over multiple inputs
    results = list(executor.map(fetch_url, urls))
```

- Simpler than manual thread + Queue management
- Automatically manages thread lifecycle
- `max_workers` controls parallelism
- Use `ProcessPoolExecutor` for CPU-bound tasks

## Item 60: Achieve Highly Concurrent I/O with Coroutines
```python
import asyncio

async def fetch_data(url):
    # async I/O operation
    reader, writer = await asyncio.open_connection(host, port)
    writer.write(request)
    data = await reader.read()
    return data

async def main():
    # Run multiple coroutines concurrently
    results = await asyncio.gather(
        fetch_data('url1'),
        fetch_data('url2'),
        fetch_data('url3'),
    )

asyncio.run(main())
```

- Coroutines enable thousands of concurrent I/O operations
- Use `async def` and `await` keywords
- `asyncio.gather` runs multiple coroutines concurrently
- Far more efficient than threads for I/O-heavy workloads

## Item 61: Know How to Port Threaded I/O to asyncio
- Replace `threading.Thread` with `async def` coroutines
- Replace blocking I/O calls with `await async_version`
- Replace `Lock` with `asyncio.Lock`
- Replace `Queue` with `asyncio.Queue`
- Use `asyncio.run()` as the entry point

## Item 62: Mix Threads and Coroutines to Ease the Transition to asyncio
```python
# Run blocking code in a thread from async context
import asyncio

async def main():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_function, arg)

# Run async code from synchronous context
def sync_function():
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(async_function())
```

- Use `run_in_executor` to call blocking code from async code
- Allows gradual migration from threads to asyncio
- Never call blocking functions directly in async code (it blocks the event loop)

## Item 63: Avoid Blocking the asyncio Event Loop to Maximize Responsiveness
- Never use `time.sleep()` in async code — use `await asyncio.sleep()`
- Never do CPU-heavy work in coroutines — use `run_in_executor`
- Never use blocking I/O calls — use async equivalents (aiohttp, aiofiles, etc.)
- Profile with `asyncio.get_event_loop().slow_callback_duration`

## Item 64: Consider concurrent.futures for True Parallelism
```python
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy(data):
    return complex_computation(data)

with ProcessPoolExecutor() as executor:
    results = list(executor.map(cpu_heavy, data_chunks))
```

- `ProcessPoolExecutor` bypasses the GIL for true CPU parallelism
- Data is serialized between processes (use for independent tasks)
- Same API as `ThreadPoolExecutor` — easy to switch
