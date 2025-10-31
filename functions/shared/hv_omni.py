# functions/shared/hv_omni.py
import os, time, json, requests, pandas as pd
from datetime import datetime, timedelta

HV_API = "https://api.helioviewer.org/v2"
AIA_193_SOURCE_ID = 14

def get_euv_sequence(hours=12):
    end_dt = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    seq = []
    for h in range(hours-1, -1, -1):
        t = (end_dt - timedelta(hours=h)).strftime("%Y-%m-%dT%H:%M:%SZ")
        m = requests.get(f"{HV_API}/getClosestImage/", params={"date": t, "sourceId": AIA_193_SOURCE_ID}).json()
        img = requests.get(f"{HV_API}/getJP2Image/", params={"id": m["id"]}).content
        # We return base64 to avoid filesystem in Functions
        seq.append({"id": m["id"], "content": img.hex()})
        time.sleep(0.2)
    return seq

def get_omni_window(hours=24):
    # Placeholder: replace with OMNIWeb fetch. Returns minimal schema.
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    rows = []
    for i in range(hours):
        t = now - timedelta(hours=hours-i)
        rows.append({
            "datetime": t.isoformat()+"Z",
            "flow_speed": 400.0,
            "bx": 0.1, "by_gse": -0.2, "bz_gse": -1.5, "bt": 3.0,
            "proton_density": 5.0, "proton_temperature": 1e5
        })
    return pd.DataFrame(rows)
