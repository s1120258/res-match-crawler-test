"""Sample script to test RemoteOK API scraping."""

import logging
from res_match_crawler.scrapers import RemoteOKScraper

# Enable detailed logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    try:
        scraper = RemoteOKScraper()
        print("Searching for Python jobs via RemoteOK API...")
        jobs = scraper.search("python", limit=5)

        print(f"Found {len(jobs)} jobs:")
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job.title}")
            print(f"   Company: {job.company}")
            print(f"   Location: {job.location}")
            print(f"   URL: {job.url}")
            print(f"   Description: {job.description[:200]}...")

    except Exception as e:
        print(f"Error occurred: {e}")
        print("\nNote: RemoteOK API is free and requires no authentication.")
        print("If this fails, check your internet connection.")


if __name__ == "__main__":
    main()
