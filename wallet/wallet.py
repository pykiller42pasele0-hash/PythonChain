# -*- coding: utf-8 -*-
import ecdsa
import hashlib
import base58
import binascii
import os

class Wallet:
    def __init__(self):
        self.key_file = 'private.txt'
        self.private_key = self._load_or_generate_key()
        self.public_key = self.private_key.get_verifying_key()
        # Deine Master-Identit�t (Die Adresse)
        self.address = self._generate_btc_style_address()

    def _load_or_generate_key(self):
        """Laedt den Key aus private.txt oder erstellt einen neuen (Deterministisch)"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'r') as f:
                seed = f.read().strip()
                # Erzeugt den Key basierend auf deiner Phrase/Seed
                seed_bytes = hashlib.sha256(seed.encode()).digest()
                return ecdsa.SigningKey.from_string(seed_bytes, curve=ecdsa.SECP256k1)
        else:
            # Falls keine Datei da ist, neue generieren und speichern
            new_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
            with open(self.key_file, 'w') as f:
                f.write(binascii.hexlify(new_key.to_string()).decode())
            return new_key

    def _generate_btc_style_address(self):
        """Erzeugt eine echte Double-Hash Adresse (BTC-kompatibel)"""
        public_key_bytes = self.public_key.to_string(encoding="compressed")
        
        # 1. SHA-256 auf den Public Key
        sha256_bpk = hashlib.sha256(public_key_bytes).digest()
        
        # 2. RIPEMD-160 auf das Resultat (Double Hashing)
        ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
        
        # 3. Network Byte hinzufuegen (0x00 fuer Mainnet-Stil)
        network_byte = b'\x00' + ripemd160_bpk
        
        # 4. Checksum berechnen (Doppel SHA-256)
        checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
        
        # 5. Base58 Encoding fuer die finale Adresse
        binary_address = network_byte + checksum
        return base58.b58encode(binary_address).decode('utf-8')

    def sign_transaction(self, message):
        """Signiert Daten mit deinem Private Key"""
        signature = self.private_key.sign(message.encode())
        return binascii.hexlify(signature).decode()

    @staticmethod
    def verify_signature(public_key_hex, signature_hex, message):
        """Validiert Signaturen im Netzwerk"""
        try:
            public_key = ecdsa.VerifyingKey.from_string(binascii.unhexlify(public_key_hex), curve=ecdsa.SECP256k1)
            signature = binascii.unhexlify(signature_hex)
            return public_key.verify(signature, message.encode())
        except:
            return False

    def get_identity(self):
        """Gibt die Domain-Info zurueck"""
        return {
            "address": self.address,
            "domain": f"PythonChain@pykiller42-{self.address[:8]}"
        }

