import os, yaml

def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path
