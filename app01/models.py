from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


# 用户表
class UserInfo(AbstractUser):
    phone = models.CharField(max_length=11, verbose_name='手机号', null=True, blank=True)
    ''' 
    null:  数据库可以为空
    blank: django 后台可以为空
    '''
    avatar = models.FileField(upload_to='avatar/', default='avatar/default.jpg', verbose_name='用户头像')
    ''' 
        用户上传头像则保存在avatar文件夹，否则放一个默认头像
    '''

    class Meta:
        verbose_name_plural = '用户表'
    #
    # def __str__(self):
    #     return self.username


# 工厂表
class Factory(models.Model):
    name = models.CharField(verbose_name='厂名', max_length=50)
    addr = models.CharField(verbose_name='厂址', max_length=50)
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(verbose_name='联系方式', max_length=11)

    class Meta:
        verbose_name_plural = '工厂表'

    def __str__(self):
        return self.name


# 货物表
class Commodity(models.Model):
    name = models.CharField(verbose_name='商品名', max_length=30)
    count = models.BigIntegerField(verbose_name='库存量')
    type = models.CharField(verbose_name='规格', max_length=30)
    standard = models.CharField(verbose_name='型号', max_length=30)
    # through_fields写的是第三章表的字段
    factory = models.ManyToManyField(to='Factory',through='F2C',through_fields=('commodity', 'factory'))

    class Meta:
        verbose_name_plural = '货物表'

    # def __str__(self):
    #     return self.name


class F2C(models.Model):
    commodity = models.ForeignKey(to='Commodity', verbose_name='商品名')
    factory = models.ForeignKey(to='Factory', verbose_name='厂名')


# 流动信息表
class Message(models.Model):
    count = models.BigIntegerField(verbose_name='流动数量')
    date = models.DateField(verbose_name='变动日期')
    flag = models.BooleanField(verbose_name='是否出货', default=0)
    unit = models.CharField(verbose_name='单位', max_length=20)
    person = models.CharField(verbose_name='人物姓名', max_length=20)

    factory = models.ForeignKey(to='Factory')
    name = models.ForeignKey(to='Commodity')

    class Meta:
        verbose_name_plural = '流动信息表'
