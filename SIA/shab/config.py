# config.py
import os
from configparser import ConfigParser


def read_config(file_path):
    """
    Read configuration from the specified file.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        ConfigParser: The configuration parser object.
    """
    config = ConfigParser()
    config.read(file_path)
    return config
