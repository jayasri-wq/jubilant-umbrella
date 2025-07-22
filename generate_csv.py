import os
import random
import pandas as pd

# Path to the image folder
image_folder = 'data/images'

# Output CSV file
output_csv = 'data/data.csv'

# List of possible blood groups
blood_groups = ['A', 'B', 'AB', 'O']

# Prepare the data list
data = []

# Go through each image file
for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.bmp', '.jpg', '.png')):
        label = random.choice(blood_groups)
        data.append([filename, label])

# Save as a CSV file
import pandas as pd
df = pd.DataFrame(data, columns=['filename', 'blood_group'])
df.to_csv(output_csv, index=False)

print("✅ CSV created: data/data.csv")
