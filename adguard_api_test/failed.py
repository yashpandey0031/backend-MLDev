import requests

API_KEY = ""
HEADERS = {"api-key": API_KEY}

ids = {
    "Delhi (non-US)": "27d1fe5d-b3b5-47b3-9fb3-f1dbe4ae17f2",
    "Pre-2019 date":  "fd05dec8-d827-4216-a84c-2295e192176e",
    "Unclosed polygon": "8aceab03-3348-4dda-bb73-427d69761918"
}

for label, aid in ids.items():
    r = requests.get(f"https://api.fortyguard.com/v1/status/{aid}", headers=HEADERS)
    print(f"\n{label}: {r.json()}")