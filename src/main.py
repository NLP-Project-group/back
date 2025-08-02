import sys
import os

# Ajouter le dossier 'translation' au path Python
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "translation"))
if module_path not in sys.path:
    sys.path.insert(0, module_path)

from traduction import main

if __name__ == "__main__":
    print("🟢 Lancement du programme de traduction...")
    main()
