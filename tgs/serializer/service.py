from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from tgs.models import AdService, MediaPlan, AdPlan, MediaData, AdData


class AdDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdData
        fields = "__all__"
        read_only_fields = ["click_rate", "income"]


class MediaDataSerializer(serializers.ModelSerializer):
    # serv_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MediaData
        fields = "__all__"
        read_only_fields = ["click_rate", "cost"]


class AdPlanSerializer(serializers.ModelSerializer):
    ad_text = serializers.SerializerMethodField(read_only=True)
    charge_sort_text = serializers.SerializerMethodField(read_only=True)
    ad_data = serializers.SerializerMethodField(read_only=True)

    def get_ad_text(self, obj):
        return obj.ad.name

    def get_charge_sort_text(self, obj):
        return obj.charge_sort.title

    def get_ad_data(self, obj):

        try:
            ad_data_obj = AdDataSerializer(instance=obj.addata)
            # print("obj.ad_data_obj", media_data_obj.data)
            return ad_data_obj.data

        except ObjectDoesNotExist:
            return None

    class Meta:
        model = AdPlan
        # fields = "__all__"
        exclude = ["created"]


class MediaPlanSerializer(serializers.ModelSerializer):
    media_text = serializers.SerializerMethodField(read_only=True)
    location_text = serializers.SerializerMethodField(read_only=True)
    charge_sort_text = serializers.SerializerMethodField(read_only=True)
    port_text = serializers.CharField(source="get_port_display", read_only=True)
    media_data = serializers.SerializerMethodField(read_only=True)

    def get_media_text(self, obj):
        return obj.media.name

    def get_location_text(self, obj):
        return obj.location.title

    def get_charge_sort_text(self, obj):
        return obj.charge_sort.title

    def get_media_data(self, obj):

        try:
            media_data_obj = MediaDataSerializer(instance=obj.mediadata)
            # print("obj.mediadata", media_data_obj.data)
            return media_data_obj.data

        except ObjectDoesNotExist:
            return None

    class Meta:
        model = MediaPlan
        # fields = "__all__"
        exclude = ["created"]


class AdServiceSerializer(serializers.ModelSerializer):
    status_text = serializers.CharField(source='get_status_display', read_only=True)
    media_plan = MediaPlanSerializer(read_only=True)
    ad_plan = AdPlanSerializer(read_only=True)
    serv_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = AdService
        fields = "__all__"
        read_only_fields = ["created"]
        # exclude = ["created"]
        # depth = 1
        # extra_kwargs = {
        #     "sort": {"write_only": True}
        # }
