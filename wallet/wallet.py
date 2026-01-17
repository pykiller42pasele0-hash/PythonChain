# file: wallet.py
import ecdsa
import binascii

class Wallet:
    def __init__(self):
        # Erzeugt einen geheimen Schlüssel (Private Key)
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        # Leitet den öffentlichen Schlüssel ab (Public Key)
        self.public_key = self.private_key.get_verifying_key()

    def get_address(self):
        # Deine Wallet-Adresse als lesbarer String
        return binascii.hexlify(self.public_key.to_string()).decode()

    def sign_transaction(self, message):
        # Unterschreibt eine Nachricht (z.B. "Sende 10 Coins")
        signature = self.private_key.sign(message.encode())
        return binascii.hexlify(signature).decode()

    @staticmethod
    def verify_signature(public_key_hex, signature_hex, message):
        # Prüft, ob die Unterschrift zum Public Key passt
        public_key = ecdsa.VerifyingKey.from_string(binascii.unhexlify(public_key_hex), curve=ecdsa.SECP256k1)
        signature = binascii.unhexlify(signature_hex)
        try:
            return public_key.verify(signature, message.encode())
        except:
            return False