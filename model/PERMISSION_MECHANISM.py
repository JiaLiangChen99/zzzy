from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class PERMISSION_MECHANISM(Model):
    # 机构ID
    MECHANISM_ID = AutoField()
    # 机构名
    MECHANISM = CharField(max_length=90)

    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_MECHANISM' #表名

mysql_db.create_tables([PERMISSION_MECHANISM])