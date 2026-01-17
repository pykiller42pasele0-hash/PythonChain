import socket
import threading
import time

# Ein einfacher Node, der senden und empfangen kann
class PythonChainNode:
    def __init__(self, my_port, peer_port=None):
        self.host = '127.0.0.1' # Lokal auf deinem Laptop
        self.port = my_port
        self.peer_port = peer_port
        
    def start_server(self):
        # Der Node "hört" zu, ob andere ihm neue Blöcke schicken
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[*] Node läuft auf Port {self.port} und wartet auf Daten...")

        while True:
            conn, addr = server.accept()
            data = conn.recv(1024).decode()
            print(f"\n[EMPFANGEN] Neuer Block-Inhalt von {addr}: {data}")
            conn.close()

    def send_data(self, message):
        # Der Node schickt Daten an einen anderen Node
        if self.peer_port:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.host, self.peer_port))
                client.send(message.encode())
                client.close()
                print(f"[GESENDET] Block an Port {self.peer_port} übertragen.")
            except ConnectionRefusedError:
                print("[FEHLER] Der andere Node ist noch nicht online!")

# Simulation starten
if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) # Port beim Start angeben
    peer = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    node = PythonChainNode(port, peer)
    
    # Server in einem eigenen Thread starten, damit wir gleichzeitig tippen können
    threading.Thread(target=node.start_server, daemon=True).start()
    
    time.sleep(1)
    if peer:
        while True:
            msg = input("Gib eine Transaktion ein (oder 'exit'): ")
            if msg == 'exit': break
            node.send_data(msg)