# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 00:04
# @filename: test
# @function: 
# @version : V1

from sqlalchemy import create_engine, text


engine = create_engine('mysql+pymysql://root:dj124342@localhost/college')

with engine.connect() as conn:
    result = conn.execute(text('SELECT * FROM classroom'))
    for row in result:
        print(row)

engine.dispose()
