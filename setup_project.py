import os

# Definition der Pfadstruktur
project_name = "PythonChain"
folders = [
    "core",
    "network",
    "wallet",
    "frontend",
    "docs"
]

files = {
    "README.md": """# ⛓️ PythonChain
**Die erste echte dezentrale Python-Blockchain fuer Entwickler.**

## 🚀 Vision: Devs for Devs
PythonChain ist eine unabhaengige Infrastruktur. Entwickler bauen hier eigene oekosysteme, verdienen durch dApps und betreiben das Netzwerk selbst – ohne Cloud-Anbieter oder Konzerne.

## 📁 Struktur
- `core/`: Blockchain-Logik & Mining
- `wallet/`: Private/Public Keys & Signaturen
- `network/`: P2P-Kommunikation (Sockets)
- `frontend/`: Dashboard (HTML/JS)

## 🛠️ Installation
1. `pip install ecdsa flask`
2. `python core/blockchain.py`
""",
    "GOVERNANCE.md": "# Governance Modell\\n- Dezentrale Mitbestimmung.\\n- Profit durch Code-Beitraege.\\n- Keine zentrale Instanz.",
    "requirements.txt": "ecdsa\\nflask\\nrequests",
    "wallet/wallet.py": "# Wallet Logik hier einfuegen",
    "core/blockchain.py": "# Blockchain Core hier einfuegen",
    "network/node.py": "# P2P Socket Logik hier einfuegen",
    "frontend/index.html": ""
}

def create_structure():
    # Hauptordner erstellen
    if not os.path.exists(project_name):
        os.makedirs(project_name)
    
    os.chdir(project_name)
    
    # Unterordner erstellen
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            with open(os.path.join(folder, "__init__.py"), "w") as f:
                f.write("") # Macht es zu einem Python-Paket

    # Dateien erstellen
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
    print(f"✅ PythonChain Struktur wurde erfolgreich in '{os.getcwd()}' erstellt!")

if __name__ == "__main__":
    create_structure()

