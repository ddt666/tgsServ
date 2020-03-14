from collections import OrderedDict

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from tgs.models import AdData
from tgs.serializer.service import AdDataSerializer
from tgs.utils.response import BaseResponse
from tgs.utils.pagination import MyPagination


class AdDataView(APIView):
    def post(self, request, *args, **kwargs):
        ad_data = request.data

        ad_ser = AdDataSerializer(data=ad_data)
        res = BaseResponse()
        if ad_ser.is_valid():
            ad_obj = ad_ser.save()
            print(ad_obj)
            ad_obj.ad_plan.status = 1
            ad_obj.ad_plan.save()
            res.data = ad_ser.data
        else:
            res.code=1001
            res.msg = ad_ser.errors
        return Response(res.dict)
