"""Sample script to test LinkedIn Jobs API scraping."""

import logging
import os
from dotenv import load_dotenv
from res_match_crawler.scrapers import LinkedInAPIScraper

# Load environment variables from .env file
load_dotenv()

# Enable detailed logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    # Check if API key is set
    api_key = os.getenv("LINKEDIN_API_KEY")
    if not api_key:
        print("Error: LINKEDIN_API_KEY environment variable is not set.")
        print("\nTo set it:")
        print("export LINKEDIN_API_KEY='your_api_key_here'")
        print("\nNote: This is a sample implementation. You'll need to:")
        print("1. Get an actual LinkedIn Jobs API key from a provider")
        print("2. Update the API_ENDPOINT in linkedin_api.py")
        print("3. Adjust the JSON response parsing to match the actual API")
        return

    try:
        scraper = LinkedInAPIScraper()
        print("Searching for Python jobs via LinkedIn API...")
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
        print("\nPossible solutions:")
        print("1. Verify your API key is correct")
        print("2. Check if the API endpoint is accessible")
        print("3. Update the API_ENDPOINT in linkedin_api.py to match your provider")
        print("4. Adjust JSON field names in the response parsing")


if __name__ == "__main__":
    main()
