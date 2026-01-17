# -*- coding: utf-8 -*-
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from core.blockchain import PythonChain

# Erzwingt UTF-8 fuer die Konsole
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)

blockchain = PythonChain()

@app.route('/mine', methods=['GET'])
def mine():
    proof = 100 
    block = blockchain.new_block(proof)
    response = {
        'message': "Neuer Block erfolgreich gemined!",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    if not values:
        return 'Keine Daten empfangen', 400
        
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Fehlende Daten', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaktion wird Block {index} hinzugefuegt'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/', methods=['GET'])
def home():
    return "Blockchain Server laeuft auf Port 5000!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)