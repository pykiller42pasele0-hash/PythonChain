# -*- coding: utf-8 -*-
import sys
import io
import os
import threading
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# Importiere deine Module
from core.blockchain import PythonChain
from core.core import MiningEngine
from wallet.wallet import Wallet
from network.node import PythonChainNode

# Terminal-Erweiterung
try:
    from backend.api_extension import get_terminal_response
except ImportError:
    def get_terminal_response(cmd, bc): return "Backend Extension nicht gefunden."

# UTF-8 Fix
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- FLASK KONFIGURATION (FIXED) ---
# Hier sagen wir Flask, dass die index.html im Hauptordner liegt
app = Flask(__name__, template_folder='.', static_folder='frontend')
CORS(app)

# 1. Identitaet & Blockchain
my_wallet = Wallet()
my_identity = my_wallet.get_identity()
blockchain = PythonChain(node_wallet_address=my_identity['address'])
miner = MiningEngine(blockchain)
node = PythonChainNode(host='0.0.0.0', port=5001, wallet_address=my_identity['address'])

# --- ROUTEN ---

@app.route('/')
def index():
    """Zeigt das Dashboard an"""
    return render_template('index.html')

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    proof = miner.proof_of_work(last_block)
    if proof:
        blockchain.new_transaction(sender="0", recipient=my_identity['address'], amount=miner.calculate_coin_value())
        block = blockchain.new_block(proof)
        node.broadcast_data('NEW_BLOCK', block)
        return jsonify({'message': "Block gemined!", 'index': block['index']}), 200
    return jsonify({'message': 'Mining abgebrochen.'}), 400

@app.route('/api/terminal/execute', methods=['POST'])
def terminal_execute():
    data = request.get_json()
    response = get_terminal_response(data.get('command'), blockchain)
    return jsonify({'output': response}), 200

@app.route('/wallet/info', methods=['GET'])
def wallet_info(): return jsonify(my_identity), 200

@app.route('/chain', methods=['GET'])
def full_chain(): return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

# --- START ---
if __name__ == '__main__':
    def start_node(node_instance):
        for port in range(5001, 5010):
            try:
                node_instance.port = port
                node_instance.start_server()
                break
            except: continue

    threading.Thread(target=start_node, args=(node,), daemon=True).start()
    print(f"[*] PythonChain Dashboard: http://pykiller42.io:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)