"""Sample script to test actual Indeed scraping."""

import logging
from res_match_crawler.scrapers import IndeedScraper

# Enable detailed logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    scraper = IndeedScraper()

    # Test search
    try:
        print("Searching for Python jobs...")
        jobs = scraper.search("python developer", "Remote", limit=3)

        print(f"Found {len(jobs)} jobs:")
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job.title}")
            print(f"   Company: {job.company}")
            print(f"   Location: {job.location}")
            print(f"   URL: {job.url}")
            print(f"   Description: {job.description[:200]}...")

    except Exception as e:
        print(f"Error occurred: {e}")
        print("\nNote: Indeed may block requests. Try:")
        print("1. Adding delays between requests")
        print("2. Using different User-Agent strings")
        print("3. Using proxy servers")

if __name__ == "__main__":
    main()