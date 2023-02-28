from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class PERMISSION_PROJECT(Model):
    # 项目ID
    PROJECT_ID = AutoField()
    # 项目名
    PROJECT_NAME = CharField(max_length=90)
    # 创建人
    PROJECT_CREATE_MEMBER = CharField()
    # 创建时间
    PROJECT_CREATE_TIME = DateTimeField(default=datetime.now())
    # 成员
    PROJECT_MEMBER = CharField()
    # 项目状态
    PROJECT_CODE = IntegerField()
    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_PROJECT' #表名

mysql_db.create_tables([PERMISSION_PROJECT])