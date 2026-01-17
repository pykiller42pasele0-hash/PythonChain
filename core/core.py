# file: core.py (Auszug)
import json
import hashlib

class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Der Fingerabdruck des Blocks
        data = json.dumps(self.transactions) + self.previous_hash + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine(self, difficulty=4):
        # Proof-of-Work: Findet einen Hash, der mit vielen Nullen beginnt
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block gemined! Hash: {self.hash}")