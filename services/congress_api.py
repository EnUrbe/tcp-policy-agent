import requests

def search_federal_bills(keyword):
    url = "https://www.govtrack.us/api/v2/bill"
    params = {
        "q": keyword,
        "sort": "-introduced_date",
        "limit": 5
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["objects"]
    else:
        return {"error": response.text}

