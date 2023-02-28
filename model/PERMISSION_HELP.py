from peewee import (
    Model,
    CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class PERMISSION_HELP(Model):
    # 帮助服务ID
    HELP_SERVER_ID = AutoField()
    # 帮助服务
    HELP_SERVER_NAME = CharField(max_length=50)
    # 申请单位
    HELP_SERVER_DESCRIBE = TextField()
    # 帮助服务具体信息
    HELP_SERVER_INFO = CharField(max_length=50)
    # 上传时间
    HELP_SERVER_TIME = DateTimeField(null=True,default=datetime.now())
    # 帮助服务图片ID
    HELP_SERVER_IMG_ID = CharField()

    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_HELP' #表名

mysql_db.create_tables([PERMISSION_HELP])