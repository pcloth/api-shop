from django.db import models

# Create your models here.

class AccountCmdsAlias(models.Model):
    class Meta:
        db_table = 'account_cmds_alias'

    sender = models.CharField(max_length=64, verbose_name="发送者")
    commands = models.TextField(verbose_name="指令内容json")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')