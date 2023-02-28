from peewee import (
    Model,
    IntegerField, DateTimeField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class SEED_TEMPERATURE(Model):
    # 库存单位ID
    SAVE_HOUSE_ID = AutoField()
    # 日期
    TIME_STAMPT = DateTimeField(default=datetime.now())
    # 温度
    TEMPERATURE = IntegerField()

    class Meta:
        database = mysql_db
        table_name = 'SEED_TEMPERATURE' #表名

mysql_db.create_tables([SEED_TEMPERATURE])