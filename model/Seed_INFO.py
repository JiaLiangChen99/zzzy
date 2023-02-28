
from peewee import (
    Model,
    IntegerField, CharField, TextField,AutoField
)
import random
from faker import Faker
import json
from model.engine import mysql_db

class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)

#建表
class Seed_INFO(Model):
    # 种质id
    SEED_ID = AutoField
    # 具体品种名称  水稻为例：丝苗米
    SPECIES_NAME = CharField( max_length=90)
    # 经济作用等分类  如经济作物，水产
    FUNCTION_ClASSIFY = CharField(max_length=20)
    # 作物名称   水稻，鲫鱼
    CROP_NAME = CharField(max_length=50)
    # 种质资源类型  种子？幼苗？
    GERMOLASM_TYPE = CharField(max_length=30)
    #父本
    MALE_PARENT = CharField(null= True, max_length=50)
    # 母本
    FEMALE_PARENT = CharField(null=True, max_length=50)
    # 育种单位
    BREEDING_UNIT = CharField(null=True, max_length=50)
    # 性状
    CHARACTER = JSONField()
    class Meta:
        database = mysql_db
        table_name = 'Seed_INFO' #表名

mysql_db.create_tables([Seed_INFO])