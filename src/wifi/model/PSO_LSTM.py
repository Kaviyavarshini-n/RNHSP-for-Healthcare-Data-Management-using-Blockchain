import numpy as np
import pandas as pd
import torch
import time
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
from pyswarm import pso
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="X does not have valid feature names")
data = pd.read_csv('Preprocessed_data.txt')
X = data.drop(['attack', 'ip_src', 'ip_dest','IoT_Node_ID'], axis=1)
y = data['attack']
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32)
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = x.unsqueeze(1)
        lstm_out, _ = self.lstm(x)
        lstm_out = lstm_out[:, -1, :]
        out = self.fc(lstm_out)
        out = self.sigmoid(out)
        return out

def lstm_model(weights):
    model = LSTMModel(input_size=X_train_tensor.shape[1], hidden_size=int(weights[0]))
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    for epoch in range(50):
        model.train()
        optimizer.zero_grad()
        outputs = model(X_train_tensor)
        loss = criterion(outputs.squeeze(), y_train_tensor)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        outputs = model(X_test_tensor)
        loss = criterion(outputs.squeeze(), y_test_tensor).item()
    return loss

lb = [10]
ub = [100]
best_weights, best_loss = pso(lstm_model, lb, ub, maxiter=50, swarmsize=30)
best_model = LSTMModel(input_size=X_train_tensor.shape[1], hidden_size=int(best_weights[0]))
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(best_model.parameters(), lr=0.001)
print("\n======================\n  PSO-LSTM Training: \n======================\n")
time.sleep(3)
for epoch in range(50):
    best_model.train()
    optimizer.zero_grad()
    outputs = best_model(X_train_tensor)
    loss = criterion(outputs.squeeze(), y_train_tensor)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}: Loss: {loss.item():.3f}")

best_model.eval()
with torch.no_grad():
    y_pred = best_model(X_test_tensor).squeeze()
    y_pred = (y_pred > 0.5).float()

time.sleep(5)
print("\n======================\n  Prediction Report: \n======================\n")
time.sleep(3)
new_data = pd.DataFrame([[0, 3, 1, 0.019, 0.31, 0.06, 0.16, 0.15, 0.10, 0.21, 0.39, 0.42, 0.49, 0.19, 0.31, 0.29, 288.28, 208.50]],
                        columns=X.columns)
new_data_scaled = scaler.transform(new_data)
new_data_tensor = torch.tensor(new_data_scaled, dtype=torch.float32)
with torch.no_grad():
    prediction = best_model(new_data_tensor).squeeze()
    predicted_value = (prediction > 0.5).float().item()
    if predicted_value == 1.0:
        print(f"Predicted value: {predicted_value} - Normal")
    else:
        print(f"Predicted value: {predicted_value} - Attack")
