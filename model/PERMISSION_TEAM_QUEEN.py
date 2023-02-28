from peewee import (
    Model,
    IntegerField, CharField, DateTimeField, TextField, AutoField
)
from model.engine import mysql_db
from datetime import datetime

class PERMISSION_TEAM_QUEEN(Model):
    # 团队ID
    TEAM_ID = AutoField()
    # 团队名
    TEAM_NAME = CharField(max_length=90)
    # 团队创建人
    TEAM_CREATER = CharField(max_length=90)
    # 消息状态(发送邀请，接受邀请，拒绝邀请,退出团队)
    # 作为发送方，我需要给user发送code为0 代表邀请人
    # 作为邀请人,我可以检索code为0的数据，这时候我的检索条件为
    # QUEEN_GETTER=邀请人视角， 然后如果我同意邀请了，这时候发送的code为1 如果我拒绝 发送的code为2
    # 这时，就去修改这条信息，把这条邀请的code改为1,说明我同意，改为2说明我拒绝
    # 同时，我要需要额外添加一条
    # 这时候作为邀请者  看到code=1  就知道我是同意加入了 看到code =2 说明是拒绝了 看到code还是为0，说明邀请的人还没有处理呗
    #
    TEAM_CODE = IntegerField()
    # 消息创建人
    QUEEN_SENDER = CharField()
    # 消息接收人
    QUEEN_GETTER = CharField()
    # 发送时间
    SEND_TIME = DateTimeField()
    #消息描述
    SEND_DESC = CharField(null=True)

    class Meta:
        database = mysql_db
        table_name = 'PERMISSION_TEAM_QUEEN' #表名

mysql_db.create_tables([PERMISSION_TEAM_QUEEN])