import torch
import torch.nn as nn

class XYZGenerator(nn.Module):
    def __init__(self):
        super(XYZGenerator, self).__init__()
        self.fc1 = nn.Linear(11, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 256)
        self.fc4 = nn.Linear(256, 64)
        self.fc5 = nn.Linear(64, 21*3)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

    def forward(self, x, accel):
        # Combine 8 emg signals with accelerometer data
        x = torch.cat((x, accel), dim=1)
        
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc5(x)
        x = self.relu(x)

        # Reshape to 21 XYZ coordinates
        x = x.view(-1, 21, 3)

        return x

import torch.nn.functional as F

def loss_fn(predicted_coords, actual_coords):
    # Flatten predicted and actual coordinates
    predicted_coords = predicted_coords.view(-1, 21*3)
    actual_coords = actual_coords.view(-1, 21*3)

    # Compute L2 loss between predicted and actual coordinates
    loss = F.mse_loss(predicted_coords, actual_coords)

    return loss

