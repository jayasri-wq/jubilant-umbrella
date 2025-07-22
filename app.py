from flask import Flask, render_template
from recommend import future_prices, run_recommendation

app = Flask(__name__)

@app.route('/')
def home():
    run_recommendation()  # refresh data every time you open
    return render_template("index.html", future_prices=future_prices)

if __name__ == '__main__':
    app.run(debug=True)
