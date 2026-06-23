"""
FortyGuard API Test Suite
Run: python fortyguard_test.py
Replace YOUR_API_KEY below before running.
"""

import requests
import json
import time
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────────────────────────
API_KEY = ""
BASE_URL = "https://api.fortyguard.com/v1"

HEADERS = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

# Small area in Lower Manhattan (~0.5 sq mi, well within Basic 10 sq mi limit)
MANHATTAN_POLYGON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-74.0170, 40.7050],
                    [-74.0030, 40.7050],
                    [-74.0030, 40.7180],
                    [-74.0170, 40.7180],
                    [-74.0170, 40.7050]   # closed polygon (first == last)
                ]]
            }
        }
    ]
}

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def log(label, status, data):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  Status: {status}")
    print(f"  Response: {json.dumps(data, indent=2)[:800]}")  # truncate long responses
    print(f"{'='*60}")

def post(endpoint, payload, label):
    url = f"{BASE_URL}{endpoint}"
    print(f"\n[→] POST {url}")
    try:
        r = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        data = r.json() if r.text else {}
        log(label, r.status_code, data)
        return r.status_code, data
    except Exception as e:
        print(f"[!] Exception: {e}")
        return None, {}

def get(endpoint, label, params=None):
    url = f"{BASE_URL}{endpoint}"
    print(f"\n[→] GET {url}")
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        data = r.json() if r.text else {}
        log(label, r.status_code, data)
        return r.status_code, data
    except Exception as e:
        print(f"[!] Exception: {e}")
        return None, {}

def poll_activity(activity_id, label, max_wait=60):
    """Poll /status/{activity_id} until Completed or Failed."""
    print(f"\n[⏳] Polling activity {activity_id} for '{label}'...")
    for i in range(max_wait // 5):
        time.sleep(5)
        status_code, data = get(f"/status/{activity_id}", f"Poll {i+1} - {label}")
        status = data.get("status", "")
        if status in ("Completed", "Failed"):
            print(f"[✓] Final status: {status}")
            return data
    print("[!] Timed out waiting for completion.")
    return {}

# ─── TEST 1: Credits & Plan ────────────────────────────────────────────────────
print("\n" + "★"*60)
print("  FORTYGUARD API TEST SUITE")
print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("★"*60)

print("\n\n[1/6] CHECK API CREDITS & PLAN")
status, credits_data = get("/credits", "Credits Usage")

# ─── TEST 2: Create Heatmap (filter_type 1 = Single Hour) ─────────────────────
print("\n\n[2/6] CREATE HEATMAP — filter_type 1 (Single Hour)")
heatmap_payload = {
    "polygon_aoi": MANHATTAN_POLYGON,
    "date_time": {
        "start_date": "2024-07-15",
        "start_time": "14:00",
        "filter_type": 1
    },
    "granularity": 100
}
status, heatmap_resp = post("/heatmap", heatmap_payload, "Create Heatmap (Single Hour)")
heatmap_activity_id = heatmap_resp.get("activity_id")

# Poll if we got an activity_id
if heatmap_activity_id:
    heatmap_result = poll_activity(heatmap_activity_id, "Heatmap")

# ─── TEST 3: Create Heatmap (filter_type 2 = Range of Hours) ──────────────────
print("\n\n[3/6] CREATE HEATMAP — filter_type 2 (Range of Hours)")
heatmap_range_payload = {
    "polygon_aoi": MANHATTAN_POLYGON,
    "date_time": {
        "start_date": "2024-07-15",
        "start_time": "10:00",
        "end_date": "2024-07-15",
        "end_time": "13:00",
        "filter_type": 2
    },
    "granularity": 100
}
status, _ = post("/heatmap", heatmap_range_payload, "Create Heatmap (Range of Hours)")

# ─── TEST 4: Environmental Parameters ─────────────────────────────────────────
print("\n\n[4/6] ENVIRONMENTAL PARAMETERS (Basic: up to 3 params)")
env_payload = {
    "polygon_aoi": MANHATTAN_POLYGON,
    "date_time": {
        "start_date": "2024-07-15",
        "start_time": "14:00",
        "filter_type": 1
    },
    "analysis": ["geographic", "environmental", "urban"]  # 3 max on Basic
}
status, env_resp = post("/environmental-parameters", env_payload, "Environmental Parameters")
env_activity_id = env_resp.get("activity_id")
if env_activity_id:
    poll_activity(env_activity_id, "Environmental Parameters")

# ─── TEST 5: Edge Cases ────────────────────────────────────────────────────────
print("\n\n[5/6] EDGE CASES")

# 5a: Invalid coordinates (outside US)
print("\n  [5a] Invalid coordinates — Delhi, India (should 400)")
invalid_payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [77.20, 28.61], [77.22, 28.61],
                    [77.22, 28.63], [77.20, 28.63],
                    [77.20, 28.61]
                ]]
            }
        }]
    },
    "date_time": {"start_date": "2024-07-15", "start_time": "14:00", "filter_type": 1},
    "granularity": 100
}
post("/heatmap", invalid_payload, "Edge Case: Non-US coordinates")

# 5b: Missing required field
print("\n  [5b] Missing granularity field (should 400)")
missing_field_payload = {
    "polygon_aoi": MANHATTAN_POLYGON,
    "date_time": {"start_date": "2024-07-15", "start_time": "14:00", "filter_type": 1}
    # granularity intentionally omitted
}
post("/heatmap", missing_field_payload, "Edge Case: Missing granularity")

# 5c: Invalid date (before 2019-01-01)
print("\n  [5c] Date before allowed range (should 400)")
old_date_payload = {
    "polygon_aoi": MANHATTAN_POLYGON,
    "date_time": {"start_date": "2018-12-31", "start_time": "14:00", "filter_type": 1},
    "granularity": 100
}
post("/heatmap", old_date_payload, "Edge Case: Date before 2019-01-01")

# 5d: Invalid granularity value
print("\n  [5d] Invalid granularity value (should 400)")
bad_granularity_payload = {
    "polygon_aoi": MANHATTAN_POLYGON,
    "date_time": {"start_date": "2024-07-15", "start_time": "14:00", "filter_type": 1},
    "granularity": 50  # only 60, 80, 100 are valid
}
post("/heatmap", bad_granularity_payload, "Edge Case: Invalid granularity (50m)")

# 5e: Unclosed polygon
print("\n  [5e] Unclosed polygon — first != last coordinate (should 400)")
unclosed_payload = {
    "polygon_aoi": {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-74.0170, 40.7050],
                    [-74.0030, 40.7050],
                    [-74.0030, 40.7180],
                    [-74.0170, 40.7180]
                    # intentionally not closed
                ]]
            }
        }]
    },
    "date_time": {"start_date": "2024-07-15", "start_time": "14:00", "filter_type": 1},
    "granularity": 100
}
post("/heatmap", unclosed_payload, "Edge Case: Unclosed polygon")

# ─── TEST 6: Premium Endpoints (expect 403 on Basic) ──────────────────────────
print("\n\n[6/6] PREMIUM ENDPOINTS — Expect 403 on Basic plan")

base_body = {
    "polygon_aoi": MANHATTAN_POLYGON,
    "date_time": {"start_date": "2024-07-15", "start_time": "14:00", "filter_type": 1},
    "granularity": 100
}

post("/satellite-segmentation", base_body, "Satellite View Segmentation (Premium)")
post("/street-segmentation", base_body, "Street View Segmentation (Premium)")
post("/heat-intelligence", {
    "polygon_aoi": MANHATTAN_POLYGON,
    "date_time": {"start_date": "2024-07-15", "start_time": "14:00", "filter_type": 1},
    "analysis": ["geographic", "environmental", "urban"]
}, "Heat Intelligence (Premium)")

print("\n\n[✓] Test suite complete.")