import datetime
from abc import abstractmethod, ABC

import jwt
from rest_framework import authentication, exceptions
from django.contrib.auth.models import User
from decouple import config


class Token(ABC):
    @abstractmethod
    def get_token_str(self):
        pass


class JWTToken(Token):
    def __init__(self, payload, secret_key):
        self._payload = payload
        self._secret_key = secret_key

    def get_token_str(self):
        return jwt.encode(self._payload, self._secret_key, algorithm='HS256')


class TokenFactory(ABC):
    @abstractmethod
    def create_token(self, user_id, username):
        pass


class JWTTokenFactory(TokenFactory):
    def create_token(self, user_id, username):
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': int(config('TOKEN_EXPIRATION_TIME', default=3600))
        }
        return JWTToken(payload, config('SECRET_KEY'))


def generate_jwt_token(user_id, username, factory=JWTTokenFactory()):
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(config('TOKEN_EXPIRATION_TIME', default=3600)))
    }
    token = jwt.encode(payload, config('SECRET_KEY'), algorithm='HS256')
    return token
    # return factory.create_token(user_id, username)


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(' ')
        except ValueError:
            raise exceptions.AuthenticationFailed('Неверный формат токена')

        if prefix.lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Неверный тип токена')

        try:
            payload = jwt.decode(token, config('SECRET_KEY'), algorithms=['HS256'])
            user_id = payload['user_id']
            username = payload['username']
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Срок действия токена истек')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Неверный токен')

        try:
            user = User.objects.get(pk=user_id, username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Пользователь не найден')

        return (user, None)
