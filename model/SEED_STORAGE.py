
from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, FloatField, AutoField
)
from model.engine import mysql_db
from datetime import datetime
import json

class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)

#建表
class SEED_STORAGE(Model):
    # 种质id
    SEED_ID = AutoField()
    # 种质保存类型
    SEED_SAVE_TYPE = CharField(null=True, max_length=90)
    # 申请人
    APPLY_USERNAME = CharField(max_length=90)
    # 申请单位
    APPLY_UNIT = CharField(max_length=90)
    # 申请电话
    APPLY_PHONE = CharField(max_length=90)
    # 申请时间
    APPLY_TIME = DateTimeField(default=datetime.now())
    # 有效期（年）
    VALIDITY_PERIOD = CharField(null=True, max_length=90)
    # 申请单号
    APPLY_NUMBER = CharField(null=True,)
    # 申请原因
    APPLY_REASON = TextField(null=True,)
    # 其他条件
    OTHER_CONDITION = TextField(null=True,)
    # 入库量
    STORAGE = FloatField()
    # 单位
    UNIT = CharField(null=True, max_length=90)
    # 全国统一编号
    SEED_COUNTRY_CODE = CharField(null=True, max_length=90)
    # 收集单位
    COLLECT_UNIT = CharField(null=True, max_length=90)
    # 保存单位
    SAVE_UNIT = CharField(null=True, max_length=90)
    # 审批状态
    APPLY_CODE = IntegerField()
    class Meta:
        database = mysql_db
        table_name = 'SEED_STORAGE' #表名

mysql_db.create_tables([SEED_STORAGE])