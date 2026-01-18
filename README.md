# ⛓️ PythonChain | Sovereign OS & Full-Node
**Identity:** `1LH6W1qEzcK3sMSjieS5XaHMejYfMc3vGf`
**Domain:** `pykiller42.io` (Managed by Sovereign DNS Logic)
**Protocol:** `.pio` (PythonChain Input/Output)

## 🚀 Vision: Devs for Devs
PythonChain ist eine unabhängige Infrastruktur. Entwickler bauen hier eigene Ökosysteme, verdienen durch dApps und betreiben das Netzwerk selbst – ohne Cloud-Anbieter oder Konzerne. Durch das integrierte **PCCMD Terminal** wird Code direkt zum Gesetz der Chain.

## 🏗 Fullstack Architektur
Das System ist als vertikaler Stack aufgebaut, um maximale Unabhängigkeit von externen Schnittstellen zu garantieren:

- **BACKEND (Kernel):** Flask-Server (`app.py`) steuert den Zugriff auf den `core/`.
- **FRONTEND (Dashboard):** HTML/JS Interface zur Visualisierung des Mesh-Netzwerks.
- **PCCMD (.pio):** Das integrierte Terminal ermöglicht Live-Coding. Dateien mit der Endung `.pio` werden vom System als ausführbare Blockchain-Befehle interpretiert.
- **MESH-NET:** Autonome Port-Wahl (5001-5010) sorgt für Erreichbarkeit auch hinter Firewalls.

## 📁 Projekt-Struktur
- `core/`: Das mathematische Rückgrat (Mining & Validierung).
- `backend/`: API-Extensions (`api_extension.py`) & C++ Performance-Bridges.
- `frontend/`: Client-side Security (`logic.js`) & UI-Assets.
- `wallet/`: Kryptographische Identitätsverwaltung.
- `network/`: P2P-Socket-Logik für den globalen Sync.

## 🛠️ Installation & Setup
1. **Sovereign Host-Link:** Füge die `pykiller42.io` Einträge zu deiner Windows `hosts`-Datei hinzu (siehe Dokumentation).
2. **Abhängigkeiten:**
   ```bash
   pip install -r requirements.txt