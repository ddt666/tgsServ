from rest_framework.response import Response
from rest_framework.views import APIView

from tgsAdmin.utils.response import BaseResponse
from tgsAdmin.models import Advertiser
from tgsAdmin.serializer.advert import AdvertSerializer


class AdvertiserView(APIView):
    def get(self, request, *arg, **kwargs):
        query_set = Advertiser.objects.all().order_by('-id')
        ad_ser = AdvertSerializer(query_set, many=True)
        res = BaseResponse()
        res.msg = "获取所有广告成功！"
        res.data = ad_ser.data
        return Response(res.dict)

    def post(self, request):
        receive = request.data
        ser_obj = AdvertSerializer(data=receive)
        res = BaseResponse()
        if ser_obj.is_valid():
            ser_obj.save()
            res.msg = "添加广告成功！"
            res.data = ser_obj.data
            return Response(res.dict)
        else:
            res.code = -1001
            res.msg = "添加广告失败！"
            return Response(res.dict)
