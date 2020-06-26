from __future__ import annotations
import configparser
import os
from dataclasses import dataclass
from typing import Optional, List

CONFIG_FILE_NAME = ".bbtronic"


def load_config() -> Optional[Config]:
    config_path = _find_config()
    if config_path is not None:
        config = configparser.ConfigParser()
        config.read(config_path)
        return Config(
            servers=[ConfigServer(
                alias=server_alias,
                base_uri=config[server_alias]["base_uri"],
                access_token=config[server_alias]["access_token"]
            ) for server_alias in config.sections()]
        )
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


@dataclass
class Config:
    servers: List[ConfigServer]

    def find_server(self, alias: str) -> ConfigServer:
        for server in self.servers:
            if server.alias == alias:
                return server
        raise Exception(f"Server with alias \"{alias}\" is not configured")


@dataclass
class ConfigServer:
    alias: str
    base_uri: str
    access_token: str
