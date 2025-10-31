# src/dataset.py
import cv2, numpy as np, pandas as pd, torch
from torch.utils.data import Dataset

def read_jp2(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(path)
    img = img.astype(np.float32)
    mn, mx = np.nanmin(img), np.nanmax(img)
    img = (img - mn) / (mx - mn + 1e-6)
    return img

class MultimodalSolarWind(Dataset):
    def __init__(self, index_df, seq_len_img=12, seq_len_ts=24, img_size=256, horizon=1):
        self.df = index_df.reset_index(drop=True)
        self.seq_len_img = seq_len_img
        self.seq_len_ts = seq_len_ts
        self.img_size = img_size
        self.horizon = horizon

    def __len__(self):
        return len(self.df)

    def __getitem__(self, i):
        row = self.df.iloc[i]
        imgs = []
        for p in row.euv_paths[-self.seq_len_img:]:
            im = cv2.resize(read_jp2(p), (self.img_size, self.img_size))
            imgs.append(im)
        x_img = np.stack(imgs, 0)[...,None]  # (T,H,W,1)
        x_img = np.transpose(x_img, (0,3,1,2))  # (T,1,H,W)
        x_img = torch.from_numpy(x_img)

        ts = pd.read_csv(row.ts_window_csv, parse_dates=["datetime"]).tail(self.seq_len_ts)
        feats = ts[["flow_speed","bx","by_gse","bz_gse","bt","proton_density","proton_temperature"]].values.astype(np.float32)
        mu = feats.mean(0, keepdims=True); sd = feats.std(0, keepdims=True)+1e-6
        x_ts = (feats - mu) / sd
        x_ts = torch.from_numpy(x_ts)

        y = torch.tensor([row.label_speed], dtype=torch.float32)
        return x_img, x_ts, y
