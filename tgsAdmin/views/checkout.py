import time, datetime

from django.utils.timezone import now
from django.db.models import Count, Min, Max, Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from tgsAdmin.utils.response import BaseResponse
from tgsAdmin.models import Plan, Settlement, MediaStatement
from tgsAdmin.serializer.checkout import AdvertCheckoutSerializer


class AdvertCheckoutView(APIView):
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
        print("filter_conditions", filter_conditions)
        query_set = Settlement.objects.filter(**filter_conditions) \
            .values("plan__advertiser__name", "plan__advertiser__pk") \
            .annotate(income=Sum("income"), start=Min("plan__launch_date"), end=Max("plan__launch_date"))

        # query_set = Settlement.objects.filter(**filter_conditions) \
        #     .values("plan__advertiser__name", "plan__advertiser__pk").annotate(cost=Sum("cost"))
        print("query_set", query_set.query)
        ser = AdvertCheckoutSerializer(query_set, many=True)
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
        res.msg = "广告待对账"
        res.data = ser.data
        return Response(res.dict)


