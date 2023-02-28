from peewee import (
    Model,
    IntegerField, CharField, TextField, AutoField
)
from model.engine import mysql_db


class PERMISSION_LITERATURE(Model):
    # 文献id
    LITERATURE_ID = AutoField()
    # 文献标题
    LITERATURE_NAME = CharField(null=True)
    # 文献作者
    LITERATURE_AUTHOR = CharField(null=True)
    # 问下关键词
    LITERATURE_KEYWORD = CharField(null=True)
    # 文献摘要
    LITERATURE_DESCRIBE = TextField(null=True)
    # 文献分类
    LITERATURE_TYPE = CharField(null=True)
    # 文献下载地址
    LITERATURE_URL = CharField(null=True)
    # 文献状态
    LITERATURE_CODE = IntegerField()
    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_LITERATURE' #表名

mysql_db.create_tables([PERMISSION_LITERATURE])