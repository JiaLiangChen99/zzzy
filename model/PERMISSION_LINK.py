from peewee import (
    Model,
    CharField, AutoField
)
from model.engine import mysql_db


class PERMISSION_LINK(Model):
    # 链接id
    LINK_ID = AutoField()
    # 链接名称
    LINK_NAME = CharField()
    # 链接URL
    LINK_URL = CharField()


    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_LINK' #表名

mysql_db.create_tables([PERMISSION_LINK])