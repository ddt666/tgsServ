from rest_framework import serializers

from tgsAdmin.models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["id","username"]
