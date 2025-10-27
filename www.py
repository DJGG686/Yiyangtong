# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 13:34
# @filename: www
# @function: 
# @version : V1
# @description : 注册蓝图，管理路由

from app import app
from controller import InstitutionController
from controller import ScheduleController
from controller import UserController

controllers = [
    UserController(),
    InstitutionController(),
    ScheduleController(),
]

for controller in controllers:
    controller.register(app)



