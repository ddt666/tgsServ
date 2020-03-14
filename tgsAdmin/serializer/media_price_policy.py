# from rest_framework import serializers
#
# from tgsAdmin.models import MediaPricePolicy
#
#
# class MediaPricePolicySerializer(serializers.ModelSerializer):
#     media_full_name = serializers.SerializerMethodField(read_only=True)
#     location_text = serializers.CharField(source='location.title', read_only=True)
#     port_text = serializers.CharField(source='port.title', read_only=True)
#     charge_sort_text = serializers.CharField(source='charge_sort.title', read_only=True)
#
#     def get_media_full_name(self, obj):
#         return obj.media.__str__()
#
#     class Meta:
#         model = MediaPricePolicy
#         fields = "__all__"
