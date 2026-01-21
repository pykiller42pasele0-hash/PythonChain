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

# Terminal Extension (PCCMD Logic)
try:
    from backend.api_extension import get_terminal_response
except ImportError:
    def get_terminal_response(cmd, bc): return "Backend Extension not found."

# UTF-8 Fix for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- FLASK & SOVEREIGN CONFIG ---
app = Flask(__name__, template_folder='.', static_folder='frontend')
CORS(app)

# 1. Identity & Blockchain Initialization
my_wallet = Wallet()
my_identity = my_wallet.get_identity()
blockchain = PythonChain(node_wallet_address=my_identity['address'])
miner = MiningEngine(blockchain)
node = PythonChainNode(host='0.0.0.0', port=5001, wallet_address=my_identity['address'])

# --- AUTONOMOUS MATHEMATICAL CORE (DAEMON) ---
def autonomous_heartbeat():
    """Autonomous process: Mines blocks deterministically in background"""
    print(f"[*] WWPC Autonomous Core active. Master: {my_identity['address']}")
    while True:
        try:
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
                print(f"[MATH] Autonomous Block {block['index']} sealed (Resonance 0ms)")
        except Exception as e:
            print(f"[!] Core Heartbeat Error: {e}")
        
        time.sleep(1)

# --- MIDDLEWARE: HTTPS ENFORCEMENT ---
@app.before_request
def enforce_sovereign_protocol():
    # Force redirect to HTTPS if not local
    if not request.is_secure and 'localhost' not in request.host and '127.0.0.1' not in request.host:
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

@app.after_request
def apply_security_headers(response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-World-Wide-PythonChain"] = "Sovereign-Node-v1.0"
    return response

# --- API ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mine', methods=['GET'])
def manual_mine():
    last_block = blockchain.last_block
    proof = miner.proof_of_work(last_block)
    if proof:
        blockchain.new_transaction(sender="0", recipient=my_identity['address'], amount=miner.calculate_coin_value())
        block = blockchain.new_block(proof)
        return jsonify({'status': 'success', 'block': block}), 200
    return jsonify({'status': 'error', 'message': 'Mining aborted'}), 400

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
    def start_node_service(node_instance):
        for port in range(5001, 5010):
            try:
                node_instance.port = port
                node_instance.start_server()
                break
            except: continue

    core_thread = threading.Thread(target=autonomous_heartbeat, daemon=True)
    core_thread.start()

    node_thread = threading.Thread(target=start_node_service, args=(node,), daemon=True)
    node_thread.start()
    
    print(f"[*] PythonChain Dashboard: https://pykiller42.io:5000")
    print(f"[*] Autonomous Mining running in background...")
    
    # KORREKTUR: Muss eingerückt sein und nutzt 0.0.0.0 für stabilere IPv4 Bindung
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context='adhoc')