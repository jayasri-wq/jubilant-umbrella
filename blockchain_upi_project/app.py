from flask import Flask, render_template, request, redirect, session, flash, url_for
import hashlib
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Blockchain class
class Block:
    def __init__(self, sender, receiver, amount, previous_hash):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = str(datetime.now())
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        tx_data = self.sender + self.receiver + str(self.amount) + self.timestamp + self.previous_hash
        return hashlib.sha256(tx_data.encode()).hexdigest()

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis", "Genesis", 0, "0")

    def add_block(self, sender, receiver, amount):
        previous_block = self.chain[-1]
        new_block = Block(sender, receiver, amount, previous_block.hash)
        self.chain.append(new_block)
        self.save_transaction(new_block)

    def save_transaction(self, block):
        tx = block.to_dict()
        if os.path.exists("transactions.json"):
            with open("transactions.json", "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(tx)
        with open("transactions.json", "w") as f:
            json.dump(data, f, indent=4)

blockchain = Blockchain()

# Helpers
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return []

def save_user(user):
    users = load_users()
    users.append(user)
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        uname = request.form['upi']
        pwd = request.form['password']
        hashed_pwd = hash_password(pwd)

        users = load_users()
        for user in users:
            if user["upi"] == uname and user["password"] == hashed_pwd:
                session["user"] = user
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))

        flash("Invalid credentials", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        upi = request.form['upi']
        password = request.form['password']
        hashed_pwd = hash_password(password)

        user = {
            "name": name,
            "upi": upi,
            "password": hashed_pwd
        }
        save_user(user)
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if "user" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    user = session["user"]
    users = load_users()
    receivers = [u for u in users if u["upi"] != user["upi"]]

    if request.method == "POST":
        to = request.form['to']
        amount = request.form['amount']
        blockchain.add_block(user["upi"], to, float(amount))
        flash("Transaction successful!", "success")

    return render_template("dashboard.html", user=user, receivers=receivers)

@app.route('/transactions')
def transactions():
    if not os.path.exists("transactions.json"):
        txns = []
    else:
        with open("transactions.json", "r") as f:
            txns = json.load(f)
    return render_template("transactions.html", transactions=txns)

@app.route('/blockchain')
def view_blockchain():
    chain_data = [block.to_dict() for block in blockchain.chain]
    return render_template("blockchain.html", chain=chain_data)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
