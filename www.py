# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 13:34
# @filename: www
# @function: 
# @version : V1
# @description : 注册蓝图，管理路由

from app import app
from controller.institution_controller import InstitutionController
from controller.schedule_controller import ScheduleController
from controller.user_controller import UserController

app.register_blueprint(UserController().blueprint, url_prefix=f'/{UserController.PREFIX}')
app.register_blueprint(InstitutionController().blueprint, url_prefix=f'/{InstitutionController.PREFIX}')
app.register_blueprint(ScheduleController().blueprint, url_prefix=f'/{ScheduleController.PREFIX}')



