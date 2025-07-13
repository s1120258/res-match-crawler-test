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

`jobs` は `JobPosting` オブジェクトのリストで、`to_dict()` で辞書化できます。

## Running Tests

```bash
pytest -q
```

ユニットテストではネットワークをスタブ化してあるため、オフラインで高速に実行可能です。

## Future Work

- 複数ジョブボード対応の共通インターフェース実装
- レジュメとのマッチングスコア計算ロジックとの統合
- Dockerfile / CI パイプライン追加
