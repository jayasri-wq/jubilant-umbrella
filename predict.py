import cv2
import numpy as np
import joblib
import os

# Load trained model and label encoder
model = joblib.load('data/blood_group_model.pkl')
le = joblib.load('data/label_encoder.pkl')

# Image size (should match training size)
img_size = 64

# Path to test image (you can change this to any image from your dataset)
test_image_path = 'data/images/10__M_Left_middle_finger_Zcut.BMP'



# Check if image exists
if not os.path.exists(test_image_path):
    print("❌ Image not found.")
    exit()

# Read and preprocess test image
img = cv2.imread(test_image_path, cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (img_size, img_size))
img = img.flatten() / 255.0
img = img.reshape(1, -1)

# Predict
prediction = model.predict(img)
predicted_label = le.inverse_transform(prediction)

print(f"🔍 Predicted Blood Group: {predicted_label[0]}")
