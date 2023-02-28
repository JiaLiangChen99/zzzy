from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class PERMISSION_ASSOCIATE_SERVICE(Model):
    # 关联id
    ASSOCIATE_ID = AutoField()
    # 关联服务名称
    ASSOCIATE_NAME = CharField(max_length=50)
    # 专家描述
    ASSOCIATE_DESCRIBE = TextField()
    # 关联服务图片路径
    IMAGE_ID = CharField(null=True)
    # 时间
    ASSOCIATE_TIME = DateTimeField(null=True)
    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_ASSOCIATE_SERVICE' #表名

mysql_db.create_tables([PERMISSION_ASSOCIATE_SERVICE])