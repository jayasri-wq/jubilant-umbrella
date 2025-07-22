# recommend.py

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

future_prices = {}  # make available for app

def run_recommendation():
    df = pd.read_csv("data/merged_data.csv")
    features = ['Tomato', 'Onion', 'Wheat', 'Rice', 'Potato']
    weather = ['Temperature', 'Rainfall', 'Humidity']
    cols = features + weather

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[cols])

    def create_dataset(data, window_size=12):
        X = []
        for i in range(len(data) - window_size):
            X.append(data[i:i+window_size].flatten())
        return np.array(X)

    X_all = create_dataset(scaled)

    for i, crop in enumerate(features):
        y = scaled[12:, i]
        model = LinearRegression()
        model.fit(X_all, y)

        last_12 = scaled[-12:]
        preds = []
        input_seq = last_12.copy()

        for _ in range(6):
            x = input_seq.flatten().reshape(1, -1)
            pred = model.predict(x)[0]
            preds.append(pred)
            new_row = input_seq[-1].copy()
            new_row[i] = pred
            input_seq = np.vstack([input_seq[1:], new_row])

        inv_preds = []
        for j in range(6):
            row = np.array([0]*len(cols), dtype=float)
            row[i] = preds[j]
            row = scaler.inverse_transform([row])[0]
            inv_preds.append(row[i])

        future_prices[crop] = inv_preds

# For manual testing
if __name__ == "__main__":
    run_recommendation()
    print(future_prices)
