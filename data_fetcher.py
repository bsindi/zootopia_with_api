import os
import sys
import requests
from dotenv import load_dotenv

# Load .env so API key can be kept out of the repo
load_dotenv()

API_URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = os.getenv("API_NINJAS_KEY")

def fetch_data(animal_name: str):
    """
    Fetches the animals data for the animal 'animal_name'.
    Returns: a list of animals, each animal is a dictionary:
    {
      'name': ...,
      'taxonomy': { ... },
      'locations': [ ... ],
      'characteristics': { ... }
    }
    """
    if not API_KEY:
        print("Error: Please set API_NINJAS_KEY in your environment (e.g. .env).")
        sys.exit(1)

    headers = {"X-Api-Key": API_KEY}
    params = {"name": animal_name}
    resp = requests.get(API_URL, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()  # list (possibly empty)
