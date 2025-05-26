import os
import yaml
import re

def expand_env_vars(s):
    if not isinstance(s, str): return s
    return re.sub(r"\$\{([^}^{]+)\}", lambda m: os.environ.get(m.group(1), ""), s)

def load_config(path):
    with open(path) as f:
        data = yaml.safe_load(f)
        for src in data.get("sources", []):
            if "token" in src:
                src["token"] = expand_env_vars(src["token"])
        data["backup_dir"] = os.path.expanduser(data["backup_dir"])
        return data