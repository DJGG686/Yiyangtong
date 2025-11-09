# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/30 17:53
# @filename: response
# @function: API响应类
# @version : V1
from utils import StatusCode
from flask import jsonify


class ApiResponse:
    def __init__(self, code=StatusCode.SUCCESS, data=None):
        self.code = code.value
        self.message = code.phrase
        if data is not None:
            self.data = data

    def update(self, code=None, data=None, msg=None):
        if code is not None:
            self.code = code.value
            self.message = code.phrase
        if data is not None:
            self.data = data
        if msg is not None:
            self.message = msg

    @property
    def info(self):
        return self.__dict__


if __name__ == '__main__':
    response = ApiResponse()
    response.update(data={'name': 'digjie'})
    print(response.info)
