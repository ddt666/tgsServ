from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from tgsAdmin.utils.response import BaseResponse
from tgsAdmin.models import AdLocation, Port, ChargeSort
from tgsAdmin.serializer.option import AdLocationSerializer, PortSerializer, ChargeSortSerializer


class OptionView(APIView):
    def get(self, request, *arg, **kwargs):
        option_dict = {}
        loc_query_set = AdLocation.objects.all()
        loc_ser = AdLocationSerializer(loc_query_set, many=True)

        option_dict["location"] = loc_ser.data

        port_query_set = Port.objects.all()
        port_ser = PortSerializer(port_query_set, many=True)

        option_dict["port"] = port_ser.data

        sort_query_set = ChargeSort.objects.all()
        sort_ser = ChargeSortSerializer(sort_query_set, many=True)

        option_dict["charge_sort"] = sort_ser.data

        res = BaseResponse()
        res.msg = "获取配置成功！"
        res.data = option_dict
        return Response(res.dict)


class LocationView(APIView):
    def post(self, request, *args, **kwargs):
        res = BaseResponse()
        receive = request.data

        ser = AdLocationSerializer(data=receive)

        if ser.is_valid():
            ser.save()
            res.msg = "添加位置成功"
            res.data = ser.data
        else:
            res.code = -1
            res.msg = ser.errors
        return Response(res.dict)


class PortView(APIView):
    def post(self, request, *args, **kwargs):
        res = BaseResponse()
        receive = request.data
        ser = PortSerializer(data=receive)

        if ser.is_valid():
            ser.save()
            res.msg = "添加端口成功"
            res.data = ser.data
        else:
            res.code = -1
            res.msg = ser.errors
        return Response(res.dict)


class ChargeSortView(APIView):
    def post(self, request, *args, **kwargs):
        res = BaseResponse()
        receive = request.data
        ser = ChargeSortSerializer(data=receive)

        if ser.is_valid():
            ser.save()
            res.msg = "添加计费类型成功"
            res.data = ser.data
        else:
            res.code = -1
            res.msg = ser.errors
        return Response(res.dict)
