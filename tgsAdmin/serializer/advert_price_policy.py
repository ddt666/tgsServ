# from rest_framework import serializers
#
# from tgsAdmin.models import AdPricePolicy
#
#
# class AdPricePolicySerializer(serializers.ModelSerializer):
#     ad_full_name = serializers.SerializerMethodField(read_only=True)
#
#     charge_sort_text = serializers.CharField(source='charge_sort.title', read_only=True)
#
#     def get_ad_full_name(self, obj):
#         return obj.advert.__str__()
#
#     class Meta:
#         model = AdPricePolicy
#         fields = "__all__"
