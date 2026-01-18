# -*- coding: utf-8 -*-
// Konfiguration der dApp Domain
const API_URL = "http://localhost:5000";
let isMining = false;

/**
 * Kern-Funktion fuer die Kommunikation mit der PythonChain-Hardware
 */
async function callNode(endpoint, data = null) {
    try {
        const options = data ? {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        } : { method: 'GET' };

        const response = await fetch(`${API_URL}${endpoint}`, options);
        if (!response.ok) throw new Error("Hardware antwortet nicht korrekt");
        return await response.json();
    } catch (error) {
        console.error("Node-Verbindung unterbrochen:", error);
        updateStatus("OFFLINE");
        return null;
    }
}

/**
 * Laedt deine Master-Domain und Wallet-ID beim Start
 */
async function loadIdentity() {
    const info = await callNode('/wallet/info');
    if (info) {
        document.getElementById('wallet-address').innerText = info.address;
        document.getElementById('domain-name').innerText = info.domain;
        console.log("Master-Identität geladen:", info.domain);
    }
}

/**
 * Startet den energetischen Mining-Prozess und visualisiert die Probabilistik
 */
async function startMining() {
    if (isMining) return;
    isMining = true;
    updateStatus("MINING...");
    
    // UI-Vorschau auf die Wahrscheinlichkeit (Simulierte Probabilistik)
    const miningInterval = setInterval(() => {
        if (!isMining) clearInterval(miningInterval);
        const hashPower = (Math.random() * 500 + 100).toFixed(2);
        document.getElementById('hashrate-display').innerText = `${hashPower} H/s`;
    }, 500);

    const result = await callNode('/mine');
    
    isMining = false;
    clearInterval(miningInterval);
    
    if (result) {
        alert(`Erfolg! Block #${result.index} gemined.\nEnergie-Wert: ${result.energy_value.toFixed(8)} PC-Coins`);
        refreshUI();
    }
    updateStatus("ONLINE");
}

/**
 * Aktualisiert die gesamte Ansicht (Kette und Kontostand)
 */
async function refreshUI() {
    const data = await callNode('/chain');
    if (data) {
        const chainList = document.getElementById('chain-display');
        chainList.innerHTML = ''; // Liste leeren
        
        data.chain.forEach(block => {
            const blockEl = document.createElement('div');
            blockEl.className = 'block-card';
            blockEl.innerHTML = `
                <strong>Block #${block.index}</strong><br>
                Hash: <small>${block.previous_hash.substring(0, 20)}...</small><br>
                Energie: ${block.proof} (Diff: ${data.difficulty})
            `;
            chainList.appendChild(blockEl);
        });
        
        document.getElementById('block-count').innerText = data.length;
    }
}

function updateStatus(status) {
    const statusEl = document.getElementById('node-status');
    statusEl.innerText = status;
    statusEl.className = status.toLowerCase();
}

// Initialisierung beim Laden der Seite
window.onload = () => {
    loadIdentity();
    refreshUI();
    // Alle 10 Sekunden automatisch synchronisieren
    setInterval(refreshUI, 10000);
};