from django.db import models


# Create your models here.

class AdData(models.Model):
    exposure_count = models.BigIntegerField(verbose_name="曝光量", null=True, blank=True)
    click_count = models.BigIntegerField(verbose_name="点击量", null=True, blank=True)
    # click_rate = models.FloatField(verbose_name="点击率", null=True, blank=True)
    week_rate = models.FloatField(verbose_name="七日唤醒率", null=True, blank=True)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def click_rate(self):
        if self.exposure_count and self.exposure_count > 0:
            return round(self.click_count / self.exposure_count, 4)
        else:
            return None

    click_rate.short_description = '点击率'

    class Meta:
        verbose_name_plural = "广告数据表"
        verbose_name = "广告数据表"
