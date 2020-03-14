from rest_framework import serializers

from tgsAdmin.models import AdLocation, Port, ChargeSort


class AdLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdLocation
        fields = ["id", "title"]


class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = ["id", "title"]


class ChargeSortSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeSort
        fields = "__all__"
