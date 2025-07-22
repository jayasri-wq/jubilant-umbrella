import json
from blockchain import Blockchain

# Load user data
def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

# Save updated user data
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Transfer function
def transfer_money(sender_upi, receiver_upi, amount, blockchain):
    users = load_users()

    # Check if users exist
    sender = None
    receiver = None
    for user in users.values():
        if user['upi_id'] == sender_upi:
            sender = user
        if user['upi_id'] == receiver_upi:
            receiver = user

    if not sender or not receiver:
        print("❌ UPI ID not found.")
        return

    if sender['balance'] < amount:
        print("❌ Insufficient balance.")
        return

    # Update balances
    sender['balance'] -= amount
    receiver['balance'] += amount
    save_users(users)

    # Create transaction
    transaction = {
        'from': sender_upi,
        'to': receiver_upi,
        'amount': amount
    }

    blockchain.add_block([transaction])
    print("✅ Transaction successful and recorded on blockchain!")

# View all transactions
def view_blockchain(blockchain):
    for block in blockchain.chain:
        print(f"\nBlock {block.index}:")
        print(f"  Transactions: {block.transactions}")
        print(f"  Hash: {block.hash}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Time: {block.timestamp}")

# Main loop
def main():
    blockchain = Blockchain()

    while True:
        print("\n--- Secure UPI Transaction ---")
        print("1. Send Money")
        print("2. View Blockchain")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            sender = input("Sender UPI ID: ")
            receiver = input("Receiver UPI ID: ")
            amount = float(input("Amount to send: "))
            transfer_money(sender, receiver, amount, blockchain)

        elif choice == '2':
            view_blockchain(blockchain)

        elif choice == '3':
            break

        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
