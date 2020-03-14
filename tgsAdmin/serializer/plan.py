import datetime

from rest_framework import serializers

from tgsAdmin.models import Plan, Settlement
from tgsAdmin.serializer.settlement import SettlementSerializer


# from tgsAdmin.serializer.advert_price_policy import AdPricePolicySerializer
# from tgsAdmin.serializer.media_price_policy import MediaPricePolicySerializer
#
#
# class PlanDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Settlement
#         fields = "__all__"
#
#
# class PlanSerializer(serializers.ModelSerializer):
#     launch_date = serializers.DateTimeField(format='%Y-%m-%d', input_formats=None)
#     launch_date_str = serializers.SerializerMethodField()
#     media_id = serializers.IntegerField(source='media_price_policy.media.id', read_only=True)
#     media_full_name = serializers.CharField(source='media_price_policy.media', read_only=True)
#     media_location_text = serializers.CharField(source='media_price_policy.location.title', read_only=True)
#     media_port_text = serializers.CharField(source='media_price_policy.port.title', read_only=True)
#     media_charge_sort_text = serializers.CharField(source='media_price_policy.charge_sort.title', read_only=True)
#     media_unit_price = serializers.FloatField(source='media_price_policy.unit_price', read_only=True)
#     media_exposure_count = serializers.IntegerField(source='settlement.media_data.exposure_count', read_only=True)
#     media_click_count = serializers.IntegerField(source='settlement.media_data.click_count', read_only=True)
#     media_click_rate = serializers.IntegerField(source='settlement.media_data.click_rate', read_only=True)
#
#     # media_price_policy_info = MediaPricePolicySerializer(source="media_price_policy")
#
#     ad_id = serializers.IntegerField(source='ad_price_policy.advert.id', read_only=True)
#     ad_full_name = serializers.CharField(source='ad_price_policy.advert', read_only=True)
#     ad_url = serializers.CharField(source='ad_price_policy.url')
#     # charge_sort_text = serializers.CharField(source='charge_sort.title', read_only=True)
#     ad_charge_sort_text = serializers.CharField(source='ad_price_policy.charge_sort.title', read_only=True)
#     ad_unit_price = serializers.FloatField(source='ad_price_policy.unit_price', read_only=True)
#
#     ad_exposure_count = serializers.IntegerField(source='settlement.ad_data.exposure_count', read_only=True)
#     ad_click_count = serializers.IntegerField(source='settlement.ad_data.click_count', read_only=True)
#     ad_click_rate = serializers.IntegerField(source='settlement.ad_data.click_rate', read_only=True)
#     ad_week_rate = serializers.IntegerField(source='settlement.ad_data.week_rate', read_only=True)
#
#     # ad_price_policy_info = AdPricePolicySerializer(source="ad_price_policy")
#     settlement_count=serializers.IntegerField(source='settlement.settlement_count', read_only=True)
#     cost = serializers.IntegerField(source='settlement.cost', read_only=True)
#     income = serializers.IntegerField(source='settlement.income', read_only=True)
#     profit = serializers.IntegerField(source='settlement.profit', read_only=True)
#
#     def get_launch_date_str(self, obj):
#         format = '%Y-%m-%d'
#         return int(datetime.datetime.strptime(obj.launch_date.strftime(format), format).timestamp() * 1000)
#
#     class Meta:
#         model = Plan
#         fields = "__all__"
#         read_only_fields = ["budget", "settlement_status"]


class PlanSerializer(serializers.ModelSerializer):
    launch_date = serializers.DateTimeField(format='%Y-%m-%d')

    launch_date_str = serializers.SerializerMethodField(read_only=True)
    # media_id = serializers.IntegerField(source='media_price_policy.media.id', read_only=True)
    m_full_name = serializers.CharField(source='media', read_only=True)
    m_location_text = serializers.CharField(source='m_location.title', read_only=True)
    m_port_text = serializers.CharField(source='m_port.title', read_only=True)
    m_charge_sort_text = serializers.CharField(source='m_charge_sort.title', read_only=True)

    # ad_id = serializers.IntegerField(source='ad_price_policy.advert.id', read_only=True)
    a_full_name = serializers.CharField(source='advertiser', read_only=True)
    # ad_url = serializers.CharField(source='ad_price_policy.url')
    # # charge_sort_text = serializers.CharField(source='charge_sort.title', read_only=True)
    a_charge_sort_text = serializers.CharField(source='a_charge_sort.title', read_only=True)
    settlement_info = SettlementSerializer(source='settlement', read_only=True)

    # d_unit_price = serializers.FloatField(source='ad_price_policy.unit_price', read_only=True)

    # m_unit_price = serializers.FloatField(source='settlement.m_unit_price', read_only=True)
    # media_exposure_count = serializers.IntegerField(source='settlement.media_data.exposure_count', read_only=True)
    # media_click_count = serializers.IntegerField(source='settlement.media_data.click_count', read_only=True)
    # media_click_rate = serializers.IntegerField(source='settlement.media_data.click_rate', read_only=True)
    #
    # # media_price_policy_info = MediaPricePolicySerializer(source="media_price_policy")
    #
    # ad_id = serializers.IntegerField(source='ad_price_policy.advert.id', read_only=True)
    # ad_full_name = serializers.CharField(source='ad_price_policy.advert', read_only=True)
    # ad_url = serializers.CharField(source='ad_price_policy.url')
    # # charge_sort_text = serializers.CharField(source='charge_sort.title', read_only=True)
    # ad_charge_sort_text = serializers.CharField(source='ad_price_policy.charge_sort.title', read_only=True)
    # ad_unit_price = serializers.FloatField(source='ad_price_policy.unit_price', read_only=True)
    #
    # ad_exposure_count = serializers.IntegerField(source='settlement.ad_data.exposure_count', read_only=True)
    # ad_click_count = serializers.IntegerField(source='settlement.ad_data.click_count', read_only=True)
    # ad_click_rate = serializers.IntegerField(source='settlement.ad_data.click_rate', read_only=True)
    # ad_week_rate = serializers.IntegerField(source='settlement.ad_data.week_rate', read_only=True)
    #
    # # ad_price_policy_info = AdPricePolicySerializer(source="ad_price_policy")
    # settlement_count=serializers.IntegerField(source='settlement.settlement_count', read_only=True)
    # cost = serializers.IntegerField(source='settlement.cost', read_only=True)
    # income = serializers.IntegerField(source='settlement.income', read_only=True)
    # profit = serializers.IntegerField(source='settlement.profit', read_only=True)

    def get_launch_date_str(self, obj):
        format = '%Y-%m-%d'
        return int(datetime.datetime.strptime(obj.launch_date.strftime(format), format).timestamp() * 1000)

    class Meta:
        model = Plan
        fields = "__all__"
        # read_only_fields = ["budget", "settlement_status"]


class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = "__all__"
        # read_only_fields = ["budget", "settlement_status"]
