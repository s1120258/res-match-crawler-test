# res-match-crawler-test

Experimental module to fetch and parse job postings from job boards like Indeed. Used to test and validate data extraction and job-to-resume matching logic before integrating into the main ResMatch API.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## CLI Usage

Search Indeed for jobs:

```bash
python -m res_match_crawler.cli "python developer" -l "New York, NY" -n 10 --json -vv
```

Options:

- `keyword` (positional): search term
- `-l, --location`: location filter (optional)
- `-n, --limit`: number of results (default 20)
- `--json`: output JSON instead of plain text
- `-v / -vv`: increase verbosity

## Library Usage

```python
from res_match_crawler.scrapers import IndeedScraper

scraper = IndeedScraper()
jobs = scraper.search("data scientist", "Remote", limit=5)
for job in jobs:
    print(job.title, job.company)
```

The `jobs` variable is a list of `JobPosting` objects; you can call `to_dict()` on each to get a JSON-serializable dictionary.

## Running Tests

```bash
pytest -q
```

The unit tests stub network calls, allowing them to run quickly and offline.

## Future Work

- Implement a common interface for multiple job board scrapers.
- Integrate resume-to-job matching score computation logic.
- Add a Dockerfile and CI pipeline.
