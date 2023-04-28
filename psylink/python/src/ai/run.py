from pytorchModel import *

# Initialize model
model = XYZGenerator()

# Define optimizer and learning rate
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
isTraining = True
while(isTraining):
    # Zero out gradients
    optimizer.zero_grad()

    # Forward pass
    predicted_coords = model(emgs, accel)

    # Compute loss
    loss = loss_fn(predicted_coords, actual_coords)

    # Backward pass
    loss.backward()

    # Update parameters
    optimizer.step()

    # Print loss every 10 batches
    if batch_idx % 10 == 0:
        print(f"Epoch {epoch}, Batch {batch_idx}, Loss {loss.item():.4f}")

