from collections import OrderedDict

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from tgs.models import MediaData, AdService
from tgs.serializer.service import MediaDataSerializer
from tgs.utils.response import BaseResponse
from tgs.utils.pagination import MyPagination


class MediaDataView(APIView):
    def post(self, request, *args, **kwargs):
        m_data = request.data
        serv_id = m_data.pop("serv_id")
        print("serv_id", serv_id)
        m_ser = MediaDataSerializer(data=m_data)
        res = BaseResponse()
        if m_ser.is_valid():
            m_obj = m_ser.save()
            print(m_obj)
            m_obj.media_plan.status = 1
            m_obj.media_plan.save()
            res.data = m_ser.data

            # 检查广告是否结算并结算整个服务
            serv_obj = AdService.objects.get(id=serv_id)
            if serv_obj.ad_plan.status == 1:
                serv_obj.status = 1
                serv_obj.save()




        else:
            res.code = 1001
            res.msg = m_ser.errors
        return Response(res.dict)
