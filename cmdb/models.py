from django.db import models


# Create your models here.
class UserInfo(models.Model):
    Role_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="角色名称")
    Foster_time = models.CharField(max_length=200, verbose_name="寄养时间")
    user = models.CharField(max_length=200, null=True, blank=True, verbose_name="账号")
    pwd = models.CharField(max_length=200, null=True, blank=True, verbose_name="密码")
    District_Service = models.CharField(max_length=200, null=True, blank=True, verbose_name="区服")
    type = models.CharField(max_length=200, null=True, blank=True, verbose_name="类型")
    Target_boundary = models.CharField(max_length=200, null=True, blank=True,verbose_name="目标结界")
    u_id = models.CharField(max_length=200, null=True, blank=True, verbose_name="角色id")
    simulator = models.CharField(max_length=200, null=True, blank=True, verbose_name="模拟器")
    mode = models.CharField(max_length=200, null=True, blank=True, verbose_name="上号方式")
    time1 = models.CharField(max_length=200, null=True, blank=True, verbose_name="限制时间")
    time2 = models.CharField(max_length=200, null=True, blank=True, verbose_name="到期时间")
    Pit_type= models.CharField(max_length=200, null=True, blank=True, verbose_name="坑型")

