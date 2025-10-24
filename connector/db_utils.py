"""
数据库工具函数
提供常用的数据库操作辅助函数
"""
from models import db, User, Institution, Order, Favorite, ReservingPerson, BedInfo, ServiceSchedule
from datetime import datetime


class UserService:
    """用户相关服务"""
    
    @staticmethod
    def get_or_create_user(openid):
        """根据openid获取或创建用户"""
        user = User.query.filter_by(openid=openid).first()
        if not user:
            user = User(user_id=f"user_{openid[:16]}", openid=openid)
            db.session.add(user)
            db.session.commit()
        return user
    
    @staticmethod
    def get_user_orders(user_id):
        """获取用户的所有订单"""
        return Order.query.filter_by(user_id=user_id).order_by(Order.order_time.desc()).all()
    
    @staticmethod
    def get_user_favorites(user_id):
        """获取用户收藏的机构"""
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        return [fav.institution for fav in favorites]
    
    @staticmethod
    def add_favorite(user_id, institution_id):
        """添加收藏"""
        existing = Favorite.query.filter_by(
            user_id=user_id, 
            institution_id=institution_id
        ).first()
        
        if not existing:
            favorite = Favorite(user_id=user_id, institution_id=institution_id)
            db.session.add(favorite)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def remove_favorite(user_id, institution_id):
        """取消收藏"""
        favorite = Favorite.query.filter_by(
            user_id=user_id, 
            institution_id=institution_id
        ).first()
        
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return True
        return False


class InstitutionService:
    """机构相关服务"""
    
    @staticmethod
    def get_institutions(district=None, service_type=None, page=1, page_size=10):
        """
        获取机构列表
        :param district: 区域筛选
        :param service_type: 服务类型（1-到点服务, 2-居家上门, 4-床位预约）
        :param page: 页码
        :param page_size: 每页数量
        """
        query = Institution.query
        
        if district:
            query = query.filter_by(district=district)
        
        if service_type:
            # 使用位运算筛选支持该服务类型的机构
            query = query.filter(Institution.service_types.op('&')(service_type) > 0)
        
        return query.paginate(page=page, per_page=page_size, error_out=False)
    
    @staticmethod
    def get_institution_detail(institution_id, user_id=None):
        """
        获取机构详情
        :param institution_id: 机构ID
        :param user_id: 用户ID（用于判断是否收藏）
        """
        institution = Institution.query.get(institution_id)
        if not institution:
            return None
        
        result = {
            'institution_id': institution.institution_id,
            'name': institution.name,
            'score': institution.score,
            'address': institution.address,
            'phone': institution.phone,
            'cover': institution.cover,
            'is_favorite': False
        }
        
        if user_id:
            favorite = Favorite.query.filter_by(
                user_id=user_id,
                institution_id=institution_id
            ).first()
            result['is_favorite'] = favorite is not None
        
        return result
    
    @staticmethod
    def get_service_schedule(institution_id, service_type):
        """
        获取机构服务时间表
        :param institution_id: 机构ID
        :param service_type: 服务类型（0-居家上门, 1-到点服务）
        """
        schedules = ServiceSchedule.query.filter_by(
            institution_id=institution_id,
            service_type=service_type
        ).order_by(ServiceSchedule.date, ServiceSchedule.time).all()
        
        # 按日期分组
        result = {}
        for schedule in schedules:
            if schedule.date not in result:
                result[schedule.date] = []
            result[schedule.date].append({
                'time': schedule.time,
                'surplus': schedule.surplus
            })
        
        return [{'date': date, 'time': times} for date, times in result.items()]
    
    @staticmethod
    def get_bed_info(institution_id):
        """获取机构床位信息"""
        return BedInfo.query.filter_by(institution_id=institution_id).first()


class OrderService:
    """订单相关服务"""
    
    @staticmethod
    def create_order(user_id, institution_id, name, phone, address, 
                    use_date, use_time=None, service_type='', service=''):
        """
        创建订单
        :param user_id: 用户ID
        :param institution_id: 机构ID
        :param name: 预约人姓名
        :param phone: 联系电话
        :param address: 地址
        :param use_date: 使用日期
        :param use_time: 使用时间段（0-上午, 1-下午）
        :param service_type: 服务类型
        :param service: 具体服务内容
        """
        order = Order(
            user_id=user_id,
            institution_id=institution_id,
            name=name,
            phone=phone,
            address=address,
            use_date=use_date,
            use_time=use_time,
            service_type=service_type,
            service=service,
            status=0  # 待使用
        )
        
        db.session.add(order)
        
        # 如果是服务预约，减少可用人员数量
        if use_time is not None and service_type in ['居家上门', '到点服务']:
            st = 0 if service_type == '居家上门' else 1
            schedule = ServiceSchedule.query.filter_by(
                institution_id=institution_id,
                date=use_date,
                time=use_time,
                service_type=st
            ).first()
            
            if schedule and schedule.surplus > 0:
                schedule.surplus -= 1
        
        # 如果是床位预约，增加等待人数
        if service_type == '床位预约':
            bed_info = BedInfo.query.filter_by(institution_id=institution_id).first()
            if bed_info:
                bed_info.waiting += 1
        
        db.session.commit()
        return order
    
    @staticmethod
    def update_order_status(order_id, status, queue_num=None):
        """
        更新订单状态
        :param order_id: 订单ID
        :param status: 新状态（0-待使用, 1-排队中, 2-已取消, 3-已完成）
        :param queue_num: 排队人数
        """
        order = Order.query.get(order_id)
        if not order:
            return False
        
        order.status = status
        if queue_num is not None:
            order.queue_num = queue_num
        
        db.session.commit()
        return True
    
    @staticmethod
    def get_schedule_by_date(user_id, date):
        """
        获取用户某天的行程安排
        :param user_id: 用户ID
        :param date: 日期
        """
        orders = Order.query.filter_by(
            user_id=user_id,
            use_date=date
        ).filter(Order.status.in_([0, 1])).all()  # 只显示待使用和排队中的订单
        
        schedule_list = []
        for order in orders:
            schedule_list.append({
                'name': order.institution.name if order.institution else '',
                'address': order.address,
                'time': '上午' if order.use_time == 0 else '下午' if order.use_time == 1 else '',
                'object': order.name
            })
        
        return schedule_list


class ReservingPersonService:
    """常用预约者服务"""
    
    @staticmethod
    def get_persons(user_id):
        """获取用户的常用预约者列表"""
        return ReservingPerson.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def add_person(user_id, name, gender, address, phone):
        """添加常用预约者"""
        person = ReservingPerson(
            user_id=user_id,
            name=name,
            gender=gender,
            address=address,
            phone=phone
        )
        db.session.add(person)
        db.session.commit()
        return person
    
    @staticmethod
    def update_person(person_id, name=None, gender=None, address=None, phone=None):
        """更新常用预约者信息"""
        person = ReservingPerson.query.get(person_id)
        if not person:
            return False
        
        if name:
            person.name = name
        if gender:
            person.gender = gender
        if address:
            person.address = address
        if phone:
            person.phone = phone
        
        db.session.commit()
        return True
    
    @staticmethod
    def delete_person(person_id):
        """删除常用预约者"""
        person = ReservingPerson.query.get(person_id)
        if not person:
            return False
        
        db.session.delete(person)
        db.session.commit()
        return True


# 辅助函数
def to_dict(model_instance):
    """将模型实例转换为字典"""
    if model_instance is None:
        return None
    
    result = {}
    for column in model_instance.__table__.columns:
        value = getattr(model_instance, column.name)
        if isinstance(value, datetime):
            value = value.strftime('%Y-%m-%d %H:%M:%S')
        result[column.name] = value
    return result


def models_to_dict_list(models):
    """将模型列表转换为字典列表"""
    return [to_dict(model) for model in models]

