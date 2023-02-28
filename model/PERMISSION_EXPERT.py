from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class PERMISSION_EXPERT(Model):
    # 专家ID
    EXPERT_ID = AutoField()
    # 名字
    EXPERT_NAME = CharField(max_length=50)
    # 专家描述
    EXPERT_DISCRIBE = TextField()
    # 发布时间
    RELEASE_TIME = DateTimeField(null=True)


    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_EXPERT' #表名

mysql_db.create_tables([PERMISSION_EXPERT])