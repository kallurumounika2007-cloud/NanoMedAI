import torch
import torch.nn as nn
import torch.optim as optim

class RLAgent:
    """
    Trainable RL agent
    """
    def __init__(self, lr=0.01, dose_scale=5.0):
        self.device = torch.device("cpu")
        self.model = nn.Sequential(
            nn.Linear(1, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        ).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.dose_scale = dose_scale
        self.history = []

    def decide_dose(self, glucose_list):
        if len(glucose_list) == 0:
            return 0.0
        x = torch.tensor([[float(glucose_list[-1])]], dtype=torch.float32, device=self.device)
        with torch.no_grad():
            out = self.model(x).item()
        return float(out * self.dose_scale)

    def train(self, glucose_list, target_dose, epochs=1):
        if len(glucose_list) == 0:
            return None
        x = torch.tensor([[float(glucose_list[-1])]], dtype=torch.float32, device=self.device)
        target = torch.tensor([[float(target_dose)/self.dose_scale]], dtype=torch.float32, device=self.device)
        for _ in range(epochs):
            self.optimizer.zero_grad()
            pred = self.model(x)
            loss = self.criterion(pred, target)
            loss.backward()
            self.optimizer.step()
            self.history.append(loss.item())
        return loss.item()
