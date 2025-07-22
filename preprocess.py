import os
import pandas as pd
import numpy as np
import cv2
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

print("🔁 Script started")

# Paths
csv_path = 'data/data.csv'
image_folder = 'data/images'

# Image size (smaller = faster)
img_size = 64

# Load CSV
if not os.path.exists(csv_path):
    print("❌ data.csv not found.")
    exit()

df = pd.read_csv(csv_path)

X = []
y = []

print(f"📄 Total records in CSV: {len(df)}")

# Process each image
for i, row in df.iterrows():
    filename = row['filename']
    label = row['blood_group']
    img_path = os.path.join(image_folder, filename)

    print(f"📸 Processing: {filename}")

    # Read image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"⚠️ Skipping unreadable image: {filename}")
        continue

    # Resize and normalize
    img = cv2.resize(img, (img_size, img_size))
    img = img.flatten() / 255.0

    X.append(img)
    y.append(label)

# Convert to arrays
if len(X) == 0:
    print("❌ No images processed. Please check your image folder and CSV.")
    exit()

X = np.array(X)
y = np.array(y)

# Encode labels
le = LabelEncoder()
y = le.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
print("🌲 Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"✅ Training complete! Accuracy: {acc * 100:.2f}%")
print(f"🏷️ Classes: {le.classes_}")

# Save model and encoder
joblib.dump(model, 'data/blood_group_model.pkl')
joblib.dump(le, 'data/label_encoder.pkl')
print("💾 Model and label encoder saved in 'data/' folder.")
