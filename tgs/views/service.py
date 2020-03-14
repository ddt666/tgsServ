import datetime
from collections import OrderedDict

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from tgs.models import AdService
from tgs.serializer.service import AdServiceSerializer
from tgs.utils.response import BaseResponse
from tgs.utils.pagination import MyPagination


class AdServiceView(APIView):
    def get(self, request):
        request = request  # type:Request
        queryset = AdService.objects.all().order_by("-id")
        # name_param = request.query_params.get("name")
        # if name_param:
        #     queryset = queryset.filter(name__contains=name_param)

        # paginator = MyPagination()
        # page_queryset = paginator.paginate_queryset(queryset, request, view=None)

        media_ser = AdServiceSerializer(queryset, many=True)

        res = BaseResponse()
        res.msg = "获取投放列表成功！"
        res.data = media_ser.data
        return Response(res.dict)


class ServiceEditView(APIView):
    def get(self, request, *args, **kwargs):
        serv_id = kwargs.get("serv_id")
        res = BaseResponse()
        if serv_id:
            serv_obj = AdService.objects.filter(id=serv_id).first()

            serv_ser = AdServiceSerializer(instance=serv_obj)

            res.msg = "获取单个投放成功！"
            res.data = serv_ser.data
            return Response(res.dict)

    def patch(self, request, *args, **kwargs):
        serv_id = kwargs.get("serv_id")
        serv_data = request.data
        res = BaseResponse()
        serv_obj = AdService.objects.filter(id=serv_id).first()
        if serv_data.get("status") == 1:
            serv_obj.settlement_time = datetime.datetime.now()

        serv_ser = AdServiceSerializer(instance=serv_obj, data=request.data, partial=True)
        if serv_ser.is_valid():
            serv_ser.save()
            res.data = serv_ser.data
        else:
            print(serv_ser.errors)
        return Response(res.dict)
