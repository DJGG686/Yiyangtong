# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/15 15:57
# @filename: user_service
# @function: 
# @version : V1
# @description : 用户服务类
from flask import request, jsonify

from models import db, User, Order, Favorite
from utils.wechat_api import WeChatAPI


class UserService:
    def __init__(self):
        pass

    @staticmethod
    def login():
        """用户登录"""
        code = request.json.get('code')
        if not code:
            return jsonify({'error': '缺少登录凭证'}), 400

        # 调用微信API获取session信息
        session_data = WeChatAPI.code2session(code)
        if not session_data:
            return jsonify({'error': '登录失败'}), 401

        # 获取或创建用户
        user = UserService.get_or_create_user(session_data['openid'])

        return jsonify({
            'message': '登录成功',
            'user_id': user.user_id
        }), 200

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

