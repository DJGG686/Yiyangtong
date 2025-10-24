# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 13:34
# @filename: main
# @function: 
# @version : V1
# @description : 启动后端服务
from www import *


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()

