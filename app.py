# -*- coding: utf-8 -*-
import sys
import io
import os
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS

# Importiere deine souveraenen Module
from core.blockchain import PythonChain
from core.core import MiningEngine
from wallet.wallet import Wallet
from network.node import PythonChainNode

# Importiere die neue Terminal-Erweiterung aus dem Backend-Ordner
try:
    from backend.api_extension import get_terminal_response
except ImportError:
    # Fallback falls die Datei noch nicht am Platz ist
    def get_terminal_response(cmd, bc): return "Backend Extension nicht gefunden."

# UTF-8 Fix fuer Windows-Konsolen
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)

# --- INITIALISIERUNG ---

# 1. Identitaet laden (Aus private.txt)
my_wallet = Wallet()
my_identity = my_wallet.get_identity()

# 2. Blockchain mit Master-ID starten
blockchain = PythonChain(node_wallet_address=my_identity['address'])

# 3. Mining-Engine und Netzwerk-Node initialisieren
miner = MiningEngine(blockchain)
node = PythonChainNode(host='0.0.0.0', port=5001, wallet_address=my_identity['address'])

# Versuche C++ Bridge zu laden (Fallback-Logik)
try:
    import ctypes
    if os.path.exists('backend/bridge.so'):
        bridge = ctypes.CDLL('./backend/bridge.so')
        print("[*] C++ Bridge aktiv: High-Speed Mining bereit.")
    else:
        print("[!] C++ Bridge nicht gefunden. Nutze stabilen Python-Kern.")
except Exception:
    print("[!] Nutze Python-Standard f�r Berechnungen.")

# --- API ENDPUNKTE ---

@app.route('/mine', methods=['GET'])
def mine():
    """Startet den energetischen Mining-Prozess"""
    last_block = blockchain.last_block
    proof = miner.proof_of_work(last_block)
    
    if proof:
        blockchain.new_transaction(
            sender="0", 
            recipient=my_identity['address'], 
            amount=miner.calculate_coin_value()
        )
        block = blockchain.new_block(proof)
        node.broadcast_data('NEW_BLOCK', block)
        
        return jsonify({
            'message': "Block gemined!",
            'index': block['index'],
            'energy_value': miner.calculate_coin_value()
        }), 200
    return jsonify({'message': 'Mining abgebrochen.'}), 400

@app.route('/wallet/info', methods=['GET'])
def wallet_info():
    return jsonify(my_identity), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'difficulty': blockchain.difficulty
    }), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    signature = my_wallet.sign_transaction(f"{my_identity['address']}{values['recipient']}{values['amount']}")
    index = blockchain.new_transaction(
        sender=my_identity['address'], 
        recipient=values['recipient'], 
        amount=values['amount'],
        signature=signature
    )
    return jsonify({'message': f'Transaktion in Block {index} eingereiht.'}), 201

# --- PCCMD TERMINAL ENDPUNKT ---

@app.route('/api/terminal/execute', methods=['POST'])
def terminal_execute():
    """Endpunkt fuer das Web-Terminal"""
    data = request.get_json()
    command = data.get('command')
    # Fuehrt den Befehl ueber die api_extension aus
    response = get_terminal_response(command, blockchain)
    return jsonify({'output': response}), 200

# --- START-LOGIK ---

if __name__ == '__main__':
    # Intelligente Port-Suche fuer den Mesh-Node (Resilienz-Funktion)
    def start_node_with_retry(node_instance, start_port):
        current_port = start_port
        while current_port < start_port + 10:
            try:
                node_instance.port = current_port
                node_instance.start_server()
                break
            except Exception:
                print(f"[!] Port {current_port} belegt. Versuche {current_port + 1}...")
                current_port += 1

    # Netzwerk-Thread starten
    node_thread = threading.Thread(
        target=start_node_with_retry, 
        args=(node, 5001), 
        daemon=True
    )
    node_thread.start()
    
    print(f"[*] PythonChain Dashboard: http://localhost:5000")
    print(f"[*] Master-Adresse: {my_identity['address']}")
    
    # Flask Webserver starten
    app.run(host='0.0.0.0', port=5000, debug=False)
