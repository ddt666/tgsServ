import datetime

from rest_framework import serializers

from tgsAdmin.models import Settlement


class SettlementSerializer(serializers.ModelSerializer):
    media = serializers.IntegerField(source="plan.media.pk")
    media_name = serializers.CharField(source="plan.media.name")
    advertiser = serializers.IntegerField(source="plan.advertiser.pk")
    advertiser_name = serializers.CharField(source="plan.advertiser.name")
    m_unit_price_status = serializers.SerializerMethodField(read_only=True)
    a_unit_price_status = serializers.SerializerMethodField(read_only=True)
    status = serializers.IntegerField(read_only=True)

    def get_m_unit_price_status(self, obj):
        if obj.m_unit_price:
            return 1
        else:
            return 0

    def get_a_unit_price_status(self, obj):
        if obj.a_unit_price:
            return 1
        else:
            return 0

    class Meta:
        model = Settlement
        fields = "__all__"
