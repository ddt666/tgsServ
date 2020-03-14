import time, datetime
import copy

from rest_framework.response import Response
from rest_framework.views import APIView

from tgsAdmin.utils.response import BaseResponse
from tgsAdmin.utils.pagination import MyPagination
from tgsAdmin.models import Plan, Settlement
from tgsAdmin.serializer.plan import PlanSerializer, SettlementSerializer
from tgsAdmin.utils.auth import LoginAuth
from tgsAdmin.utils.my_scheduler import scheduler
from tgsAdmin.utils.plan import update_plan_status


#
# class PlanView(APIView):
#     def post(self, request, *args, **kwargs):
#         res = BaseResponse()
#         t = request.data.get("launch_date") / 1000
#
#         launch_date_format = datetime.datetime.fromtimestamp(t)
#         print("launch_date_format", launch_date_format)
#
#         data = request.data
#
#         data["launch_date"] = launch_date_format
#         m_policy_data = request.data.get("media_price_policy")
#         print("m_policy_data", m_policy_data)
#         if m_policy_data:
#             m_policy_ser = MediaPricePolicySerializer(data=m_policy_data)
#             if m_policy_ser.is_valid():
#                 m_policy_obj = m_policy_ser.save()
#                 data["media_price_policy"] = m_policy_obj.pk
#                 print("m_policy_obj", m_policy_obj)
#
#         a_policy_data = request.data.get("ad_price_policy")
#         print("a_policy_data", a_policy_data)
#         if a_policy_data:
#             a_policy_ser = AdPricePolicySerializer(data=a_policy_data)
#             if a_policy_ser.is_valid():
#                 a_policy_obj = a_policy_ser.save()
#                 data["ad_price_policy"] = a_policy_obj.pk
#                 print("a_policy_obj", a_policy_obj)
#
#         print("data", data)
#         plan_ser = PlanSerializer(data=data)
#         if plan_ser.is_valid():
#             plan_ser.save()
#             res.msg = "创建计划成功"
#             res.data = plan_ser.data
#         else:
#             print(plan_ser.errors)
#             res.code = 1001
#             res.msg = str(plan_ser.errors)
#
#         return Response(res.dict)
#
#     def get(self, request, *args, **kwargs):
#         query_set = Plan.objects.all().order_by("-id")
#         plan_ser = PlanSerializer(query_set, many=True)
#         res = BaseResponse()
#         res.msg = "计划列表"
#         res.data = plan_ser.data
#
#         return Response(res.dict)
#
#
class PlanEditView(APIView):
    def get(self, request, *args, **kwargs):
        plan_id = kwargs.get("id")
        plan_obj = Plan.objects.filter(id=plan_id).first()
        plan_obj_ser = PlanSerializer(instance=plan_obj)

        res = BaseResponse()
        res.msg = "获取计划实例成功！"
        res.data = plan_obj_ser.data

        return Response(res.dict)

    def patch(self, request, *args, **kwargs):
        res = BaseResponse()
        plan_id = kwargs.get("id")
        receive = copy.deepcopy(request.data)

        settlement_data = receive.pop("settlement_info")

        plan_data = receive
        plan_data["launch_date"] = datetime.datetime.strptime(plan_data["launch_date"], "%Y-%m-%d")

        plan_obj = Plan.objects.filter(id=plan_id).first()

        settlement_obj = plan_obj.settlement
        settlement_ser = SettlementSerializer(instance=settlement_obj, data=settlement_data, partial=True)
        if settlement_ser.is_valid():

            plan_ser = PlanSerializer(instance=plan_obj, data=plan_data, partial=True)
            if plan_ser.is_valid():
                settlement_ser.save()
                plan_ser.save()
                res.msg = "修改计划成功"
                res.data = plan_ser.data
            else:
                res.msg = plan_ser.errors
                res.code = -1
        else:
            res.msg = settlement_ser.errors
            res.code = -1

        return Response(res.dict)


class PlanView(APIView):
    authentication_classes = [LoginAuth]

    def get(self, request, *args, **kwargs):
        print("query_params", request.query_params)
        filter_conditions = {}
        is_paging = True
        if request.query_params.get("noPage"):
            is_paging = False
        for k, v in request.query_params.items():
            if "page" in k.lower():

                pass
            elif "date" in k.lower():
                t = int(v) / 1000

                date_time = datetime.datetime.fromtimestamp(t)
                filter_conditions[k] = date_time

            else:
                filter_conditions[k] = v

        print("filter_conditions", filter_conditions)
        query_set = Plan.objects.filter(**filter_conditions).order_by("-id")
        # query_set = Plan.objects.all().order_by("-id")
        print("query_set.count()", query_set.count())
        if is_paging:
            paginator = MyPagination()
            query_set = paginator.paginate_queryset(query_set, request, view=None)
            count = paginator.page.paginator.count
        else:
            count = query_set.count()
        plan_ser = PlanSerializer(query_set, many=True)
        # print("plan_ser.data", plan_ser.data)
        data = {"count": count,
                "list": plan_ser.data
                }
        res = BaseResponse()
        res.msg = "获取计划列表成功"
        res.data = data

        return Response(res.dict)

    def post(self, request, *args, **kwargs):
        receive = copy.deepcopy(request.data)

        settlement_data = receive.pop("settlement_info")
        plan_data = receive
        print(request.data)

        # plan_data = request.data.get("plan")

        t = plan_data.get("launch_date_str") / 1000

        plan_data["launch_date"] = datetime.datetime.fromtimestamp(t)
        res = BaseResponse()
        p_obj = None
        if plan_data:
            print(plan_data)
            p_ser = PlanSerializer(data=plan_data)
            if p_ser.is_valid():
                p_obj = p_ser.save()


            else:
                print(p_ser.errors)

        if p_obj:

            # settlement_data = request.data.get("settlement")
            settlement_data["plan"] = p_obj.pk
            stl_ser = SettlementSerializer(data=settlement_data)
            if stl_ser.is_valid():
                stl_ser.save()
                res.msg = "计划创建成功！"
                res.data = stl_ser.data
            else:
                res.code = -1001
                res.msg = stl_ser.errors

        # MediaResult.objects.create(plan=p_obj)
        # AdResult.objects.create(plan=p_obj)

        # t = request.data.get("launch_date") / 1000
        #
        # launch_date_format = datetime.datetime.fromtimestamp(t)
        # print("launch_date_format", launch_date_format)
        #
        #
        #
        # data["launch_date"] = launch_date_format
        # m_policy_data = request.data.get("media_price_policy")
        # print("m_policy_data", m_policy_data)

        return Response(res.dict)


class PlanBatchView(APIView):

    def post(self, request, *args, **kwargs):
        res = BaseResponse()
        receive = request.data

        if "create" in receive:
            create_date = receive.get("create")
            print(create_date)
            date_range = create_date.get("launch_date_range")
            print("date_range", date_range)
            if not date_range:
                res.msg = "没有日期参数"
                return Response(res.dict)
            start_t = int(date_range[0]) / 1000
            start_date = datetime.datetime.fromtimestamp(start_t)
            end_t = int(date_range[1]) / 1000
            end_date = datetime.datetime.fromtimestamp(end_t)

            print(start_date, end_date)

            from tgsAdmin.utils.common import date_Range_list
            plan_obj_list = []
            settlement_data = create_date.pop("settlement_info")

            for date in date_Range_list(start_date, end_date, format="%Y-%m-%d %H:%M:%S"):
                print(date)
                plan_data = create_date.copy()
                plan_data["launch_date"] = date
                p_ser = PlanSerializer(data=plan_data)
                if p_ser.is_valid():
                    p_obj = p_ser.save()
                    plan_obj_list.append(p_obj)
                else:
                    res.msg = p_ser.errors
                    res.code = -1
                    return Response(res.dict)

            # print(plan_obj_list)
            settlement_list = []
            plan_pk_list = []
            # settlement_data = create_date.get("settlement").copy()
            for plan in plan_obj_list:
                settlement_list.append(Settlement(
                    m_unit_price=settlement_data.get("m_unit_price"),
                    plan_launch_count=settlement_data.get("plan_launch_count"),
                    a_unit_price=settlement_data.get("a_unit_price"),
                    plan=plan
                ))
                plan_pk_list.append(plan.pk)

            Settlement.objects.bulk_create(settlement_list)
            plan_query = Plan.objects.filter(id__in=plan_pk_list)
            plan_ser = PlanSerializer(plan_query, many=True)
            for p in plan_query:
                scheduler.add_job(update_plan_status, 'date',
                                  run_date=datetime.datetime.now() + datetime.timedelta(seconds=20),
                                  args=[p.pk], jobstore='redis', replace_existing=True)
            # scheduler.add_job(test_test, 'interval',
            #                   seconds=3, jobstore='redis', replace_existing=True)

            res.msg = "批量创建计划成功！"
            res.data = plan_ser.data
        return Response(res.dict)


def test_test():
    print(f"test_test")


from django.http import HttpResponse

from openpyxl import Workbook
from django.utils.encoding import escape_uri_path


def export_as_excel(request):
    print("request.GET", request.GET)
    # for k,v in request.GET.items():
    filter_condition = {}
    start_time = request.GET.get("start_time")
    if start_time:
        filter_condition["launch_date__gte"] = start_time
    end_time = request.GET.get("end_time")
    if end_time:
        filter_condition["launch_date__lte"] = end_time
    media_id = request.GET.get("media")
    if media_id:
        filter_condition["media"] = media_id
    statement_status = request.GET.get("m_statement_status")
    if statement_status:
        filter_condition["settlement__m_statement_status"] = statement_status

    if statement_status == "0":
        status_text = "未对账"
    else:
        status_text = "已对账"
    # filter_condition = {
    #     "media": media_id,
    #     "launch_date__gte": start_time,
    #     "launch_date__lte": end_time,
    #
    #     "settlement__m_statement_status": statement_status
    # }

    Plan.objects.filter(**filter_condition).values("launch_date", "media__name")
    fields = ["launch_date", "media__name", "m_location__title", "m_port__title", "settlement__m_exposure_count",
              "settlement__m_click_count", "settlement__m_click_rate", "m_charge_sort__title",
              "settlement__m_unit_price",
              "settlement__m_settlement_count", "settlement__cost", "advertiser__name"
              ]
    query_set = Plan.objects.filter(**filter_condition).extra(
        select={"launch_date": "DATE_FORMAT(launch_date, '%%Y/%%m/%%d')"}) \
        .values_list(*fields)

    print("query_set", query_set)
    fields_names = ["日期", "媒体", "位置", "端口", "曝光量", "点击", "点击率", "计费类型", "单价", "结算数", "成本",
                    "广告"]
    wb = Workbook()
    ws = wb.active
    ws.title = status_text
    ws.append(fields_names)
    for i in query_set:
        ws.append(i)
    file_name = "媒体明细(" + status_text + "_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".xlsx"
    response = HttpResponse(content_type='application/msexcel')  # 定义响应内容类型
    # response['Content-Disposition'] = f'attachment; filename=媒体.xlsx'  # 定义响应数据格式
    # response['Content-Disposition'] = 'attachment; filename=' + filename.encode('utf-8').decode('ISO-8859-1')
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file_name))  # 定义响应数据格式
    print("response", response)
    wb.save(response)  # 将数据存入响应内容
    return response


def export_advert_statement(request):
    print("request.GET", request.GET)
    # for k,v in request.GET.items():
    filter_condition = {}
    start_time = request.GET.get("start_time")
    if start_time:
        filter_condition["launch_date__gte"] = start_time
    end_time = request.GET.get("end_time")
    if end_time:
        filter_condition["launch_date__lte"] = end_time
    advertiser_id = request.GET.get("advertiser")
    if advertiser_id:
        filter_condition["advertiser"] = advertiser_id
    statement_status = request.GET.get("a_statement_status")

    if statement_status:
        filter_condition["settlement__a_statement_status"] = statement_status

    if statement_status == "0":
        status_text = "未对账"
    else:
        status_text = "已对账"
    # filter_condition = {
    #     "media": media_id,
    #     "launch_date__gte": start_time,
    #     "launch_date__lte": end_time,
    #
    #     "settlement__m_statement_status": statement_status
    # }
    print("filter_condition", filter_condition)
    Plan.objects.filter(**filter_condition).values("launch_date", "media__name")
    fields = ["launch_date", "advertiser__name", "ad_url", "settlement__a_exposure_count",
              "settlement__a_click_count", "settlement__a_click_rate", "a_charge_sort__title",
              "settlement__a_unit_price",
              "settlement__a_settlement_count", "settlement__income", "media__name"
              ]
    query_set = Plan.objects.filter(**filter_condition).extra(
        select={"launch_date": "DATE_FORMAT(launch_date, '%%Y/%%m/%%d')"}) \
        .values_list(*fields)

    print("query_set", query_set)
    fields_names = ["日期", "广告", "链接", "曝光量", "点击", "点击率", "计费类型", "单价", "结算数", "收费",
                    "媒体"]
    wb = Workbook()
    ws = wb.active
    ws.title = status_text
    ws.append(fields_names)
    for i in query_set:
        ws.append(i)
    file_name = "广告明细(" + status_text + ")_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".xlsx"
    response = HttpResponse(content_type='application/msexcel')  # 定义响应内容类型
    # response['Content-Disposition'] = f'attachment; filename=媒体.xlsx'  # 定义响应数据格式
    # response['Content-Disposition'] = 'attachment; filename=' + filename.encode('utf-8').decode('ISO-8859-1')
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file_name))  # 定义响应数据格式
    print("response", response)
    wb.save(response)  # 将数据存入响应内容
    return response
