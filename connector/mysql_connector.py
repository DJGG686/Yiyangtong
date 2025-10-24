# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/13 23:23
# @filename: mysql_connector
# @function: 
# @version : V1
from sqlalchemy import create_engine, text, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class MySQLConnector:
    # 数据库连接器单例模式
    __connector = None

    def __new__(cls, *args, **kwargs):
        if not cls.__connector:
            cls.__connector = super(MySQLConnector, cls).__new__(cls)
        return cls.__connector

    def __init__(self, user, password, host, database):
        try:
            url = f'mysql+pymysql://{user}:{password}@{host}/{database}'
            self.__engine = create_engine(url, echo=True)
            self.Session = sessionmaker(bind=self.__engine)
        except exc.SQLAlchemyError as e:
            print(f"Error connecting to MySQL: {e}")

    def __del__(self):
        # 关闭引擎
        self.__engine.dispose()

    def execute(self, sql):
        with self.__engine.begin() as conn:
            result = conn.execute(text(sql))
            return result.fetchall()


