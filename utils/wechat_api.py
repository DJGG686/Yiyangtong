# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/25 12:37
# @filename: wechat_api
# @function: 
# @version : V1

import requests
import jwt
from flask import current_app
from models import db, User, UserSession
from datetime import datetime, timedelta


class WeChatAPI:
    @staticmethod
    def code2session(code):
        """
        微信登录凭证校验
        文档: https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
        """
        appid = current_app.config['WECHAT_APPID']
        secret = current_app.config['WECHAT_SECRET']

        url = 'https://api.weixin.qq.com/sns/jscode2session'
        params = {
            'appid': appid,
            'secret': secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if 'errcode' in data and data['errcode'] != 0:
                current_app.logger.error(f"WeChat API error: {data}")
                return None

            return data
        except Exception as e:
            current_app.logger.error(f"WeChat API request failed: {str(e)}")
            return None

    @staticmethod
    def get_phone_number(code):
        """
        获取用户手机号
        文档: https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-info/phone-number/getPhoneNumber.html
        """
        appid = current_app.config['WECHAT_APPID']
        secret = current_app.config['WECHAT_SECRET']

        # 注意：这里需要先获取access_token
        access_token = WeChatAPI.get_access_token()
        if not access_token:
            return None

        url = 'https://api.weixin.qq.com/wxa/business/getuserphonenumber'
        params = {
            'access_token': access_token
        }
        data = {
            'code': code
        }

        try:
            response = requests.post(url, params=params, json=data, timeout=10)
            result = response.json()

            if result.get('errcode') == 0:
                return result.get('phone_info', {})
            else:
                current_app.logger.error(f"WeChat phone API error: {result}")
                return None
        except Exception as e:
            current_app.logger.error(f"WeChat phone API request failed: {str(e)}")
            return None

    @staticmethod
    def get_access_token():
        """
        获取微信接口调用凭证
        """
        appid = current_app.config['WECHAT_APPID']
        secret = current_app.config['WECHAT_SECRET']

        url = 'https://api.weixin.qq.com/cgi-bin/token'
        params = {
            'grant_type': 'client_credential',
            'appid': appid,
            'secret': secret
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            return data.get('access_token')
        except Exception as e:
            current_app.logger.error(f"Get access token failed: {str(e)}")
            return None


class JWTUtils:
    @staticmethod
    def generate_token(user_id):
        """
        生成JWT token
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            'iat': datetime.utcnow()
        }

        token = jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        return token

    @staticmethod
    def verify_token(token):
        """
        验证JWT token
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            current_app.logger.error("Token expired")
            return None
        except jwt.InvalidTokenError:
            current_app.logger.error("Invalid token")
            return None


def create_or_update_user(wechat_data, user_info=None):
    """
    创建或更新用户信息
    """
    openid = wechat_data.get('openid')
    session_key = wechat_data.get('session_key')

    # 查找用户
    user = User.query.filter_by(openid=openid).first()

    if not user:
        # 创建新用户
        user = User(
            openid=openid,
            unionid=wechat_data.get('unionid')
        )
        db.session.add(user)
        db.session.flush()  # 获取user id

    # 更新用户信息（如果提供了用户信息）
    if user_info:
        user.nickname = user_info.get('nickName')
        user.avatar_url = user_info.get('avatarUrl')
        user.gender = user_info.get('gender', 0)
        user.country = user_info.get('country')
        user.province = user_info.get('province')
        user.city = user_info.get('city')
        user.language = user_info.get('language')

    user.last_login = datetime.utcnow()

    # 保存session
    session = UserSession(
        user_id=user.id,
        session_key=session_key,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.session.add(session)

    db.session.commit()

    return user

