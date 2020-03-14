import time, datetime

from django.utils.timezone import now
from django.db.models import Count, Min, Max, Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from tgsAdmin.utils.response import BaseResponse
from tgsAdmin.models import AdvertStatement, Settlement

from tgsAdmin.serializer.statement import AdvertStatementSerializer


class AdvertStatementsView(APIView):
    def get(self, request, *args, **kwargs):
        filter_conditions = {}
        for k, v in request.query_params.items():
            if v:
                filter_conditions[k] = v
        print("filter_conditions",filter_conditions)
        queryset = AdvertStatement.objects.filter(**filter_conditions).order_by("-id")
        ser = AdvertStatementSerializer(queryset, many=True)
        res = BaseResponse()
        res.msg = "获取广告历史账单成功！"
        res.data = ser.data
        return Response(res.dict)

    def post(self, request, *args, **kwargs):
        filter_conditions = {}
        check_data = request.data
        advertiser_id = check_data.get("advertiser")
        start_time = check_data.get("start_time")
        end_time = check_data.get("end_time")
        cost = check_data.get("income")
        filter_conditions["plan__advertiser"] = advertiser_id
        filter_conditions["plan__launch_date__gte"] = start_time
        filter_conditions["plan__launch_date__lte"] = end_time
        Settlement.objects.filter(**filter_conditions).update(a_statement_status=1, a_checkout_time=now())
        res = BaseResponse()
        print(start_time, end_time)
        ser = AdvertStatementSerializer(
            data={"advertiser": advertiser_id, "start_time": start_time + " 00:00:00",
                  "end_time": end_time + " 00:00:00",
                  "income": cost})
        if ser.is_valid():
            ser.save()
            res.msg = "广告确认对账成功！"
            res.data = ser.data
        else:
            print(ser.errors)
        return Response(res.dict)
