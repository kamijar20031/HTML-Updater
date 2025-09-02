import json, shutil, os

PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR =  os.path.dirname(PYTHON_DIR)
TEMPLATE_DIR = os.path.join(MAIN_DIR, "template")
OUTPUT_DIR = os.path.join(MAIN_DIR, "output")

SETTINGS_FILE = "loadedSettings.json"
MEM_FILE = "currentState.json"
CONFIG = "config.json"
MEM_CONFIG = "currentConfig.json"