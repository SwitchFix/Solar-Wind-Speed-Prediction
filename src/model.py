# src/model.py
import torch, torch.nn as nn
from torchvision.models import resnet18

class CNNEncoder(nn.Module):
    def __init__(self, out_dim=256):
        super().__init__()
        base = resnet18(weights=None)
        base.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.backbone = nn.Sequential(*list(base.children())[:-1])
        self.proj = nn.Linear(512, out_dim)

    def forward(self, x):
        feat = self.backbone(x).flatten(1)
        return self.proj(feat)

class VisionTemporal(nn.Module):
    def __init__(self, enc_dim=256, hidden=256, layers=1):
        super().__init__()
        self.enc = CNNEncoder(out_dim=enc_dim)
        self.lstm = nn.LSTM(enc_dim, hidden, num_layers=layers, batch_first=True)
    def forward(self, x_seq):
        B,T,_,H,W = x_seq.shape
        x = x_seq.reshape(B*T,1,H,W)
        f = self.enc(x)
        f = f.view(B,T,-1)
        _, (h,_) = self.lstm(f)
        return h[-1]

class TSBranch(nn.Module):
    def __init__(self, f_in, hidden=128, layers=2):
        super().__init__()
        self.lstm = nn.LSTM(f_in, hidden, num_layers=layers, batch_first=True)
    def forward(self, x):
        _, (h,_) = self.lstm(x)
        return h[-1]

class SWindNet(nn.Module):
    def __init__(self, ts_dim=7, v_hidden=256, ts_hidden=128):
        super().__init__()
        self.vision = VisionTemporal(256, v_hidden, 1)
        self.ts = TSBranch(ts_dim, ts_hidden, 2)
        self.head = nn.Sequential(
            nn.Linear(v_hidden+ts_hidden, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 1)
        )
    def forward(self, x_img, x_ts):
        v = self.vision(x_img)
        t = self.ts(x_ts)
        x = torch.cat([v,t], dim=1)
        return self.head(x).squeeze(1)
