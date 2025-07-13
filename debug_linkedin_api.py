"""Debug script to test LinkedIn API and identify 403 error cause."""

import logging
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable debug logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


def test_api_directly():
    """Test the API directly to debug 403 error."""
    api_key = os.getenv("LINKEDIN_API_KEY")
    if not api_key:
        print("Error: LINKEDIN_API_KEY not found")
        return

    print(f"Using API key: {api_key[:10]}...")

    # Test different endpoints
    endpoints = [
        "https://linkedin-jobs-search.p.rapidapi.com/search",
        "https://linkedin-jobs-search.p.rapidapi.com/",
        "https://linkedin-data-api.p.rapidapi.com/search-jobs",
    ]

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "linkedin-jobs-search.p.rapidapi.com",
    }

    params = {"keywords": "python", "location": "Remote", "limit": "3"}

    session = requests.Session()
    session.headers.update(headers)

    for endpoint in endpoints:
        print(f"\n--- Testing endpoint: {endpoint} ---")
        try:
            response = session.get(endpoint, params=params, timeout=30)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")

            if response.status_code == 403:
                print(f"403 Error content: {response.text[:500]}")
            elif response.status_code == 200:
                print("Success! Response preview:")
                data = response.json()
                print(
                    f"Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}"
                )
                break
            else:
                print(f"Response: {response.text[:200]}")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    test_api_directly()
