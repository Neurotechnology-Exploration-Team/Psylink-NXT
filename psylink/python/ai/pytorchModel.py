import torch
import torch.nn as nn
from os.path import isfile as os.path.isfile

learning_rate = 1e-3
batch_size = 64
epochs = 15

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")

class XYZGenerator(nn.Module):
    def __init__(self):
        super(XYZGenerator, self).__init__()
        self.fc1 = nn.Linear(11, 32)
        self.fc2 = nn.Linear(32, 64)
        self.fc3 = nn.Linear(64, 128)
        self.fc4 = nn.Linear(128, 256)
        self.fc5 = nn.Linear(256, 128)
        self.fc6 = nn.Linear(128, 21*3)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):#x is an 11 float tensor
        x = self.fc1(x)         
        x = nn.ReLU(x)
        x = self.fc2(x)
        x = nn.ReLU(x)
        x = self.fc3(x)
        x = nn.ReLU(x)
        x = self.fc4(x)
        x = nn.ReLU(x)
        x = self.fc5(x)
        x = nn.ReLU(x)
        x = self.dropout(x)
        x = self.fc6(x)
        x = nn.ReLU(x)

        # Reshape to 21 XYZ coordinates
        psylink_data = psylink_data.view(-1, 21, 3)

        return psylink_data

def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        pred = model(X)
        loss = loss_fn(pred, y)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch+1) * len(X)
            print(f"loss: {loss:>7f} [{current:>5d}/{size:>5d}]")

def test_loop(dataloader, model, loss_fn){
    size = len(dataloader.dataset)
    model.eval()
    num_batches = len(dataloader)
    test_loss, correct = 0,0

    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    
    test_loss /= num_batches
    correct /= size
    print(f"Test Error:\nAccuracy: {100*correct:>0.1f}%, Avg loss: {test_loss:>8f}\n")

import torch.nn.functional as F

def loss_fn(predicted_coords, actual_coords):
    # Flatten predicted and actual coordinates
    predicted_coords = predicted_coords.view(-1, 21*3)
    actual_coords = actual_coords.view(-1, 21*3)

    # Compute L2 loss between predicted and actual coordinates
    loss = F.mse_loss(predicted_coords, actual_coords)

    return loss

if __name__ == "__main__":
    model = XYZGenerator()
    if(input("Load weights? [y/N]").lower() == 'y'):
        if(os.path.isfile('xyzgen_weights.pth')):
            model.load_state_dict(torch.load("xyzgen_weights.pth")
            print("Loaded successfully!\n")
        else:
            print("No weights found.\n")
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    
    train_dataloader = Dataloader(training_data, batch_size = batch_size)
    test_dataloader = Dataloader(testing_data, batch_size = batch_size)

    for t in range(epochs):
        print(f"Epoch: {t+1}\n----------------------------------")
        train_loop(train_dataloader, model, loss_fn, optimizer)
        test_loop(test_dataloader, model, loss_fn)

    print("Done!")

    if(input("Save weights? [y/N]").lower() == 'y'):
        torch.save(model.state_dict(), 'xyzgen_weights.pth')
