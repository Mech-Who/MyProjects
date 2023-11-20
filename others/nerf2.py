import torch
from torch import nn
from torch.nn import functional as F

class NeRF(nn.Module):
    def __init__(self, input_dims, output_dims, hidden_dims=256, num_layers=8):
        super().__init__()

        self.input_dims = input_dims
        self.output_dims = output_dims

        # MLP layers
        layers = []
        for i in range(num_layers):
            layers.append(nn.Linear(input_dims, hidden_dims))
            layers.append(nn.ReLU(inplace=True))
            input_dims = hidden_dims
        layers.append(nn.Linear(hidden_dims, output_dims))
        self.mlp = nn.Sequential(*layers)

    def forward(self, x):
        x = self.mlp(x)
        return x

# create model instance
model = NeRF(input_dims=3, output_dims=3)

# generate input data
x = torch.randn(10, 3)

# forward pass
y = model(x)
print(y.shape)  # (10, 3)
