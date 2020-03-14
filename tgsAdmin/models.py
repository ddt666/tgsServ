from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Create your models here.


class UserInfo(AbstractUser):
    username = models.CharField(verbose_name="用户账号", max_length=32, unique=True, help_text="填写用户名")
    password = models.CharField(_("密码"), max_length=128)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.username


class Token(models.Model):
    key = models.CharField(max_length=40)
    user = models.OneToOneField("UserInfo", related_name='auth_token',
                                verbose_name="关联用户", on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


# 计费类型
class ChargeSort(models.Model):
    title = models.CharField(verbose_name="名称", max_length=32, null=True, blank=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "计费类型表"
        verbose_name = "计费类型表"


# 媒体#######################################################################################################
# 媒体
class Media(models.Model):
    name = models.CharField(verbose_name="媒体名称", max_length=32)
    agent = models.CharField(verbose_name="代理商", max_length=32, null=True, blank=True)

    sort_choice = (
        (0, "直媒"),
        (1, "代媒")
    )
    sort = models.SmallIntegerField(verbose_name="媒体类型", choices=sort_choice, default=0)

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        if self.agent:
            return f"{self.name} - {self.agent}"
        else:
            return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.sort == 1:
            if not self.agent:
                raise ValueError("代媒类型必须填写代理商")
        super(Media, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "媒体表"
        verbose_name = "媒体表"

        ordering = ("-id",)


# 广告位置
class AdLocation(models.Model):
    title = models.CharField(verbose_name="名称s", max_length=32, null=True, blank=True, unique=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "广告位置表"
        verbose_name = "广告位置表"


# 广告端口
class Port(models.Model):
    title = models.CharField(verbose_name="名称", max_length=32, null=True, blank=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "广告端口表"
        verbose_name_plural = "广告端口表"


#  客户（广告）######################################################################################################


# 广告主 客户
class Advertiser(models.Model):
    name = models.CharField(verbose_name="客户名称", max_length=32)
    agent = models.CharField(verbose_name="代理商", max_length=32, null=True, blank=True)
    sort_choice = (
        (0, "直客"),
        (1, "代客")
    )
    sort = models.SmallIntegerField(verbose_name="客户类型", choices=sort_choice, default=0)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        if self.agent:
            return f"{self.name} - {self.agent}"
        else:
            return f"{self.name}"

    class Meta:
        verbose_name_plural = "客户表"
        verbose_name = "客户表"
        # unique_together = ("name", "agent")


# 业务####################################################################################################

class Plan(models.Model):
    launch_date = models.DateTimeField(verbose_name="投放日期", null=True, blank=True)
    media = models.ForeignKey(to="Media", verbose_name="媒体", on_delete=models.CASCADE)
    m_location = models.ForeignKey(to="AdLocation", verbose_name="位置", on_delete=models.CASCADE, null=True)
    m_port = models.ForeignKey(to="Port", verbose_name="端口", on_delete=models.CASCADE, null=True)
    m_charge_sort = models.ForeignKey(to="ChargeSort", related_name="m_sort2plan", verbose_name="媒体计费类型",
                                      on_delete=models.CASCADE, null=True)

    advertiser = models.ForeignKey(to="Advertiser", verbose_name="客户", on_delete=models.CASCADE)

    ad_url = models.CharField(verbose_name="广告链接", max_length=1024, null=True, blank=True)
    a_charge_sort = models.ForeignKey(to="ChargeSort", verbose_name="广告计费类型", related_name="ad_sort2plan",
                                      on_delete=models.CASCADE)
    # settlement = models.OneToOneField(to="Settlement", verbose_name="结算", null=True, blank=True,
    #                                   on_delete=models.CASCADE)
    #
    # media_result = models.OneToOneField(to="MediaResult", verbose_name="媒体效果数据", null=True, blank=True,
    #                                     on_delete=models.CASCADE)
    # advert_result = models.OneToOneField(to="AdResult", verbose_name="广告效果数据", null=True, blank=True,
    #                                      on_delete=models.CASCADE)

    # media_price_policy = models.OneToOneField(to="MediaPricePolicy", verbose_name="媒体计价策略", on_delete=models.CASCADE)

    # ad_price_policy = models.OneToOneField(to="AdPricePolicy", verbose_name="广告计价策略", on_delete=models.CASCADE)
    remark = models.TextField(verbose_name="备注", null=True, blank=True)
    status_choice = (
        (0, "未执行"),
        (1, "执行中"),
        (2, "已完成"),
    )

    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name="状态")

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.launch_date}  |  {self.media}  |  {self.advertiser} "

    # def save(self, *args, **kwargs):
    #     if self.media_price_policy.unit_price and self.plan_launch_count:
    #         self.budget = round(self.media_price_policy.unit_price * self.plan_launch_count, 3)
    #     super(Plan, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "计划表"
        verbose_name = "计划表"


class Settlement(models.Model):
    plan = models.OneToOneField(to="Plan", verbose_name="计划", on_delete=models.CASCADE)
    m_unit_price = models.FloatField(verbose_name="媒体广告位单价", null=True, blank=True)
    a_unit_price = models.FloatField(verbose_name="广告单价", null=True, blank=True)

    plan_launch_count = models.BigIntegerField(verbose_name="预计投放量", null=True, blank=True)
    budget = models.BigIntegerField(verbose_name="预计成本", null=True, blank=True)

    m_exposure_count = models.BigIntegerField(verbose_name="媒体-曝光量", null=True, blank=True)
    m_click_count = models.BigIntegerField(verbose_name="媒体-点击量", null=True, blank=True)

    m_click_rate = models.FloatField(verbose_name="媒体-点击率", null=True, blank=True)
    m_settlement_count = models.BigIntegerField(verbose_name="媒体-结算数", null=True, blank=True)
    statement_status_choice = (
        (0, "未对账"),
        (1, "已对账"),
    )
    m_statement_status = models.SmallIntegerField(choices=statement_status_choice, verbose_name="媒体对账状态", default=0)
    m_checkout_time = models.DateTimeField(verbose_name="媒体对账时间", null=True, blank=True)

    a_exposure_count = models.BigIntegerField(verbose_name="客户-曝光量", null=True, blank=True)
    a_click_count = models.BigIntegerField(verbose_name="客户-点击量", null=True, blank=True)
    a_click_rate = models.FloatField(verbose_name="客户-点击率", null=True, blank=True)
    a_week_rate = models.FloatField(verbose_name="客户-七日唤醒率", null=True, blank=True)
    a_settlement_count = models.BigIntegerField(verbose_name="客户-结算数", null=True, blank=True)
    a_statement_status = models.SmallIntegerField(choices=statement_status_choice, verbose_name="客户对账状态", default=0)
    a_checkout_time = models.DateTimeField(verbose_name="客户对账时间", null=True, blank=True)

    cost = models.FloatField(verbose_name="实际成本", null=True, blank=True)
    income = models.FloatField(verbose_name="收入", null=True, blank=True)
    profit = models.FloatField(verbose_name="利润", null=True, blank=True)

    def status(self):

        if self.m_statement_status == 1 and self.a_statement_status == 1:
            return 1
        else:
            return 0

    status.short_description = "计划对账状态(0：未完成，1：全部完成)"
    # status_choice = (
    #     (0, "待结算"),
    #     (1, "完成")
    # )
    #
    # status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name="状态")
    # # settlement_time = models.DateTimeField(verbose_name="结算时间", null=True, blank=True)

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.plan} - 利润:{self.profit}"

    def save(self, *args, **kwargs):

        if self.m_exposure_count and self.m_click_count:
            self.m_click_rate = round(self.m_click_count / self.m_exposure_count, 4)

        if self.a_exposure_count and self.a_click_count:
            self.a_click_rate = round(self.a_click_count / self.a_exposure_count, 4)
        if self.m_unit_price and self.plan_launch_count:
            self.budget = round(self.m_unit_price * self.plan_launch_count, 3)

        if self.m_settlement_count and self.m_unit_price:
            self.cost = round(self.m_settlement_count * self.m_unit_price, 3)

        if self.a_settlement_count and self.a_unit_price:
            self.income = round(self.a_settlement_count * self.a_unit_price, 3)

        if self.cost and self.income:
            self.profit = round(self.income - self.cost, 3)
        # if self.m_statement_status == 1 and self.a_statement_status == 1:
        #     self.status = 1

        super(Settlement, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "结算表"
        verbose_name = "结算表"


class MediaStatement(models.Model):
    media = models.ForeignKey(to="Media", verbose_name="媒体", on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="截至时间")
    cost = models.FloatField(verbose_name="成本")
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name_plural = "媒体对账表"
        verbose_name = "媒体对账表"


class AdvertStatement(models.Model):
    advertiser = models.ForeignKey(to="Advertiser", verbose_name="广告", on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="截至时间")
    income = models.FloatField(verbose_name="收入")
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name_plural = "客户对账表"
        verbose_name = "客户对账表"

# class
# class PlanDetail(models.Model):
#     plan = models.OneToOneField(to="Plan", verbose_name="计划", on_delete=models.CASCADE)
#
#
#
#     created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.plan} 的数据 "
#
#     class Meta:
#         verbose_name_plural = "计划详细表"
#         verbose_name = "计划详细表"


# class MediaResult(models.Model):
#     plan = models.OneToOneField(to="Plan", verbose_name="计划", on_delete=models.CASCADE)
#     exposure_count = models.BigIntegerField(verbose_name="曝光量", null=True, blank=True)
#     click_count = models.BigIntegerField(verbose_name="点击量", null=True, blank=True)
#
#     click_rate = models.FloatField(verbose_name="点击率", null=True, blank=True)
#     input_time = models.DateTimeField(verbose_name="录入时间", null=True, blank=True)
#     created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.plan} 媒体的数据"
#
#     class Meta:
#         verbose_name_plural = "媒体效果数据表"
#         verbose_name = "媒体效果数据表"
#
#
# class AdResult(models.Model):
#     plan = models.OneToOneField(to="Plan", verbose_name="计划", on_delete=models.CASCADE)
#     exposure_count = models.BigIntegerField(verbose_name="曝光量", null=True, blank=True)
#     click_count = models.BigIntegerField(verbose_name="点击量", null=True, blank=True)
#     click_rate = models.FloatField(verbose_name="点击率", null=True, blank=True)
#     week_rate = models.FloatField(verbose_name="七日唤醒率", null=True, blank=True)
#     input_time = models.DateTimeField(verbose_name="录入时间", null=True, blank=True)
#
#     created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#
#     # def click_rate(self):
#     #     if self.exposure_count and self.exposure_count > 0:
#     #         return round(self.click_count / self.exposure_count, 4)
#     #     else:
#     #         return None
#     #
#     # click_rate.short_description = '点击率'
#     def __str__(self):
#         return f"{self.plan} 客户的数据 "
#
#     class Meta:
#         verbose_name_plural = "客户效果数据表"
#         verbose_name = "客户效果数据表"

# ###############################################################################################
