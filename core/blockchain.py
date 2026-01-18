# -*- coding: utf-8 -*-
import hashlib
import json
from time import time

class PythonChain:
    def __init__(self, node_wallet_address):
        self.chain = []
        self.pending_transactions = []
        self.node_wallet = node_wallet_address # Deine Master-ID vom Wallet
        self.difficulty = 4 # Start-Schwierigkeit (Energetischer Schwellenwert)
        
        # Der Genesis-Block (Block 0)
        # Hier wird deine Domain pykiller42 kryptografisch verankert
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_transaction = {
            'sender': "SYSTEM",
            'recipient': self.node_wallet,
            'amount': 1000000, # Deine Initial-Versorgung
            'message': "PythonChain Genesis - Domain: pykiller42-hash"
        }
        self.pending_transactions.append(genesis_transaction)
        self.new_block(proof=100, previous_hash="0" * 64)

    def new_block(self, proof, previous_hash=None):
        """Erstellt einen neuen Block nach erfolgreichem energetischem Beweis"""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'difficulty': self.difficulty
        }
        
        # Leere den Pool der ausstehenden Transaktionen
        self.pending_transactions = []
        self.chain.append(block)
        
        # Speichere die Kette lokal (Persistenz)
        self.save_to_disk()
        return block

    def new_transaction(self, sender, recipient, amount, signature=None):
        """Fuegt eine neue Transaktion hinzu (Muss spaeter signiert sein)"""
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': time()
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """Erzeugt einen SHA-256 Hash eines Blocks (Double Hashing faehig)"""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def valid_proof(self, last_proof, proof, last_hash):
        """Validiert den energetischen Beweis (Proof of Work)"""
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:self.difficulty] == "0" * self.difficulty

    def save_to_disk(self):
        """Autonome Datensicherung"""
        with open('blockchain_data.json', 'w') as f:
            json.dump(self.chain, f, indent=4)
