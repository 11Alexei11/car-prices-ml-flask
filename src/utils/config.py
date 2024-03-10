import os
import yaml
from typing import Dict, Any


class ConfigLoader:
    CONFIG_PATH: str = os.environ.get("CONFIGS_FOLDER_PATH", "./configs/")

    @classmethod
    def load(cls) -> Dict[str, Any]:
        configs = {}
        for config_name in os.listdir(cls.CONFIG_PATH):

            config_name, ext = os.path.splitext(config_name)
            with open(os.path.join(cls.CONFIG_PATH, config_name + ext), 'r') as f:
               configs[config_name] = yaml.safe_load(f)

        return configs