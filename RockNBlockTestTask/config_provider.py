import os
from pathlib import Path

import yaml


class ConfigProvider:

    def __init__(self, base_dir: Path, path_to_config: str):
        self.config_path = path_to_config
        self.base_dir = base_dir

    def get_config(self):
        path = os.path.join(self.base_dir, self.config_path)
        with open(path, 'r') as conf:
            data = yaml.safe_load(conf)
            return data