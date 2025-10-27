# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 15:56
# @filename: user_controller
# @function: 
# @version : V1

from flask import Blueprint, Response
from .base_controller import Controller
from service.user_service import UserService


class UserController(Controller):
    PREFIX = 'user'

    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        self.blueprint = Blueprint('user_api', __name__)
        self.bind_view_func()

    def bind_view_func(self):
        self.blueprint.add_url_rule('/login', view_func=self.login, methods=['POST'])
        self.blueprint.add_url_rule('/information', view_func=self.get_reserver_info, methods=['GET'])
        self.blueprint.add_url_rule('/information', view_func=self.add_reserver_info, methods=['POST'])
        self.blueprint.add_url_rule('/information', view_func=self.update_reserver_info, methods=['PUT'])
        self.blueprint.add_url_rule('/order', view_func=self.get_user_order, methods=['GET'])
        self.blueprint.add_url_rule('/favorite', view_func=self.get_user_favorate, methods=['GET'])

    def login(self):
        return Response('login', 200)

    def get_reserver_info(self):
        return Response('user info', 200)

    def add_reserver_info(self):
        return Response('add user info', 200)

    def update_reserver_info(self):
        return Response('update user info', 200)

    def get_user_order(self):
        return Response('user order', 200)

    def get_user_favorate(self):
        return Response('user favorate', 200)


if __name__ == '__main__':
    user_controller = UserController()
    print(user_controller.login())

