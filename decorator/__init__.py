# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/30 17:20
# @filename: __init__.py
# @function: 
# @version : V1

from functools import wraps

from flask import jsonify


def api_response(func):
    @wraps(wrapped=func)
    def wrapper(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return wrapper
