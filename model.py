# model.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# Load merged data
df = pd.read_csv("data/merged_data.csv")

# Select relevant columns
features = ['Tomato', 'Temperature', 'Rainfall', 'Humidity']
df = df[features]

# Normalize data
scaler = MinMaxScaler()
scaled = scaler.fit_transform(df)

# Create sliding window dataset (12 months input → 1 month target)
def create_sequences(data, window_size):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i].flatten())  # flatten 12x4 into 48 features
        y.append(data[i][0])  # target: Tomato price
    return np.array(X), np.array(y)

window_size = 12
X, y = create_sequences(scaled, window_size)

# Train-test split (last 6 for test)
X_train, X_test = X[:-6], X[-6:]
y_train, y_test = y[:-6], y[-6:]

# Build and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict next 6 months
predictions = model.predict(X_test)

# Inverse transform predictions
def inverse_transform(preds, X_test):
    full = np.hstack([preds.reshape(-1, 1), X_test[:, -3:].reshape(-1, 3)])
    return scaler.inverse_transform(full)[:, 0]

predicted_prices = inverse_transform(predictions, X_test)
actual_prices = inverse_transform(y_test, X_test)

# Plot results
plt.figure(figsize=(8, 5))
plt.plot(range(1, 7), actual_prices, marker='o', label='Actual Price')
plt.plot(range(1, 7), predicted_prices, marker='x', label='Predicted Price')
plt.title('Tomato Price Prediction (Linear Regression)')
plt.xlabel('Month Index')
plt.ylabel('Price (₹)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
