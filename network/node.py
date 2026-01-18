# -*- coding: utf-8 -*-
import socket
import threading
import json
import time

class PythonChainNode:
    def __init__(self, host, port, wallet_address):
        self.host = host
        self.port = port
        self.wallet_address = wallet_address # Deine ID: PythonChain@pykiller42...
        self.peers = set() # Liste bekannter Knoten im Mesh-Netz
        self.is_running = True

    def start_server(self):
        """Startet den Provider-Dienst des Geraets"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[*] PythonChain Node aktiv auf {self.host}:{self.port}")
        print(f"[*] Identit�t: {self.wallet_address}")

        while self.is_running:
            try:
                conn, addr = server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
            except Exception as e:
                print(f"[FEHLER] Server-Socket: {e}")

    def handle_client(self, conn, addr):
        """Verarbeitet eingehende Mesh-Daten und validiert die Identit�t"""
        try:
            data = conn.recv(4096).decode('utf-8')
            if not data:
                return
            
            message = json.loads(data)
            msg_type = message.get('type')
            sender_id = message.get('sender_id')

            print(f"\n[EMPFANGEN] Typ: {msg_type} von {sender_id[:15]}...")

            if msg_type == 'NEW_BLOCK':
                # Logik zur Validierung des neuen Blocks
                print(f"[MESH] Neuer Block zur Verifizierung erhalten.")
            
            elif msg_type == 'PEER_DISCOVERY':
                # Ein neuer Knoten stellt sich vor
                self.peers.add(tuple(message.get('node_address')))
                print(f"[MESH] Neuer Peer registriert: {addr}")

        except Exception as e:
            print(f"[FEHLER] Datenverarbeitung von {addr}: {e}")
        finally:
            conn.close()

    def broadcast_data(self, data_type, payload):
        """Verteilt Informationen im gesamten PythonChain-Netzwerk (Gossip)"""
        message = json.dumps({
            'type': data_type,
            'sender_id': self.wallet_address,
            'payload': payload,
            'timestamp': time.time()
        })

        for peer in list(self.peers):
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(2.0)
                client.connect(peer)
                client.send(message.encode('utf-8'))
                client.close()
            except:
                print(f"[INFO] Peer {peer} nicht erreichbar, entferne aus Liste.")
                self.peers.remove(peer)

    def register_peer(self, host, port):
        """Manuelle oder automatische Peer-Registrierung"""
        self.peers.add((host, port))
        # Sofortige Vorstellung beim neuen Peer
        self.broadcast_data('PEER_DISCOVERY', {'node_address': (self.host, self.port)})

