from rest_framework import serializers

from tgsAdmin.models import Advertiser


class AdvertSerializer(serializers.ModelSerializer):
    sort_text = serializers.CharField(read_only=True, source="get_sort_display")
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Advertiser
        fields = "__all__"
        # extra_kwargs = {
        #     "sort": {"write_only": True}
        # }

    def get_full_name(self, obj):
        if obj.agent:
            return f"{obj.name} - {obj.agent}"
        else:
            return f"{obj.name}"
