import yaml, pathlib, os

def load_settings(path='configs/settings.yml'):
    p = pathlib.Path(path)
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text())

def load_whitelist(path='configs/whitelist.yml'):
    p = pathlib.Path(path)
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text())
