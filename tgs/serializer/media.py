from rest_framework import serializers

from tgs.models import Media


class MediaSerializer(serializers.ModelSerializer):
    sort_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Media
        fields = "__all__"
        # extra_kwargs = {
        #     "sort": {"write_only": True}
        # }

    def get_sort_info(self, obj):
        return {"sort": obj.sort, "text": obj.get_sort_display()}


