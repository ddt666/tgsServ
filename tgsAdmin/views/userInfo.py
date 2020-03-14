import uuid

from django.contrib import auth
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from tgsAdmin.utils.response import BaseResponse
from tgsAdmin.models import UserInfo
from tgsAdmin.models import Token
from tgsAdmin.serializer.userInfo import UserInfoSerializer
from tgsAdmin.utils.auth import LoginAuth


class UserInfoView(APIView):
    authentication_classes = [LoginAuth]

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        user_obj = request.user
        ser = UserInfoSerializer(user_obj)
        res.data = ser.data
        res.msg = "获取用户信息成功"

        return Response(res.dict)
