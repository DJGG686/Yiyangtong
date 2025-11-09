# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 13:36
# @filename: develop_setting
# @function:
# @version : V1
import os
from . import Config


# 开发环境配置
class DevelopConfig(Config):
    pass

    # 微信小程序配置
    WECHAT_APPID = os.environ.get('WECHAT_APPID') or 'wxb264754c2abacc99'
    WECHAT_SECRET = os.environ.get('WECHAT_SECRET') or '2e6209d0139be8b5a4902912f2ce7025'
