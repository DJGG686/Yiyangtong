# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/26 16:48
# @filename: base_controller
# @function: 
# @version : V1
from flask import Blueprint


class Controller:
    PREFIX = None

    def __init__(self):
        self.blueprint = Blueprint(self.PREFIX, __name__)

    def register(self, app):
        app.register_blueprint(self.blueprint, url_prefix=f'/{self.PREFIX}')
