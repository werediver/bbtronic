import configparser
import os
from typing import Optional

CONFIG_FILE_NAME = ".bbtronic"


def load_config() -> Optional[configparser.ConfigParser]:
    config_path = _find_config()
    if config_path is not None:
        config = configparser.ConfigParser()
        config.read(config_path)
        return config
    else:
        return None


def _find_config(d: str = os.getcwd()) -> Optional[str]:
    config_path = os.path.join(d, CONFIG_FILE_NAME)
    if os.path.isfile(config_path):
        return config_path
    else:
        parent_dir = os.path.dirname(d)
        if parent_dir != d:
            return _find_config(parent_dir)
        else:
            return None
