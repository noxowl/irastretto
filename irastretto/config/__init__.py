""":mod:'irastretto.config'

"""
import yaml
import pathlib


class ConfigDict(dict):
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            raise ConfigKeyError(key)


class ConfigKeyError(KeyError):
    def __str__(selfj):
        return 'missing configuration: ' + super().__str__()


def read_config(filename):
    pass


def read_config_from_yaml():
    pass
