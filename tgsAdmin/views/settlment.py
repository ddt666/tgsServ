import time, datetime

from django.utils.timezone import now
from django.db.models import Count, Min, Max, Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from tgsAdmin.utils.response import BaseResponse
from tgsAdmin.models import Plan, Settlement, MediaStatement
from tgsAdmin.serializer.settlement import SettlementSerializer
from tgsAdmin.serializer.statement import StatementSerializer, MediaStatementSerializer


class SettlementView(APIView):
    def get(self, request, *args, **kwargs):
        filter_conditions = {}

        for k, v in request.query_params.items():
            if "page" in k.lower():
                pass
            elif "date" in k.lower():
                t = int(v) / 1000

                date_time = datetime.datetime.fromtimestamp(t)
                filter_conditions["plan__" + k] = date_time

            else:
                filter_conditions["plan__" + k] = v
        query_set = Settlement.objects.filter(**filter_conditions)
        print("query_set", query_set)
        ser = SettlementSerializer(query_set, many=True)
        res = BaseResponse()
        res.data = ser.data
        return Response(res.dict)


class SettlementEditView(APIView):
    def get(self, request, *args, **kwargs):
        slt_id = kwargs.get("id")

        slt_obj = Settlement.objects.filter(id=slt_id).first()
        slt_ser = SettlementSerializer(slt_obj)

        res = BaseResponse()
        res.msg = "获取结算实例成功"
        res.data = slt_ser.data

        return Response(res.dict)

    def patch(self, request, *args, **kwargs):
        res = BaseResponse()
        slt_id = kwargs.get("id")

        slt_obj = Settlement.objects.filter(id=slt_id).first()

        print(request.data)
        slt_ser = SettlementSerializer(instance=slt_obj, data=request.data, partial=True)
        if slt_ser.is_valid():
            slt_ser.save()
            res.msg = "结算成功！"
            res.data = slt_ser.data
        else:
            print(slt_ser.errors)

        return Response(res.dict)


class StatementView(APIView):
    def get(self, request, *args, **kwargs):
        filter_conditions = {}

        for k, v in request.query_params.items():
            if "page" in k.lower():
                pass
            elif "date" in k.lower():
                t = int(v) / 1000

                date_time = datetime.datetime.fromtimestamp(t)
                filter_conditions["plan__" + k] = date_time

            else:
                filter_conditions["plan__" + k] = v
        query_set = Settlement.objects.filter(**filter_conditions) \
            .values("plan__media__name", "plan__media__pk") \
            .annotate(cost=Sum("cost"), start=Min("plan__launch_date"), end=Max("plan__launch_date"))

        # query_set = Settlement.objects.filter(**filter_conditions) \
        #     .values("plan__advertiser__name", "plan__advertiser__pk").annotate(cost=Sum("cost"))
        print("query_set", query_set.query)
        ser = StatementSerializer(query_set, many=True)
        # start_t = int(request.query_params.get("launch_date__gte")) / 1000
        # start_date_f = datetime.datetime.fromtimestamp(start_t).strftime("%Y-%m-%d")
        #
        # end_t = int(request.query_params.get("launch_date__lte")) / 1000
        # end_date_f = datetime.datetime.fromtimestamp(end_t).strftime("%Y-%m-%d")
        #
        # res_data = {
        #     "media": request.query_params.get("media"),
        #     "start_date_str": request.query_params.get("launch_date__gte"),
        #     "start_date": start_date_f,
        #     "end_date_str": request.query_params.get("launch_date__lte"),
        #     "end_date": end_date_f,
        #     "list": ser.data
        # }
        res = BaseResponse()
        res.msg = "媒体对账"
        res.data = ser.data
        return Response(res.dict)

    def post(self, request, *args, **kwargs):
        filter_conditions = {}
        check_data = request.data
        media_id = check_data.get("media")
        start_time = check_data.get("start_time")
        end_time = check_data.get("end_time")
        cost = check_data.get("cost")
        filter_conditions["plan__media"] = media_id
        filter_conditions["plan__launch_date__gte"] = start_time
        filter_conditions["plan__launch_date__lte"] = end_time
        Settlement.objects.filter(**filter_conditions).update(m_statement_status=1, m_checkout_time=now())
        res = BaseResponse()
        print(start_time, end_time)
        ser = MediaStatementSerializer(
            data={"media": media_id, "start_time": start_time + " 00:00:00", "end_time": end_time + " 00:00:00",
                  "cost": cost})
        if ser.is_valid():
            ser.save()
            res.msg = "媒体确认对账成功！"
            res.data = ser.data
        else:
            print(ser.errors)
        return Response(res.dict)


class MediaStatementsView(APIView):
    def get(self, request, *args, **kwargs):
        filter_conditions = {}
        for k, v in request.query_params.items():
            if v:
                filter_conditions[k] = v

        queryset = MediaStatement.objects.filter(**filter_conditions).order_by("-id")
        ser = MediaStatementSerializer(queryset, many=True)
        res = BaseResponse()
        res.msg = "获取历史账单成功！"
        res.data = ser.data
        return Response(res.dict)
