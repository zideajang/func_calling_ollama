from typing import Dict
from function_calling_ollama.utils import printd

def get_completions_settings(defaults="simple") -> Dict:
    printd(f"Loading default settings from '{defaults}'")