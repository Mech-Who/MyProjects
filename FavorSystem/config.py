from typing import Dict

import yaml

def ReadConfig(filename: str="config.yaml") -> Dict:
    with open(filename, 'r') as f:
        config = yaml.safe_load(f)
    return config

def EditConfig(new_config: Dict, filename: str="config.yaml"):
    with open(filename, 'w') as f:
        yaml.safe_dump(new_config, f)

