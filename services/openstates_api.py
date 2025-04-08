import requests
import os

OPENSTATES_API_KEY = os.getenv("OPENSTATES_API_KEY")

def search_state_bills(state_code, keyword):
    url = "https://v3.openstates.org/bills"
    params = {
        "jurisdiction": state_code,
        "q": keyword,
        "sort": "-updated_at",
        "per_page": 5,
        "apikey": OPENSTATES_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return {"error": response.text}

