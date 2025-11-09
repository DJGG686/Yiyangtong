# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/25 13:50
# @filename: log_tool
# @function: 
# @version : V1
import logging
import os
from logging import config
import yaml


class LogTool:
    def __init__(self, yaml_path=f".\yaml_files\logging.yaml", default_level=logging.INFO):
        path = yaml_path
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                config_dict = yaml.safe_load(f.read())
            logging.config.dictConfig(config_dict)
        else:
            logging.basicConfig(level=default_level)

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)
