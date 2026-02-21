# After

A scraper using `requests.Session` for connection reuse, `BeautifulSoup` for HTML parsing, per-request retry logic, and polite rate limiting between pages.

```python
import logging
import time
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

USER_AGENT = "JobResearchBot/1.0 (contact: scraping@mycompany.com)"
REQUEST_DELAY_SECONDS = 2.0


@dataclass
class JobListing:
    title: str
    company: str
    salary: str


def make_session() -> requests.Session:
    """Create a session with retry logic and a descriptive User-Agent."""
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    retry_policy = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_policy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def parse_job_listings(html: str) -> list[JobListing]:
    """Extract job listings from a page of HTML using BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select("article.job-card"):
        title_el   = card.select_one("h2.job-title")
        company_el = card.select_one("span.company")
        salary_el  = card.select_one("div.salary")

        if title_el is None:
            logger.debug("Skipping card with no title element")
            continue

        jobs.append(JobListing(
            title=title_el.get_text(strip=True),
            company=company_el.get_text(strip=True) if company_el else "",
            salary=salary_el.get_text(strip=True) if salary_el else "Not specified",
        ))

    return jobs


def scrape_jobs(base_url: str, num_pages: int) -> list[JobListing]:
    """Scrape job listings across multiple pages with rate limiting."""
    session = make_session()
    all_jobs: list[JobListing] = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}?page={page}"
        logger.info("Fetching page %d: %s", page, url)

        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()
        except requests.HTTPError as exc:
            logger.error("HTTP error on page %d: %s", page, exc)
            break
        except requests.RequestException as exc:
            logger.error("Request failed on page %d: %s — stopping", page, exc)
            break

        page_jobs = parse_job_listings(response.text)
        logger.info("Extracted %d listings from page %d", len(page_jobs), page)
        all_jobs.extend(page_jobs)

        if page < num_pages:
            time.sleep(REQUEST_DELAY_SECONDS)  # be polite

    return all_jobs


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    jobs = scrape_jobs("https://jobs.example.com/listings", num_pages=20)
    print(f"Total jobs scraped: {len(jobs)}")
```

Key improvements:
- `requests.Session` with `HTTPAdapter` reuses TCP connections and retries on transient server errors — one session for all pages instead of a new connection per request (Ch 1, 14: Session reuse and retry)
- `BeautifulSoup` with CSS selectors replaces regex HTML parsing — correct, readable, and resilient to attribute ordering changes (Ch 2: Use BeautifulSoup, not regex, for HTML)
- `parse_job_listings` is a pure function that takes an HTML string and returns typed `JobListing` dataclasses — easily unit-tested with saved HTML fixtures (Ch 15: Testing scrapers)
- `None` checks on each element before `.get_text()` prevent `AttributeError` when elements are missing (Ch 2: Defensive parsing)
- `time.sleep(REQUEST_DELAY_SECONDS)` between pages respects the server; `USER_AGENT` identifies the bot with a contact address (Ch 14, 18: Rate limiting and identification)
- Specific `requests.HTTPError` and `requests.RequestException` replace the bare `except` — errors are logged with page context and the crawl stops gracefully (Ch 1, 14: Error handling)
