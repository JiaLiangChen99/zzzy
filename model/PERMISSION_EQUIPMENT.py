from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class PERMISSION_EQUIPMENT(Model):
    # 设备ID
    EQUIPMENT_ID = AutoField()
    # 设备名字
    EQUIPMENT_NAME = CharField(max_length=50)
    # 设备描述
    EQUIPMENT_DESCRIBE = TextField()
    # 发布时间
    RELEASE_TIME = DateTimeField(null=True)
    # 图片路径
    IMAGE_ID = CharField(null=True)
    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_EQUIPMENT' #表名

mysql_db.create_tables([PERMISSION_EQUIPMENT])