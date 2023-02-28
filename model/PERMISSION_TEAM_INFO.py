from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class PERMISSION_TEAM_INFO(Model):
    # 团队ID
    TEAM_ID = AutoField()
    # 团队名
    TEAM_NAME = CharField(max_length=90)
    # 团队成员
    TEAM_MEMBER = CharField()
    # 团队成员权限
    TEAM_MEMBER_CODE = IntegerField()
    # 成员机构
    TEAM_MEMBER_UNIT = CharField()
    # 创建事件
    TEAM_CREATE_TIME = DateTimeField()
    #团队描述
    TEAM_DESCRIBE = CharField(null=True)
    #创建人
    TEAM_CREATE_MEMBER = CharField()
    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_TEAM_INFO' #表名

mysql_db.create_tables([PERMISSION_TEAM_INFO])