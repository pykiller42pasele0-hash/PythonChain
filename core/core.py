# -*- coding: utf-8 -*-
import hashlib
import json
import time

class MiningEngine:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.is_mining = False

    def proof_of_work(self, last_block):
        """
        Der energetische Algorithmus:
        Findet eine Zahl p', so dass hash(pp') mit 4 Nullen beginnt.
        p ist der vorherige Proof, p' ist der neue Proof.
        """
        last_proof = last_block['proof']
        last_hash = self.blockchain.hash(last_block)
        
        proof = 0
        self.is_mining = True
        start_time = time.time()
        hashes_tried = 0

        print(f"[*] Mining gestartet... Difficulty: {self.blockchain.difficulty}")

        while self.valid_proof(last_proof, proof, last_hash) is False:
            if not self.is_mining: # Abbruch falls Node stoppt
                return None
            proof += 1
            hashes_tried += 1
            
            # Alle 100.000 Versuche kurz die Leistung berechnen
            if hashes_tried % 100000 == 0:
                elapsed = time.time() - start_time
                hashrate = hashes_tried / elapsed
                print(f"[STATUS] Energie-Output: {hashrate:.2f} Hashes/s")

        total_time = time.time() - start_time
        print(f"[ERFOLG] Block gefunden in {total_time:.2f} Sekunden!")
        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """Prueft die energetische Korrektheit des Hashes"""
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # Die Difficulty bestimmt, wie viele Nullen am Anfang stehen muessen
        return guess_hash[:4] == "0000"

    def calculate_coin_value(self):
        """
        Deterministische Wertermittlung:
        Der Wert basiert auf der Difficulty (Potenz) und der Netz-Hashrate.
        """
        base_value = 0.0001
        difficulty_multiplier = 2 ** self.blockchain.difficulty
        # Je schwerer das Raetsel, desto hoeher der energetische Wert
        return base_value * difficulty_multiplier
