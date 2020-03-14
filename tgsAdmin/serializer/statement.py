from rest_framework import serializers

from tgsAdmin.models import MediaStatement,AdvertStatement


class StatementSerializer(serializers.Serializer):
    media = serializers.IntegerField(source="plan__media__pk")
    media_name = serializers.CharField(source="plan__media__name")
    start_time = serializers.DateTimeField(source="start", format="%Y-%m-%d")
    # start_time = serializers.SerializerMethodField(source="start")
    end_time = serializers.DateTimeField(source="end", format="%Y-%m-%d")
    cost = serializers.SerializerMethodField()

    def get_cost(self, obj):
        print("obj", obj)
        if obj.get("cost"):
            return round(obj["cost"], 3)
        return None






class MediaStatementSerializer(serializers.ModelSerializer):
    media_name = serializers.CharField(source="media.name", read_only=True)
    start_time = serializers.DateTimeField(format="%Y-%m-%d")
    # start_time = serializers.SerializerMethodField(source="start")
    end_time = serializers.DateTimeField(format="%Y-%m-%d")
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = MediaStatement
        fields = "__all__"
        # exclude = ["end_time"]


class AdvertStatementSerializer(serializers.ModelSerializer):
    advertiser_name = serializers.CharField(source="advertiser.name", read_only=True)
    start_time = serializers.DateTimeField(format="%Y-%m-%d")
    # start_time = serializers.SerializerMethodField(source="start")
    end_time = serializers.DateTimeField(format="%Y-%m-%d")
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = AdvertStatement
        fields = "__all__"
        # exclude = ["end_time"]
