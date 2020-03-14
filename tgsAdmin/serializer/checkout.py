from rest_framework import serializers


class AdvertCheckoutSerializer(serializers.Serializer):
    advertiser = serializers.IntegerField(source="plan__advertiser__pk")
    advertiser_name = serializers.CharField(source="plan__advertiser__name")
    start_time = serializers.DateTimeField(source="start", format="%Y-%m-%d")
    # start_time = serializers.SerializerMethodField(source="start")
    end_time = serializers.DateTimeField(source="end", format="%Y-%m-%d")
    income = serializers.SerializerMethodField()

    def get_income(self, obj):
        print("obj", obj)
        return round(obj["income"], 3)
