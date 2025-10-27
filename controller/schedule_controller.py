# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 16:04
# @filename: schedule_controller
# @function: 
# @version : V1

from flask import Blueprint, Response
from .base_controller import Controller
from service.schedule_service import ScheduleService


class ScheduleController(Controller):
    PREFIX = 'schedule'

    def __init__(self):
        super().__init__()
        self.schedule_service = ScheduleService()
        self.blueprint = Blueprint('schedule_api', __name__)
        self.bind_view_func()

    def bind_view_func(self):
        self.blueprint.add_url_rule('', view_func=self.get_schedule_list, methods=['GET'])

    def get_schedule_list(self):
        return Response('schedule list', 200)
