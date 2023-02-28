from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class SEED_HOUSE_INFO(Model):
    # 库存单位ID
    SAVE_HOUSE_ID = AutoField()
    # 库存单位
    SAVE_HOUSE_NAME = CharField(max_length=50)
    # 长期库短期库
    HOUSE_TIME_TYPE = CharField(max_length=50)
    # 库存储情况
    HOUSE_INFO = CharField(max_length=50)


    class Meta:
        database = mysql_db
        table_name = 'SEED_HOUSE_INFO' #表名

mysql_db.create_tables([SEED_HOUSE_INFO])