from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """用户表"""
    __tablename__ = 'users'
    
    user_id = db.Column(db.String(64), primary_key=True, comment='用户ID')
    openid = db.Column(db.String(64), unique=True, nullable=False, comment='微信openid')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    
    # 关系
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic')
    reserving_persons = db.relationship('ReservingPerson', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.user_id}>'


class Institution(db.Model):
    """养老机构表"""
    __tablename__ = 'institutions'
    
    institution_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='机构ID')
    name = db.Column(db.String(100), nullable=False, comment='机构名称')
    score = db.Column(db.Float, default=0.0, comment='评分')
    address = db.Column(db.String(200), nullable=False, comment='地址')
    phone = db.Column(db.String(20), comment='联系电话')
    cover = db.Column(db.String(200), comment='封面图片URL')
    district = db.Column(db.String(50), comment='所在区域')
    # 机构服务类型，支持多种类型（位运算）：1-到点服务, 2-居家上门, 4-床位预约
    service_types = db.Column(db.Integer, default=0, comment='服务类型（位掩码）')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    
    # 关系
    orders = db.relationship('Order', backref='institution', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='institution', lazy='dynamic')
    bed_info = db.relationship('BedInfo', backref='institution', uselist=False, lazy='select')
    service_schedules = db.relationship('ServiceSchedule', backref='institution', lazy='dynamic')
    
    def __repr__(self):
        return f'<Institution {self.name}>'


class Order(db.Model):
    """订单表"""
    __tablename__ = 'orders'
    
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='订单ID')
    user_id = db.Column(db.String(64), db.ForeignKey('users.user_id'), nullable=False, comment='用户ID')
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.institution_id'), nullable=False, comment='机构ID')
    
    # 预约人信息
    name = db.Column(db.String(50), nullable=False, comment='预约人姓名')
    phone = db.Column(db.String(20), nullable=False, comment='联系电话')
    address = db.Column(db.String(200), nullable=False, comment='地址')
    
    # 订单信息
    order_time = db.Column(db.DateTime, default=datetime.now, comment='下单时间')
    use_date = db.Column(db.String(20), comment='使用日期')
    use_time = db.Column(db.Integer, comment='使用时间段：0-上午, 1-下午')
    service_type = db.Column(db.String(50), comment='服务类型：居家上门/到点服务/床位预约')
    service = db.Column(db.String(100), comment='具体服务内容')
    
    # 订单状态：0-待使用, 1-排队中, 2-已取消, 3-已完成
    status = db.Column(db.Integer, default=0, comment='订单状态')
    queue_num = db.Column(db.Integer, comment='排队人数')
    
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<Order {self.order_id}>'


class Favorite(db.Model):
    """收藏表"""
    __tablename__ = 'favorites'
    
    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='收藏ID')
    user_id = db.Column(db.String(64), db.ForeignKey('users.user_id'), nullable=False, comment='用户ID')
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.institution_id'), nullable=False, comment='机构ID')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='收藏时间')
    
    # 唯一约束：一个用户对同一个机构只能收藏一次
    __table_args__ = (
        db.UniqueConstraint('user_id', 'institution_id', name='uk_user_institution'),
    )
    
    def __repr__(self):
        return f'<Favorite {self.favorite_id}>'


class ReservingPerson(db.Model):
    """常用预约者表"""
    __tablename__ = 'reserving_persons'
    
    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='预约者ID')
    user_id = db.Column(db.String(64), db.ForeignKey('users.user_id'), nullable=False, comment='用户ID')
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    gender = db.Column(db.String(10), comment='性别')
    address = db.Column(db.String(200), comment='地址')
    phone = db.Column(db.String(20), comment='联系电话')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<ReservingPerson {self.name}>'


class BedInfo(db.Model):
    """床位信息表"""
    __tablename__ = 'bed_info'
    
    bed_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='床位信息ID')
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.institution_id'), unique=True, nullable=False, comment='机构ID')
    sum = db.Column(db.Integer, default=0, comment='总床位数')
    booked = db.Column(db.Integer, default=0, comment='已预约床位数')
    waiting = db.Column(db.Integer, default=0, comment='等待中人数')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<BedInfo institution_id={self.institution_id}>'


class ServiceSchedule(db.Model):
    """服务时间表（用于记录机构在特定日期和时间段的服务情况）"""
    __tablename__ = 'service_schedules'
    
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='时间表ID')
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.institution_id'), nullable=False, comment='机构ID')
    date = db.Column(db.String(20), nullable=False, comment='日期')
    time = db.Column(db.Integer, nullable=False, comment='时间段：0-上午, 1-下午')
    service_type = db.Column(db.Integer, nullable=False, comment='服务类型：0-居家上门, 1-到点服务')
    surplus = db.Column(db.Integer, default=0, comment='剩余工作人员数量')
    total = db.Column(db.Integer, default=0, comment='总工作人员数量')
    
    # 唯一约束：一个机构在特定日期、时间段、服务类型下只能有一条记录
    __table_args__ = (
        db.UniqueConstraint('institution_id', 'date', 'time', 'service_type', 
                          name='uk_institution_datetime_service'),
    )
    
    def __repr__(self):
        return f'<ServiceSchedule {self.schedule_id}>'

