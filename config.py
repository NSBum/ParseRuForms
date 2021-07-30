import yaml
from typing import Dict

dbconfig = None


def load_config() -> Dict:
    with open('config.yml', 'r') as fh:
        cfg = yaml.safe_load(fh)
        return cfg


