# -*- coding: utf-8 -*-
import sys
import io

class PCCMDKernel:
    """Die Logik-Einheit f�r das Terminal im Dashboard"""
    
    def __init__(self, blockchain_ref):
        self.blockchain = blockchain_ref
        # Lokale Umgebung f�r das Terminal (Variablen-Speicher)
        self.locals = {"blockchain": self.blockchain, "status": "Ready"}

    def execute_command(self, code):
        """F�hrt Python-Code aus und f�ngt die Ausgabe (stdout) ab"""
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        
        try:
            # F�hrt den Code in der gesch�tzten Umgebung aus
            exec(code, {}, self.locals)
            result = output_buffer.getvalue()
            sys.stdout = sys.__stdout__
            return result if result else "Befehl ausgef�hrt (keine R�ckgabe)."
        except Exception as e:
            sys.stdout = sys.__stdout__
            return f"FEHLER: {str(e)}"

# Diese Erweiterung wird von app.py importiert
def get_terminal_response(command, blockchain):
    kernel = PCCMDKernel(blockchain)
    return kernel.execute_command(command)
