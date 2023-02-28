import string
import hashlib
from datetime import datetime

from peewee import (
     Model,
     CharField, DateTimeField, AutoField
)
import random
from faker import Faker
from model.engine import mysql_db


class USER_INFO(Model):
    #字段1,设置为主键
    USER_ID = AutoField()
    #字段2
    USER_NAME = CharField(max_length=20)
    #字段3
    USER_PASSWORD = CharField(max_length=20)
    USER_PASSWORD_MD5 = CharField( max_length=50)
    USER_PHONE = CharField( max_length=30)
    USER_EMAIL = CharField(null=True, max_length=50)
    USER_UNIT = CharField(null=True, max_length=50)
    UNIT_ADDRESS = CharField(null=True, max_length=50)
    CREAT_TIME = DateTimeField(default=datetime.now())
    class Meta:
        database = mysql_db
        table_name = 'USER_INFO' #表名

mysql_db.create_tables([USER_INFO])

#
# #Faker插入数据模拟
# #用户名
# fake = Faker(locale='zh_CN')
# name = fake.name()
# print(name)
# #生成16位密码
# password = ''.join(random.sample(string.ascii_lowercase + string.digits, 16))
# hl=hashlib.md5()
# hl.update(password.encode(encoding='utf8'))
# md5=hl.hexdigest()
# print(md5)
# #生成电话
# phone = fake.phone_number()
# print(phone)
# # 生成邮箱地址
# email = fake.email()
# print(email)
# # 生成中文机构单位名字
# company = fake.company()
# print(company)
# # 生成中文地址
# address = fake.address()
# print(address)
# # 生成时间
# date = datetime.now().strftime('%Y-%m-%d')
# need_date = datetime.strptime(date, '%Y-%m-%d')
# print(need_date)
# USER_INFO.insert(USER_NAME=name, USER_PASSWORD=password,USER_PASSWORD_MD5 = md5,
#                 USER_PHONE = phone, USER_EMAIL = email, USER_UNIT = company,
#                 UNIT_ADDRESS = address, CREAT_TIME = need_date
#                  ).execute()

# password = '123'
# hl=hashlib.md5()
# hl.update(password.encode(encoding='utf8'))
# md5=hl.hexdigest()
# USER_INFO.insert(USER_NAME='root', USER_PASSWORD='123',USER_PASSWORD_MD5 = md5,
#                 USER_PHONE = phone, USER_EMAIL = email, USER_UNIT = company,
#                 UNIT_ADDRESS = address, CREAT_TIME = need_date
#                  ).execute()