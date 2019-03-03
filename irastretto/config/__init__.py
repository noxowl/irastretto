""":mod:'irastretto.config'

"""
import os
import yaml
import pathlib

VERSION = '0.1'


class ConfigDict(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            raise ConfigKeyError(key)


class ConfigKeyError(KeyError):
    def __str__(selfj):
        return 'missing configuration: ' + super().__str__()


def read_config(config_path):
    try:
        return read_config_from_yaml(config_path)
    except Exception:
        raise RuntimeError


def read_config_from_yaml(config_path):
    with (config_path).open('r') as conf:
        config_dict = yaml.load(conf)
        config_dict['version'] = VERSION
    return ConfigDict((k.upper(), v) for k, v in config_dict.items())


def read_irastretto_config():
    current_dir = os.path.dirname(__file__)
    return read_config(pathlib.Path(current_dir, 'config.yaml'))
