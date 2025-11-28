import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import time
from sklearn.preprocessing import LabelEncoder

class SFTSModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SFTSModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

class NetworkSimulation:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.users_data = []
        self.load_and_preprocess_data()
    
    def load_and_preprocess_data(self):
        df = pd.read_csv(self.csv_file)
        features = df[['Age', 'Medical Condition', 'Admission Type', 'Medication']]
        target = df['Test Results']
        label_encoders = {}
        for column in features.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            features.loc[:, column] = le.fit_transform(features[column])
            label_encoders[column] = le

        features = features.astype('float32')
        target_le = LabelEncoder()
        target = target_le.fit_transform(target)
        for idx in range(len(features)):
            user_data = {
                "input": torch.tensor(features.iloc[idx].values, dtype=torch.float32),
                "target": torch.tensor([target[idx]], dtype=torch.float32)
            }
            self.users_data.append(user_data)

    def train_model(self, model, criterion, optimizer, epochs):
        print("\n==============================\n  Starting model training...\n==============================\n")
        time.sleep(5)
        for epoch in range(epochs):
            total_loss = 0.0
            correct_predictions = 0
            for user_data in self.users_data:
                inputs = user_data["input"]
                target = user_data["target"]
                output = model(inputs).squeeze()
                loss = criterion(output.unsqueeze(0), target)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                prediction = torch.round(torch.sigmoid(output)).item()
                if prediction == target.item():
                    correct_predictions += 1
            
            average_loss = total_loss / len(self.users_data)
            accuracy = correct_predictions / len(self.users_data) * 100
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {average_loss:.4f}")

        print("Model training completed.")

csv_file = 'user_health_data.csv'
input_size = 4
hidden_size = 5
output_size = 1
epochs = 50
learning_rate = 0.001
network_simulation = NetworkSimulation(csv_file)
model = SFTSModel(input_size, hidden_size, output_size)
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
network_simulation.train_model(model, criterion, optimizer, epochs)
