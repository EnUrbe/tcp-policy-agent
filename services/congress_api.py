import requests

def search_federal_bills(keyword):
    """
    Returns top 5 bills from GovTrack that match 'keyword'.
    """
    url = "https://www.govtrack.us/api/v2/bill"
    params = {
        "q": keyword,
        "sort": "-introduced_date",
        "limit": 5
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("objects", [])
    else:
        return {"error": response.text}
