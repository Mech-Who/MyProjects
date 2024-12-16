from typing import Dict

import yaml

def ReadConfig(filename: str="config.yaml") -> Dict:
    with open(filename, 'r') as f:
        config = yaml.safe_laod(f)
    return config
