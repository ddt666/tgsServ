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
    title = models.CharField(verbose_name="名称", max_length=32, null=True, blank=True)
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
class Customer(models.Model):
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
        verbose_name_plural = "广告表"
        verbose_name = "广告表"
        # unique_together = ("name", "agent")


# 业务####################################################################################################

class Plan(models.Model):
    launch_date = models.DateTimeField(verbose_name="投放日期", null=True, blank=True)
    media = models.ForeignKey(to="Media", verbose_name="媒体")
    m_location = models.ForeignKey(to="AdLocation", verbose_name="位置", on_delete=models.CASCADE, null=True)
    m_port = models.ForeignKey(to="Port", verbose_name="端口", on_delete=models.CASCADE, null=True)
    m_charge_sort = models.ForeignKey(to="ChargeSort", related_name="plan", verbose_name="媒体计费类型",
                                      on_delete=models.CASCADE, null=True)

    customer = models.ForeignKey(to="Customer", verbose_name="客户")

    ad_url = models.CharField(verbose_name="广告链接", max_length=1024, null=True, blank=True)
    ad_charge_sort = models.ForeignKey(to="ChargeSort", verbose_name="广告计费类型", on_delete=models.CASCADE)

    # media_price_policy = models.OneToOneField(to="MediaPricePolicy", verbose_name="媒体计价策略", on_delete=models.CASCADE)

    # ad_price_policy = models.OneToOneField(to="AdPricePolicy", verbose_name="广告计价策略", on_delete=models.CASCADE)

    status_choice = (
        (0, "待结算"),
        (1, "结算完成")
    )

    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name="状态")

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.launch_date} - {self.media} - {self.customer} "

    # def save(self, *args, **kwargs):
    #     if self.media_price_policy.unit_price and self.plan_launch_count:
    #         self.budget = round(self.media_price_policy.unit_price * self.plan_launch_count, 3)
    #     super(Plan, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "计划表"
        verbose_name = "计划表"


class Settlement(models.Model):
    plan = models.OneToOneField(to="Plan", verbose_name="计划", on_delete=models.CASCADE)

    media_unit_price = models.FloatField(verbose_name="媒体广告位单价", null=True, blank=True)
    ad_unit_price = models.FloatField(verbose_name="客户单价", null=True, blank=True)
    plan_launch_count = models.BigIntegerField(verbose_name="预计投放量", null=True, blank=True)
    budget = models.BigIntegerField(verbose_name="预计成本", null=True, blank=True)
    settlement_count = models.BigIntegerField(verbose_name="结算数", null=True, blank=True)
    cost = models.FloatField(verbose_name="实际成本", null=True, blank=True)
    income = models.FloatField(verbose_name="收入", null=True, blank=True)
    profit = models.FloatField(verbose_name="利润", null=True, blank=True)
    settlement_time = models.DateTimeField(verbose_name="结算时间", null=True, blank=True)

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.plan} - 利润:{self.profit}"

    # def save(self, *args, **kwargs):
    #
    #     if self.media_price_policy.unit_price and self.plan_launch_count:
    #         self.budget = round(self.media_price_policy.unit_price * self.plan_launch_count, 3)
    #     super(Plan, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "结算表"
        verbose_name = "结算表"


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


class MediaResult(models.Model):
    plan = models.OneToOneField(to="Plan", verbose_name="计划", on_delete=models.CASCADE)
    exposure_count = models.BigIntegerField(verbose_name="曝光量", null=True, blank=True)
    click_count = models.BigIntegerField(verbose_name="点击量", null=True, blank=True)

    click_rate = models.FloatField(verbose_name="点击率", null=True, blank=True)

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.plan} 媒体的数据"

    class Meta:
        verbose_name_plural = "媒体效果数据表"
        verbose_name = "媒体效果数据表"


class AdResult(models.Model):
    plan = models.OneToOneField(to="Plan", verbose_name="计划", on_delete=models.CASCADE)
    exposure_count = models.BigIntegerField(verbose_name="曝光量", null=True, blank=True)
    click_count = models.BigIntegerField(verbose_name="点击量", null=True, blank=True)

    click_rate = models.FloatField(verbose_name="点击率", null=True, blank=True)

    week_rate = models.FloatField(verbose_name="七日唤醒率", null=True, blank=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    # def click_rate(self):
    #     if self.exposure_count and self.exposure_count > 0:
    #         return round(self.click_count / self.exposure_count, 4)
    #     else:
    #         return None
    #
    # click_rate.short_description = '点击率'
    def __str__(self):
        return f"{self.plan} 客户的数据 "

    class Meta:
        verbose_name_plural = "客户效果数据表"
        verbose_name = "客户效果数据表"

# ###############################################################################################
