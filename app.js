const API_URL = "http://localhost:5000";

async function interactWithBlockchain(endpoint, data = null) {
    try {
        const options = data ? {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        } : { method: 'GET' };

        const response = await fetch(`${API_URL}${endpoint}`, options);
        
        if (!response.ok) throw new Error("Server Fehler");

        const result = await response.json();
        return result;

    } catch (error) {
        // Hier passiert die Magie: Fehlermeldung für den User
        console.error("Verbindung fehlgeschlagen:", error);
        alert("⚠️ PythonChain-Warnung: Deine lokale Node (CMD) ist nicht erreichbar! Bitte starte die .bat Datei.");
        return null;
    }
}

// Beispiel: Den Button-Klick absichern
async function getChain() {
    const chain = await interactWithBlockchain('/chain');
    if (chain) {
        console.log("Blockchain Daten:", chain);
        // Hier die Chain im HTML anzeigen
    }
}