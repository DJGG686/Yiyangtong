# --- coding:utf-8 ---
# @author  : digjie
# @time    : 2025/10/25 12:37
# @filename: wechat_api
# @function: 
# @version : V1

import requests
import jwt
from flask import current_app
from datetime import datetime


class WeChatAPI:
    @staticmethod
    def code2session(code):
        """
        微信登录凭证校验
        文档: https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
        """
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        params = {
            'appid': current_app.config['WECHAT_APPID'],
            'secret': current_app.config['WECHAT_SECRET'],
            'js_code': code,
            'grant_type': 'authorization_code'
        }

        try:
            data = requests.get(url, params=params, timeout=10).json()

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


