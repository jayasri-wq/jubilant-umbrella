from flask import Flask, render_template, request
import numpy as np
from PIL import Image
import joblib

app = Flask(__name__)
model = joblib.load('data/blood_group_model.pkl')
le = joblib.load('data/label_encoder.pkl')
img_size = 64

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files["file"]
        if file.filename.endswith(".BMP"):
            img = Image.open(file).convert("L")
            img = img.resize((img_size, img_size))
            img_array = np.array(img).astype(np.float32) / 255.0
            img_array = img_array.flatten().reshape(1, -1)

            pred = model.predict(img_array)
            result = le.inverse_transform(pred)[0]
        else:
            result = "❌ Invalid file. Please upload a .BMP image."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
