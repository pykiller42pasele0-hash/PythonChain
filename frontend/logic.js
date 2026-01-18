// PythonChain Frontend Logic - Sovereign Security
const wordList = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "omega", "python", "node", "crypt", "mesh", "flux", "energy", "solar", "prime", "matrix"];

/**
 * Generiert eine zufällige 12-Wörter Seed-Phrase für neue Accounts
 */
function generateSeedPhrase() {
    let phrase = [];
    for (let i = 0; i < 12; i++) {
        const randomIndex = Math.floor(Math.random() * wordList.length);
        phrase.push(wordList[randomIndex]);
    }
    return phrase.join(" ");
}

/**
 * Führt den Python-Code aus dem PCCMD Terminal über das Backend aus
 */
async function executePython(code) {
    const terminal = document.getElementById('terminal');
    
    try {
        const response = await fetch('/api/terminal/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: code })
        });
        
        const data = await response.json();
        
        // Ergebnis im Terminal anzeigen
        const resultDiv = document.createElement('div');
        resultDiv.style.color = "#00ff41";
        resultDiv.innerText = `[RESULT] ${data.output}`;
        terminal.appendChild(resultDiv);
    } catch (error) {
        const errDiv = document.createElement('div');
        errDiv.style.color = "#ff3e3e";
        errDiv.innerText = `[FEHLER] Verbindung zum Kernel unterbrochen.`;
        terminal.appendChild(errDiv);
    }
    terminal.scrollTop = terminal.scrollHeight;
}

// Initialisierung beim Laden der Seite
window.onload = () => {
    console.log("PythonChain Frontend-Logic geladen.");
    if (!localStorage.getItem('seed_phrase')) {
        const newPhrase = generateSeedPhrase();
        localStorage.setItem('seed_phrase', newPhrase);
        console.log("Neue Seed-Phrase generiert und lokal gesichert.");
    }
};