# src/prepare_index.py
"""
Builds index_train.csv and index_val.csv by aligning EUV sequences with OMNI windows.
Assumes EUV JP2 files and OMNI CSVs already exist in blob/.
"""
import os, glob, pandas as pd
from datetime import datetime

def build_index(euv_glob="blob/euv/193/*.jp2", omni_csv="blob/omni/window.csv", out_dir="curated"):
    os.makedirs(out_dir, exist_ok=True)
    # Placeholder logic: in production, you would time-align EUV sequences (length=12)
    # with an OMNI window (length=24) and the next-hour label_speed.
    # Here we create a tiny index row expecting you to replace with real alignment.
    row = {"t":"2020-01-01T00:00:00Z","label_speed":400.0,
           "euv_paths": sorted(glob.glob(euv_glob))[:12],
           "ts_window_csv": omni_csv}
    df = pd.DataFrame([row])
    df.to_csv(os.path.join(out_dir,"index_train.csv"), index=False)
    df.to_csv(os.path.join(out_dir,"index_val.csv"), index=False)

if __name__ == "__main__":
    build_index()
