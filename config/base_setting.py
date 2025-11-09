# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 13:35
# @filename: base_setting
# @function: 
# @version : V1
import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Yiyangtong-Backend'
    # 数据库配置
    SQLALCHEMY_DATABASE_SETTING = {
        'user': 'root',
        'password': 'dj124342',
        'host': 'localhost',
        'database': 'college'
    }

    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'Yiyangtong'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # 日志配置
    LOGGING_PATH = './logs'
    LOGGING_CONFIG_PATH = './yaml_files/logging.yaml'
