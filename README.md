# res-match-crawler-test

Experimental module to fetch and parse remote job postings. At the moment the project supports only the RemoteOK public API. The code is used to validate data extraction and job-to-resume matching logic before integrating into the main ResMatch API.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Example Usage (script)

Run the bundled sample script which fetches jobs from RemoteOK and prints the first few lines of the full description:

```bash
python main.py
```

The script queries RemoteOK for the keyword `python` and prints 3 matching jobs with full descriptions.

## Library Usage

```python
from res_match_crawler.scrapers import RemoteOKScraper

scraper = RemoteOKScraper()
jobs = scraper.search("python", limit=5)
for job in jobs:
    print(job.title, job.company)
```

The `jobs` variable is a list of `JobPosting` objects; you can call `to_dict()` on each to get a JSON-serialisable dictionary.

## Running Tests

```bash
pytest -q
```

The unit tests stub network calls, allowing them to run quickly and offline.

## Roadmap

- Add CLI support for selecting different scrapers (`remoteok`, `indeed`, etc.).
- Re-enable Indeed and LinkedIn scrapers once reliable API access is in place.
- Integrate resume-to-job matching score computation logic.
- Add a Dockerfile and CI pipeline.
