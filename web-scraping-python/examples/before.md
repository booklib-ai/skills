# Before

A scraper that hammers a job listings site with no delays, parses HTML with regex, swallows all errors, and creates a new TCP connection for every page.

```python
import urllib.request
import re

def scrape_jobs(base_url, num_pages):
    all_jobs = []

    for page in range(1, num_pages + 1):
        url = base_url + "?page=" + str(page)
        try:
            # New connection every request, no headers, no rate limiting
            response = urllib.request.urlopen(url)
            html = response.read().decode("utf-8")
        except:
            # Swallows every error — silent failures
            continue

        # Parsing HTML with regex — fragile and incorrect
        titles = re.findall(r'<h2 class="job-title">(.*?)</h2>', html)
        companies = re.findall(r'<span class="company">(.*?)</span>', html)
        salaries = re.findall(r'<div class="salary">(.*?)</div>', html)

        for i in range(len(titles)):
            job = {
                "title": titles[i],
                "company": companies[i] if i < len(companies) else "",
                "salary": salaries[i] if i < len(salaries) else "",
            }
            all_jobs.append(job)

    return all_jobs


jobs = scrape_jobs("https://jobs.example.com/listings", 20)
print(f"Scraped {len(jobs)} jobs")
```
