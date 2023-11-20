#! pip install nerf-pytorch
import torch
import nerf

model = nerf.models.NeRF()

x = torch.randn(10, 3)  # 10 samples with 3 features each
y = model(x)
print(y.shape)  # output shape: (10, 4)
