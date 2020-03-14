from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.forms import widgets
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Create your models here.


# class UserInfo(AbstractUser):
#     username = models.CharField(verbose_name="用户账号", max_length=32, unique=True, help_text="填写用户名")
#     password = models.CharField(_("密码"), max_length=128)
#     created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#
#     class Meta:
#         verbose_name = "用户表"
#         verbose_name_plural = "用户表"
#
#     def __str__(self):
#         return self.username


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
        unique_together = ("name", "agent")
        ordering = ("-id",)


# # 客户
# class Customer(models.Model):
#     name = models.CharField(verbose_name="客户名称", max_length=32)
#     agent = models.CharField(verbose_name="代理商", max_length=32, null=True, blank=True)
#     sort_choice = (
#         (0, "直客"),
#         (1, "代客")
#     )
#     sort = models.SmallIntegerField(choices=sort_choice, default=0)
#     created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.name} - {self.agent}"
#
#     class Meta:
#         verbose_name_plural = "客户表"
#         verbose_name = "客户表"
#         unique_together = ("name", "agent")


# 广告
class advertiser(models.Model):
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
        unique_together = ("name", "agent")


# 计费类型
class ChargeSort(models.Model):
    title = models.CharField(verbose_name="类型", max_length=32, null=True, blank=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "计费类型表"
        verbose_name = "计费类型表"


# 广告位置
class AdLocation(models.Model):
    title = models.CharField(verbose_name="位置", max_length=32, null=True, blank=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "广告位置表"
        verbose_name = "广告位置表"


class MediaPlan(models.Model):
    media = models.ForeignKey("Media", verbose_name="媒体", related_name="med2mp", on_delete=models.CASCADE)
    location = models.ForeignKey("AdLocation", verbose_name="位置", related_name="loc2plan", on_delete=models.CASCADE)

    img_file = models.ImageField(verbose_name="图片素材", upload_to="photos/%Y/%m/%d", null=True, blank=True)
    port_choice = (
        (0, "微信"),
        (1, "支付宝"),
        (2, "其他"),
    )
    port = models.SmallIntegerField(verbose_name="端口", choices=port_choice, default=0)
    target_number = models.BigIntegerField(verbose_name="目标数量", null=True, blank=True)

    charge_sort = models.ForeignKey("ChargeSort", verbose_name="计费类型", on_delete=models.CASCADE)
    unit_price = models.FloatField(verbose_name="单价", null=True, blank=True)

    status_choices = (
        (0, "待结算"),
        (1, "已结算")
    )
    status = models.SmallIntegerField(verbose_name="结算状态", choices=status_choices, default=0)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.media} | {self.get_port_display()} | {self.charge_sort} | {self.location} |{self.unit_price}"

    class Meta:
        verbose_name_plural = "媒体计划表"
        verbose_name = "媒体计划表"


class MediaData(models.Model):
    media_plan = models.OneToOneField("MediaPlan", verbose_name="媒体计划", on_delete=models.CASCADE)
    exposure_number = models.BigIntegerField(verbose_name="曝光量", null=True, blank=True)
    click_number = models.BigIntegerField(verbose_name="点击量", null=True, blank=True)
    click_rate = models.FloatField(verbose_name="点击率", null=True, blank=True)
    settlement_num = models.BigIntegerField(verbose_name="结算数", null=True, blank=True)
    cost = models.FloatField(verbose_name="成本", null=True, blank=True)

    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.click_number and self.exposure_number:
            if self.exposure_number > 0:
                self.click_rate = round(self.click_number / self.exposure_number, 4)
        else:
            raise ValueError("填数出错")

        if self.media_plan.unit_price and self.settlement_num:
            self.cost = round(self.media_plan.unit_price * self.settlement_num, 3)

        super(MediaData, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "媒体结算表"
        verbose_name = "媒体结算表"


class AdPlan(models.Model):
    ad = models.ForeignKey("Advertising", verbose_name="广告", related_name="ad2ap", on_delete=models.CASCADE)
    charge_sort = models.ForeignKey("ChargeSort", verbose_name="计费类型", on_delete=models.CASCADE)
    unit_price = models.FloatField(verbose_name="单价", null=True, blank=True)
    status_choices = (
        (0, "待结算"),
        (1, "已结算")
    )
    status = models.SmallIntegerField(verbose_name="结算状态", choices=status_choices, default=0)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.ad.name} | {self.charge_sort} | {self.unit_price} "

    class Meta:
        verbose_name_plural = "广告计划表"
        verbose_name = "广告计划表"


class AdData(models.Model):
    ad_plan = models.OneToOneField("AdPlan", verbose_name="广告计划", on_delete=models.CASCADE)
    exposure_number = models.BigIntegerField(verbose_name="曝光量", null=True, blank=True)
    click_number = models.BigIntegerField(verbose_name="点击量", null=True, blank=True)
    settlement_num = models.BigIntegerField(verbose_name="结算数", null=True, blank=True)
    click_rate = models.FloatField(verbose_name="点击率", null=True, blank=True)
    income = models.FloatField(verbose_name="收入", null=True, blank=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.click_number and self.exposure_number:
            if self.exposure_number > 0:
                self.click_rate = round(self.click_number / self.exposure_number, 4)
        else:
            raise ValueError("填数出错")

        if self.ad_plan.unit_price and self.settlement_num:
            self.income = round(self.ad_plan.unit_price * self.settlement_num, 3)

        super(AdData, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "广告结算表"
        verbose_name = "广告结算表"


class AdService(models.Model):
    media_plan = models.ForeignKey("MediaPlan", verbose_name="媒体", on_delete=models.CASCADE)
    ad_plan = models.ForeignKey("AdPlan", verbose_name="广告", on_delete=models.CASCADE)
    status_choice = (
        (0, "待结算"),
        (1, "已完成"),
    )

    serv_date = models.DateTimeField(verbose_name="投放时间", null=True, blank=True)

    status = models.SmallIntegerField(verbose_name="投放状态", choices=status_choice, default=0)
    profit = models.FloatField(verbose_name="利润", null=True, blank=True)
    settlement_time = models.DateTimeField(verbose_name="结算时间", null=True, blank=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.media_plan.media} | {self.ad_plan.ad} | {self.created}"

    def save(self, *args, **kwargs):
        if self.status == 1:
            if self.media_plan.mediadata.cost and self.ad_plan.addata.income:
                self.profit = round(self.ad_plan.addata.income - self.media_plan.mediadata.cost,3)
        super(AdService, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "投放计划表"
        verbose_name = "投放计划表"
