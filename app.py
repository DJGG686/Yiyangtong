# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 13:34
# @filename: www
# @function:
# @version : V1
# @description : 初始化Flask应用，完成基本配置
from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('config/base_setting.py')


@app.route('/')
def main_page():  # put application's code here
    return '颐养通后端接口'


if __name__ == '__main__':
    app.run()
