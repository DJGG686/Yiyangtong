# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/30 17:55
# @filename: enumeration
# @function: 
# @version : V1

from enum import Enum, IntEnum


class StatusCodeEnum(IntEnum):
    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.description = description
        return obj
    SUCCESS = 2000, 'Success', '请求成功'
    SQL_ERROR = 2001, 'SQL Error', 'SQL错误'
    MISSING_PARAMETER = 2002, 'Missing Parameter', '缺少参数'
    NOT_FOUND = 2003, 'Not Found', '未找到数据'
    UPLOAD_ERROR = 2004, 'Upload Error', '上传文件错误'
    AUTHORIZATION_FAILED = 2005, 'Authorization Failed', '认证失败'
    PARAMETER_NOT_ALLOWED = 2006, 'Parameter Not Allowed', '参数不允许'
    PARAMETER_ERROR = 2007, 'Parameter Error', '参数错误'
    CODE_INVALID = 2008, 'Code Invalid', 'code无效，code2Session请求失败'
    NOT_IMPLEMENTED = 2009, 'Not Implemented', '未实现'


class TableEnum(Enum):
    """
    表名枚举类
    """
    User = 'users'            # 用户表
    Order = 'orders'          # 订单表
    ReservingPerson = 'reserving_persons'
    Institution = 'institutions'
    Favorite = 'favorites'
    BedInfo = 'bed_info'
    ServiceSchedule = 'service_schedules'

    def __str__(self):
        return f'`{self.value}`'


if __name__ == '__main__':
    for item in StatusCodeEnum:
        print(item.value, item.phrase, item.description)
