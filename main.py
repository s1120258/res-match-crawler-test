"""Sample script to test RemoteOK API scraping."""

import logging
from res_match_crawler.scrapers import RemoteOKScraper

# Enable detailed logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    try:
        scraper = RemoteOKScraper()
        print("Searching for Python jobs via RemoteOK API...")
        print("(Fetching full descriptions - this may take a moment...)")

        # Set fetch_full_description=False for faster testing
        jobs = scraper.search("python", limit=3, fetch_full_description=True)

        print(f"\nFound {len(jobs)} jobs:")
        for i, job in enumerate(jobs, 1):
            print(f"\n{'='*80}")
            print(f"{i}. {job.title}")
            print(f"Company: {job.company}")
            print(f"Location: {job.location}")
            print(f"URL: {job.url}")
            print(f"\nDescription:")
            print("-" * 40)
            # Show more of the description
            desc_lines = job.description.split('\n')[:15]  # First 15 lines
            for line in desc_lines:
                if line.strip():
                    print(line.strip())
            if len(job.description.split('\n')) > 15:
                print("... (truncated)")

    except Exception as e:
        print(f"Error occurred: {e}")
        print("\nNote: RemoteOK API is free and requires no authentication.")
        print("If this fails, check your internet connection.")


if __name__ == "__main__":
    main()
