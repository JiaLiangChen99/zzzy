from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class SEED_OUT_HOUSE(Model):
    # 种质id
    SEED_ID = AutoField()
    # 申请人
    APPLY_USERNAME = CharField(max_length=50)
    # 申请单位
    APPLY_UNIT = CharField(max_length=50)
    # 作物类型
    CROP_NAME = CharField(max_length=50)
    # 申请电话
    APPLY_PHONE = CharField(max_length=50)
    # 申请时间
    APPLY_TIME = DateTimeField(default=datetime.now())
    # 协议编号
    APPLY_NUMBER = CharField(null=True)
    # 申请理由
    APPLY_REASON = TextField()
    # 出库状态
    OUT_CODE = IntegerField()  #待审批，出库

    class Meta:
        database = mysql_db
        table_name = 'SEED_OUT_HOUSE' #表名

mysql_db.create_tables([SEED_OUT_HOUSE])