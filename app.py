# -*- coding: utf-8 -*-
import sys
import io
import os
import threading
import time
from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS

# --- CORE MODULE IMPORT ---
from core.blockchain import PythonChain
from core.core import MiningEngine
from wallet.wallet import Wallet
from network.node import PythonChainNode

# Terminal-Erweiterung (PCCMD Logic)
try:
    from backend.api_extension import get_terminal_response
except ImportError:
    def get_terminal_response(cmd, bc): return "Backend Extension nicht gefunden."

# UTF-8 Fix für Windows Konsolen-Resonanz
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- FLASK & SOVEREIGN CONFIG ---
app = Flask(__name__, template_folder='.', static_folder='frontend')
CORS(app)

# 1. Identität & Blockchain Initialisierung
my_wallet = Wallet()
my_identity = my_wallet.get_identity()
blockchain = PythonChain(node_wallet_address=my_identity['address'])
miner = MiningEngine(blockchain)
node = PythonChainNode(host='0.0.0.0', port=5001, wallet_address=my_identity['address'])

# --- AUTONOMER MATHEMATISCHER CORE (DAEMON) ---
def autonomous_heartbeat():
    """Der autonome Prozess: Mined Blöcke ohne Ladezeit durch deterministische Mathematik"""
    print(f"[*] WWPC Autonomous Core aktiv. Master: {my_identity['address']}")
    while True:
        try:
            last_block = blockchain.last_block
            # Probabilistisches Mining im Hintergrund
            proof = miner.proof_of_work(last_block)
            
            if proof:
                blockchain.new_transaction(
                    sender="0", 
                    recipient=my_identity['address'], 
                    amount=miner.calculate_coin_value()
                )
                block = blockchain.new_block(proof)
                node.broadcast_data('NEW_BLOCK', block)
                print(f"[MATHEMATIK] Autonomer Block {block['index']} versiegelt (Resonanz 0ms)")
        except Exception as e:
            print(f"[!] Core Heartbeat Fehler: {e}")
        
        time.sleep(1) # Taktung der Resonanz

# --- MIDDLEWARE: DOMAIN & HTTPS ENFORCEMENT ---
@app.before_request
def enforce_sovereign_protocol():
    # Erzwingt HTTPS und checkt Domain-Konsistenz (.io / .pio)
    if not request.is_secure and 'localhost' not in request.host:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

@app.after_request
def apply_security_headers(response):
    # HSTS für Zero-Latency SSL Resonanz
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-World-Wide-PythonChain"] = "Sovereign-Node-v1.0"
    return response

# --- API ROUTEN ---

@app.route('/')
def index():
    """Liefert die dApp Oberfläche"""
    return render_template('index.html')

@app.route('/mine', methods=['GET'])
def manual_mine():
    """Manueller Mining-Trigger (für das Dashboard UI)"""
    last_block = blockchain.last_block
    proof = miner.proof_of_work(last_block)
    if proof:
        blockchain.new_transaction(sender="0", recipient=my_identity['address'], amount=miner.calculate_coin_value())
        block = blockchain.new_block(proof)
        return jsonify({'status': 'success', 'block': block}), 200
    return jsonify({'status': 'error', 'message': 'Mining abgebrochen'}), 400

@app.route('/api/terminal/execute', methods=['POST'])
def terminal_execute():
    data = request.get_json()
    response = get_terminal_response(data.get('command'), blockchain)
    return jsonify({'output': response}), 200

@app.route('/wallet/info', methods=['GET'])
def wallet_info(): return jsonify(my_identity), 200

@app.route('/chain', methods=['GET'])
def full_chain(): 
    return jsonify({
        'chain': blockchain.chain, 
        'length': len(blockchain.chain),
        'master_node': my_identity['address']
    }), 200

# --- SYSTEM START ---
if __name__ == '__main__':
    # 1. Netzwerk-Node Start (Mesh-Funktion)
    def start_node_service(node_instance):
        for port in range(5001, 5010):
            try:
                node_instance.port = port
                node_instance.start_server()
                break
            except: continue

    # Starte autonomen Mining-Thread (Der Sklaven-Prozess der Hardware)
    core_thread = threading.Thread(target=autonomous_heartbeat, daemon=True)
    core_thread.start()

    # Starte Netzwerk-Thread
    node_thread = threading.Thread(target=start_node_service, args=(node,), daemon=True)
    node_thread.start()
    
    print(f"[*] PythonChain Dashboard: https://pykiller42.io:5000")
    print(f"[*] Autonomes Mining läuft im Hintergrund...")
    
    # Flask Start mit SSL-Context für verschlüsselte dApp-Kommunikation
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context='adhoc')