
from peewee import (
    Model,
    CharField, TextField, AutoField, FloatField
)
from model.engine import mysql_db


class SEED_SHENDING(Model):
    # 种质id
    SEED_ID = AutoField()
    # 受让单位
    TRANSFER_UNIT = CharField(max_length=90)
    # 转让金额
    TRANSFER_MONEY = FloatField()
    # 累计推广面积
    COMMUNICATE_AREA = FloatField()
    # 农民喜好度
    FARM_LIKE = TextField(null=True)
    class Meta:
        database = mysql_db
        table_name = 'SEED_SHENDING' #表名

mysql_db.create_tables([SEED_SHENDING])