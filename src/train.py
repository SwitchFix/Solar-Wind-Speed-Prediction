# src/train.py
import os, json, torch
import pandas as pd
from torch.utils.data import DataLoader
from torch.optim import AdamW
from torch.nn import HuberLoss
from dataset import MultimodalSolarWind
from model import SWindNet

def train(index_train="curated/index_train.csv", index_val="curated/index_val.csv",
          epochs=5, batch_size=2, lr=3e-4, ckpt_dir="outputs"):
    os.makedirs(ckpt_dir, exist_ok=True)
    tr = pd.read_csv(index_train, converters={"euv_paths": eval})
    va = pd.read_csv(index_val, converters={"euv_paths": eval})
    dtr = MultimodalSolarWind(tr)
    dva = MultimodalSolarWind(va)
    Ltr = DataLoader(dtr, batch_size=batch_size, shuffle=True, num_workers=0)
    Lva = DataLoader(dva, batch_size=batch_size, shuffle=False, num_workers=0)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SWindNet(ts_dim=7).to(device)
    opt = AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    loss_fn = HuberLoss()
    best = float("inf")

    for ep in range(epochs):
        model.train(); tr_loss = 0.0
        for x_img, x_ts, y in Ltr:
            x_img, x_ts, y = x_img.to(device), x_ts.to(device), y.to(device).squeeze(1)
            pred = model(x_img, x_ts)
            loss = loss_fn(pred, y)
            opt.zero_grad(); loss.backward(); opt.step()
            tr_loss += float(loss) * y.size(0)
        tr_loss /= len(dtr)

        model.eval(); va_loss = 0.0
        with torch.no_grad():
            for x_img, x_ts, y in Lva:
                x_img, x_ts, y = x_img.to(device), x_ts.to(device), y.to(device).squeeze(1)
                pred = model(x_img, x_ts)
                loss = loss_fn(pred, y)
                va_loss += float(loss) * y.size(0)
        va_loss /= len(dva)
        print(f"Epoch {ep+1}: train {tr_loss:.4f}  val {va_loss:.4f}")
        torch.save(model.state_dict(), os.path.join(ckpt_dir, "last.pt"))
        if va_loss < best:
            best = va_loss
            torch.save(model.state_dict(), os.path.join(ckpt_dir, "best.pt"))
    with open(os.path.join(ckpt_dir, "metrics.json"), "w") as f:
        json.dump({"val_loss": best}, f)

if __name__ == "__main__":
    # For demo purposes, we create a tiny synthetic index if none exists.
    os.makedirs("curated", exist_ok=True)
    if not os.path.exists("curated/index_train.csv"):
        # Minimal placeholder using fake paths; replace during real curation.
        df = pd.DataFrame([{"t":"2020-01-01T00:00:00Z","label_speed":400.0,"euv_paths":["blob/euv/193/a.jp2"]*12,"ts_window_csv":"blob/omni/window.csv"}])
        df.to_csv("curated/index_train.csv", index=False)
        df.to_csv("curated/index_val.csv", index=False)
    train()
