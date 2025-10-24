# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/14 23:47
# @filename: mysql_test
# @function: 
# @version : V1

from mysql_connector import MySQLConnector


def main():
    db_info = {
        'user': 'root',
        'password': 'dj124342',
        'host': 'localhost',
        'database': 'college'
    }
    connector = MySQLConnector(**db_info)

    # 执行查询
    query = "SELECT * FROM classroom"
    result = connector.execute(query)
    for row in result:
        print(row)


if __name__ == '__main__':
    main()
