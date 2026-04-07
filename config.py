import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "hotkey": "f8",
    "mic_index": None,
    "model_size": "base",
    "max_listen_time": 6,
    "auto_play": True,
    "start_with_windows": False,
    "background_image": None
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                # Merge with default to ensure all keys exists
                for k, v in DEFAULT_CONFIG.items():
                    if k not in config:
                        config[k] = v
                return config
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
