# src/data_ingest.py
import os, time, requests, pandas as pd
from datetime import datetime, timedelta

HV_API = "https://api.helioviewer.org/v2"
AIA_193_SOURCE_ID = 14  # verify with Helioviewer

def hv_get_closest_image(ts_iso, source_id=AIA_193_SOURCE_ID):
    r = requests.get(f"{HV_API}/getClosestImage/", params={"date": ts_iso, "sourceId": source_id})
    r.raise_for_status()
    return r.json()

def hv_get_jp2(image_id, out_path):
    r = requests.get(f"{HV_API}/getJP2Image/", params={"id": image_id}, stream=True)
    r.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        for ch in r.iter_content(8192):
            f.write(ch)

def download_euv_sequence(end_dt, hours=12, out_dir="blob/euv/193"):
    seq_paths = []
    for h in range(hours-1, -1, -1):
        t = (end_dt - timedelta(hours=h)).strftime("%Y-%m-%dT%H:%M:%SZ")
        meta = hv_get_closest_image(t)
        jp2_path = os.path.join(out_dir, f"{meta['id']}.jp2")
        if not os.path.exists(jp2_path):
            hv_get_jp2(meta["id"], jp2_path)
            time.sleep(0.25)
        seq_paths.append(jp2_path)
    return seq_paths

def download_omni_hourly(end_dt, hours=36, out_csv="blob/omni/window.csv"):
    # Minimal OMNI fetch using CDAWeb CSV (fallback). For production, use OMNIWeb API or pyomnidata.
    # Placeholder endpoint (user should replace with preferred OMNI download path).
    # Here we only scaffold: expect a pre-curated CSV present at out_csv.
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    if not os.path.exists(out_csv):
        # Create an empty CSV with expected columns so pipeline can run
        cols = ["datetime","flow_speed","bx","by_gse","bz_gse","bt","proton_density","proton_temperature"]
        pd.DataFrame(columns=cols).to_csv(out_csv, index=False)
    return out_csv
