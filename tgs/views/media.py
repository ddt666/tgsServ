from collections import OrderedDict

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from tgs.models import Media
from tgs.serializer.media import MediaSerializer
from tgs.utils.response import BaseResponse
from tgs.utils.pagination import MyPagination


class MediaView(APIView):
    def get(self, request):
        request = request  # type:Request
        queryset = Media.objects.all().order_by("-id")
        name_param = request.query_params.get("name")
        if name_param:
            queryset = queryset.filter(name__contains=name_param)

        paginator = MyPagination()
        page_queryset = paginator.paginate_queryset(queryset, request, view=None)

        media_ser = MediaSerializer(page_queryset, many=True)

        data = OrderedDict([
            ('count', paginator.page.paginator.count),
            ('next', paginator.get_next_link()),
            ('previous', paginator.get_previous_link()),
            ('results', media_ser.data)
        ])


        res = BaseResponse()
        res.msg = "获取媒体列表成功！"
        res.data = data
        return Response(res.__dict__)

    def post(self, request):
        media_data = request.data
        ser_obj = MediaSerializer(data=media_data)
        res = BaseResponse()
        if ser_obj.is_valid():
            ser_obj.save()
            res.msg = "添加媒体成功！"
            res.data = ser_obj.data
            return Response(res.__dict__)
        else:
            res.code = 1001
            res.msg = "添加媒体失败！"
            res.data = None
            return Response(res.__dict__)


class MediaEditView(APIView):
    def get(self, request, id):
        query_set = Media.objects.filter(id=id).first()
        media_ser = MediaSerializer(query_set)
        res = BaseResponse()
        res.msg = "获取媒体"
        res.data = media_ser.data
        return Response(res.dict)

    def patch(self, request, id):
        res = BaseResponse()
        print("id", id)
        query_set = Media.objects.filter(id=id).first()
        media_ser = MediaSerializer(query_set, data=request.data, partial=True)
        if media_ser.is_valid():
            media_ser.save()
            res.msg = "媒体修改成功"
            res.data = media_ser.data
            return Response(res.dict)
        else:
            print(media_ser.errors)
            res.code = 1001
            res.msg = "媒体修改失败"

            return Response(res.dict)


class MediaSort(APIView):
    def get(self, request):
        choices = Media._meta.get_field("sort").choices
        li = []
        for c in choices:
            li.append({"sort": c[0], "text": c[1]})
        res = BaseResponse()
        res.msg = "获取媒体分类成功！"
        res.data = li
        return Response(res.__dict__)
