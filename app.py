# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 13:34
# @filename: www
# @function:
# @version : V1
# @description : 初始化Flask应用，完成基本配置
import os
from flask import Flask, request, jsonify, abort, Response, render_template
from config import DevelopConfig
from utils import LogTool


def create_app():
    _app = Flask(__name__)

    _app.config.from_object(DevelopConfig)

    if not os.path.exists(_app.config['LOGGING_PATH']):
        os.mkdir(_app.config['LOGGING_PATH'])

    log_tool = LogTool(_app.config['LOGGING_CONFIG_PATH'])

    logger = log_tool.get_logger("debug_handler")
    return _app


app = create_app()


@app.route('/')
def main_page():  # put application's code here
    return jsonify({
        'message': '颐养通后端接口',
        'status': 'running'
    })


@app.route('/abort')
def abort_function():
    abort(406)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        'code': 404,
        'message': '接口不存在'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'code': 500,
        'message': '服务器内部错误'
    }), 500


if __name__ == '__main__':
    app.run()
