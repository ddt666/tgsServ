import uuid

from django.contrib import auth
from django.utils import timezone
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response

from tgsAdmin.utils.response import BaseResponse
from tgsAdmin.models import UserInfo
from tgsAdmin.models import Token
from tgsAdmin.utils.auth import LoginAuth
from tgsAdmin.serializer.userInfo import UserInfoSerializer


class LoginView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        res = BaseResponse()

        receive = request.data

        user = receive.get("username")
        pwd = receive.get("password")

        user_obj = auth.authenticate(username=user, password=pwd)
        if user_obj:
            random_str = "".join(str(uuid.uuid4()).split("-"))
            Token.objects.update_or_create(user=user_obj,
                                           defaults={"key": random_str, "created": timezone.now()})
            ser = UserInfoSerializer(instance=user_obj)
            res.msg = "登录成功"
            res.data = ser.data
            res.token = random_str
        else:
            try:
                UserInfo.objects.get(username=user)
                res.msg = "密码错误"
                res.code = -1001
            except UserInfo.DoesNotExist:
                res.msg = "用户不存在"
                res.code = -1002

        return Response(res.dict)


class LogoutView(APIView):


    def post(self, request):
        res = BaseResponse()
        user_id = request.user.pk

        cache.delete(request.auth)
        Token.objects.filter(user=user_id).delete()
        res.msg = "退出成功"
        return Response(res.__dict__)

