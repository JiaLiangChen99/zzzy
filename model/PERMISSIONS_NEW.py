from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class PERMISSIONS_NEW(Model):
    # 新闻ID
    NEW_ID = AutoField()
    # 新闻标题
    NEW_TITLE = CharField(max_length=90)
    # 新闻内容
    NEW = TextField()
    # 发布时间
    RELEASE_TIME = DateTimeField(default=datetime.now())
    # 原文作者
    ORIGIN_AUTHOR = CharField(max_length=50)
    # 点击次数
    READ_COUNT = IntegerField()
    # 审核状态
    REVIEW_CODE = IntegerField()
    # 封面图片
    NEW_IMG_ID = CharField()


    class Meta:
        database = mysql_db
        table_name = 'PERMISSIONS_NEW' #表名

mysql_db.create_tables([PERMISSIONS_NEW])