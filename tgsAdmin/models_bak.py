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


# 媒体广告位
class AdSlot(models.Model):
    media = models.ForeignKey(to="Media", verbose_name="媒体", on_delete=models.CASCADE)
    port = models.ForeignKey(to="Port", verbose_name="端口", on_delete=models.CASCADE)
    location = models.ForeignKey(to="AdLocation", verbose_name="位置", on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.media.name} - {self.port.title} - {self.location.title}"

    class Meta:
        verbose_name_plural = "广告位表"
        verbose_name = "广告位表"


# 媒体计费策略
class MediaPricePolicy(models.Model):
    ad_slot = models.ForeignKey(to="AdSlot", verbose_name="广告位", on_delete=models.CASCADE)
    charge_sort = models.ForeignKey(to="ChargeSort", verbose_name="计费类型", on_delete=models.CASCADE)

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.ad_slot} - {self.charge_sort.title}"

    class Meta:
        verbose_name_plural = "媒体计费策略表"
        verbose_name = "媒体计费策略表"


#  客户（广告）######################################################################################################


# 广告
class Advertising(models.Model):
    name = models.CharField(verbose_name="广告名称", max_length=32)
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


# 广告计费策略
class AdPricePolicy(models.Model):
    advert = models.ForeignKey(to="Advertising", verbose_name="广告", on_delete=models.CASCADE)
    charge_sort = models.ForeignKey(to="ChargeSort", verbose_name="计费类型", on_delete=models.CASCADE)

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.advert} - {self.charge_sort.title} "

    class Meta:
        verbose_name_plural = "广告计费策略表"
        verbose_name = "广告计费策略表"


# 业务####################################################################################################

class Service(models.Model):
    media = models.ForeignKey(to="MediaPricePolicy", verbose_name="媒体", on_delete=models.CASCADE)
    m_unit_price = models.FloatField(verbose_name="媒体单价", default=0)

    advert = models.ForeignKey(to="AdPricePolicy", verbose_name="广告", on_delete=models.CASCADE)
    a_unit_price = models.FloatField(verbose_name="广告单价", default=0)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.media} - 单价:{self.m_unit_price}  | {self.advert} - 单价:{self.a_unit_price}"

    class Meta:
        verbose_name_plural = "业务关联表"
        verbose_name = "业务关联表"


class ServiceDetail(models.Model):
    service = models.ForeignKey(to="Service", verbose_name="投放计划", on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="投放日期", null=True, blank=True)

    # 结算依据
    settlement_sort_choice = (
        (0, "媒体"),
        (1, "客户"),
        (2, "自定义"),
    )
    settlement_sort = models.SmallIntegerField(choices=settlement_sort_choice, verbose_name="结算依据", default=0)
    plan_count = models.BigIntegerField(verbose_name="预计投放量", null=True, blank=True)
    media_data = models.OneToOneField(to="MediaData", verbose_name="媒体数据", null=True, blank=True,
                                      on_delete=models.CASCADE)
    ad_data = models.OneToOneField(to="AdData", verbose_name="客户数据", null=True, blank=True, on_delete=models.CASCADE)
    settlement_count = models.BigIntegerField(verbose_name="结算数", null=True, blank=True)

    budget = models.BigIntegerField(verbose_name="预计成本", null=True, blank=True)
    cost = models.FloatField(verbose_name="成本", null=True, blank=True)
    income = models.FloatField(verbose_name="收入", null=True, blank=True)
    profit = models.FloatField(verbose_name="利润", null=True, blank=True)

    settlement_status_choice = (
        (0, "待结算"),
        (1, "媒体结算完成,客户未结算"),
        (2, "客户结算完成,媒体未结算"),
        (3, "结算完成")
    )

    settlement_status = models.SmallIntegerField(choices=settlement_status_choice, default=0, verbose_name="结算状态")

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.service} "

    class Meta:
        verbose_name_plural = "业务详细表"
        verbose_name = "业务详细表"


class Plan(models.Model):
    date = models.DateTimeField(verbose_name="投放日期", null=True, blank=True)

    media = models.ForeignKey(to="Media", verbose_name="媒体", on_delete=models.CASCADE)
    location = models.ForeignKey(to="AdLocation", verbose_name="位置", on_delete=models.CASCADE)
    port = models.ForeignKey(to="Port", verbose_name="端口", on_delete=models.CASCADE)
    m_charge_sort = models.ForeignKey(to="ChargeSort", verbose_name="媒体计费类型", on_delete=models.CASCADE)
    m_unit_price = models.FloatField(verbose_name="媒体单价", default=0)
    plan_count = models.BigIntegerField(verbose_name="预计投放量", null=True, blank=True)
    budget = models.BigIntegerField(verbose_name="预计成本", null=True, blank=True)

    advert = models.ForeignKey(to="Advertising", verbose_name="广告", on_delete=models.CASCADE)
    ad_url = models.CharField(verbose_name="广告链接", null=True, blank=True)
    a_charge_sort = models.ForeignKey(to="ChargeSort", verbose_name="客户计费类型", on_delete=models.CASCADE)
    a_unit_price = models.FloatField(verbose_name="广告单价", default=0)

    # 结算依据
    settlement_sort_choice = (
        (0, "媒体"),
        (1, "客户"),
        (2, "自定义"),
    )
    settlement_sort = models.SmallIntegerField(choices=settlement_sort_choice, verbose_name="结算依据", default=0)

    media_data = models.OneToOneField(to="MediaData", verbose_name="媒体数据", null=True, blank=True,
                                      on_delete=models.CASCADE)
    ad_data = models.OneToOneField(to="AdData", verbose_name="客户数据", null=True, blank=True, on_delete=models.CASCADE)
    settlement_count = models.BigIntegerField(verbose_name="结算数", null=True, blank=True)

    cost = models.FloatField(verbose_name="实际成本", null=True, blank=True)
    income = models.FloatField(verbose_name="收入", null=True, blank=True)
    profit = models.FloatField(verbose_name="利润", null=True, blank=True)

    settlement_status_choice = (
        (0, "待结算"),
        (1, "媒体结算完成,客户未结算"),
        (2, "客户结算完成,媒体未结算"),
        (3, "结算完成")
    )

    settlement_status = models.SmallIntegerField(choices=settlement_status_choice, default=0, verbose_name="结算状态")

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.media} - {self.advert} "

    class Meta:
        verbose_name_plural = "业务详细表"
        verbose_name = "业务详细表"


class MediaData(models.Model):
    exposure_count = models.BigIntegerField(verbose_name="曝光量", null=True, blank=True)
    click_count = models.BigIntegerField(verbose_name="点击量", null=True, blank=True)

    click_rate = models.FloatField(verbose_name="点击率", null=True, blank=True)

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.exposure_count} - {self.click_count} -{self.created}"

    class Meta:
        verbose_name_plural = "媒体数据表"
        verbose_name = "媒体数据表"


class AdData(models.Model):
    exposure_count = models.BigIntegerField(verbose_name="曝光量", null=True, blank=True)
    click_count = models.BigIntegerField(verbose_name="点击量", null=True, blank=True)
    week_rate = models.FloatField(verbose_name="七日唤醒率", null=True, blank=True)

    click_rate = models.FloatField(verbose_name="点击率", null=True, blank=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    # def click_rate(self):
    #     if self.exposure_count and self.exposure_count > 0:
    #         return round(self.click_count / self.exposure_count, 4)
    #     else:
    #         return None
    #
    # click_rate.short_description = '点击率'
    def __str__(self):
        return f"{self.exposure_count} - {self.click_count} -{self.created}"

    class Meta:
        verbose_name_plural = "广告数据表"
        verbose_name = "广告数据表"

# ###############################################################################################
