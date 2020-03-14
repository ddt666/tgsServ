import datetime

from django.core.cache import cache
from django.utils import timezone

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from tgsAdmin.utils.response import BaseResponse
from tgsAdmin.models import Token


class LoginAuth(BaseAuthentication):
    def authenticate(self, request):
        res = BaseResponse()
        token = request.META.get("HTTP_AUTHORIZATION")
        print("token", token)
        expire = datetime.timedelta(weeks=1)
        # expire = datetime.timedelta(minutes=2)
        user = cache.get(token)
        print("user", user)
        if user:
            cache.set(token, user, expire.total_seconds())
            return user, token

        token_obj = Token.objects.filter(key=token).first()
        if not token_obj:
            res.msg = "认证失败"
            res.code = 4001
            raise AuthenticationFailed(res.dict)

        print("token_obj.created", token_obj.created)
        print("now", timezone.now())
        delta = timezone.now() - token_obj.created
        print("delta", delta)

        if delta > expire:
            res.msg = "认证超时"
            res.code = 4002
            raise AuthenticationFailed(res.dict)
            # return Response(res.dict)

        user = token_obj.user
        cache.set(token, user, expire.total_seconds())
        return user, token_obj.key
