import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import pandas as pd

# -----------------------------
# 1. Define a simple neural net
# -----------------------------
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28*28)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# -----------------------------
# 2. Load MNIST dataset
# -----------------------------
transform = transforms.Compose([transforms.ToTensor()])
train_dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# -----------------------------
# 3. Initialize model, loss, optimizer
# -----------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleNet().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=1e-4)

# -----------------------------
# 4. Training loop with logging
# -----------------------------
epochs = 5
log = []

for epoch in range(1, epochs+1):
    model.train()
    total_loss, correct, total = 0, 0, 0

    for data, target in train_loader:
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()

        # Gradient norm (proxy for selection S)
        grad_norm = 0.0
        for p in model.parameters():
            if p.grad is not None:
                grad_norm += p.grad.data.norm(2).item()

        optimizer.step()

        total_loss += loss.item() * data.size(0)
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()

    avg_loss = total_loss / total
    accuracy = correct / total

    # -----------------------------
    # Map to adaptation law fields
    # -----------------------------
    time = epoch
    P_star = accuracy  # normalized performance
    V = optimizer.param_groups[0]['lr']  # learning rate as proxy for variation
    S = grad_norm / len(train_loader)    # gradient norm as proxy for selection
    C = optimizer.param_groups[0]['weight_decay']  # regularization as constraint
    B = (V**1 * S**1) / (C**1 + 1e-8) * time

    log.append({
        "time": time,
        "loss": avg_loss,
        "accuracy": accuracy,
        "P_star": P_star,
        "V": V,
        "S": S,
        "C": C,
        "B": B
    })

    print(f"Epoch {epoch}: Loss={avg_loss:.4f}, Acc={accuracy:.4f}, V={V}, S={S:.4f}, C={C}, B={B:.4f}")

# -----------------------------
# 5. Save logs to CSV
# -----------------------------
df = pd.DataFrame(log)
df.to_csv("ml_adaptation_metrics.csv", index=False)
print("✅ Saved ml_adaptation_metrics.csv")
