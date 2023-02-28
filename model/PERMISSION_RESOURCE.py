from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class PERMISSION_RESOURCE(Model):
    # 新闻ID
    CODE_TYPE = IntegerField()
    # 资源名字
    RESOURCE_NAME = CharField(max_length=90)
    # 资源路径
    RESOURCE_PATH = CharField()

    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_RESOURCE' #表名

mysql_db.create_tables([PERMISSION_RESOURCE])