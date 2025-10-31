# src/serve/score.py
import os, json, torch
from fastapi import FastAPI, Request
from model import SWindNet

app = FastAPI()
device = "cuda" if torch.cuda.is_available() else "cpu"
model = None

@app.on_event("startup")
def init():
    global model
    model = SWindNet(ts_dim=7)
    # When deployed in AML, best.pt is mounted at AZUREML_MODEL_DIR or relative path
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR","."), "best.pt")
    if not os.path.exists(model_path):
        model_path = "best.pt"
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device).eval()

@app.post("/score")
async def score(request: Request):
    payload = await request.json()
    x_img = torch.tensor(payload["x_img"], dtype=torch.float32).unsqueeze(0).to(device)  # (1,T,1,H,W)
    x_ts  = torch.tensor(payload["x_ts"],  dtype=torch.float32).unsqueeze(0).to(device)  # (1,T,F)
    with torch.no_grad():
        y = model(x_img, x_ts).item()
    return {"speed_km_s": y}
