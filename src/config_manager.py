import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "image_folder": "",
    "slide_interval": 5,  # giây
    "transition_effect": "Fade",
    "auto_start": False,
    "dark_mode": True,
    "shuffle": False
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Merge với mặc định để tránh thiếu key
            for k, v in DEFAULT_CONFIG.items():
                data.setdefault(k, v)
            return data
    except Exception:
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)