# -*- coding: utf-8 -*-
import sys
import io
from flask import Flask, jsonify, request
from flask_cors import CORS

# Importiere deine neuen, souveraenen Module
from core.blockchain import PythonChain
from core.core import MiningEngine
from wallet.wallet import Wallet
from network.node import PythonChainNode

# UTF-8 Fix fuer Windows-Konsolen
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)

# 1. Identitaet laden (Aus private.txt)
my_wallet = Wallet()
my_identity = my_wallet.get_identity()

# 2. Blockchain mit Master-ID starten
blockchain = PythonChain(node_wallet_address=my_identity['address'])

# 3. Mining-Engine und Netzwerk-Node initialisieren
miner = MiningEngine(blockchain)
# Node auf Port 5001 (getrennt vom Web-Interface auf 5000)
node = PythonChainNode(host='0.0.0.0', port=5001, wallet_address=my_identity['address'])

@app.route('/mine', methods=['GET'])
def mine():
    """Startet den energetischen Mining-Prozess"""
    last_block = blockchain.last_block
    # Die Engine arbeitet jetzt probabilistisch (Energie-Einsatz)
    proof = miner.proof_of_work(last_block)
    
    if proof:
        # Belohnung fuer den Master (Minting)
        blockchain.new_transaction(
            sender="0", 
            recipient=my_identity['address'], 
            amount=miner.calculate_coin_value()
        )
        block = blockchain.new_block(proof)
        
        # Den neuen Block ins Mesh-Netzwerk broadcasten
        node.broadcast_data('NEW_BLOCK', block)
        
        return jsonify({
            'message': "Energetischer Beweis erbracht. Block gemined!",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'energy_value': miner.calculate_coin_value()
        }), 200
    return jsonify({'message': 'Mining abgebrochen.'}), 400

@app.route('/wallet/info', methods=['GET'])
def wallet_info():
    """Gibt deine Domain-Infos an das Dashboard weiter"""
    return jsonify(my_identity), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['recipient', 'amount']
    if not all(k in values for k in required):
        return 'Fehlende Daten', 400

    # Hier wird die Transaktion automatisch mit deinem Master-Key signiert
    signature = my_wallet.sign_transaction(f"{my_identity['address']}{values['recipient']}{values['amount']}")
    
    index = blockchain.new_transaction(
        sender=my_identity['address'], 
        recipient=values['recipient'], 
        amount=values['amount'],
        signature=signature
    )
    return jsonify({'message': f'Transaktion signiert und an Block {index} gesendet.'}), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'difficulty': blockchain.difficulty
    }), 200

if __name__ == '__main__':
    # Starte den Netzwerk-Node in einem eigenen Thread
    import threading
    threading.Thread(target=node.start_server, daemon=True).start()
    
    # Starte das Web-Interface
    app.run(host='0.0.0.0', port=5000, debug=False)
