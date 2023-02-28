from peewee import (
    Model,
    IntegerField, AutoField, CharField
)
from model.engine import mysql_db


#用户权限表
class USER_PERMISSION(Model):
    USER_NAME = CharField(primary_key=True)
    GENE_ANALYSE_CODE = IntegerField()  #0,1 有无 基因分析
    PHENOTYPE_ANALYSE_CODE = IntegerField()  #表型分析
    SEED_RESOURCE_CODE = IntegerField()  #种质资源
    REPEAT_SEQUENCE = IntegerField()  #重复序列
    HOME_REVIEW = IntegerField()  #主页资源
    class Meta:
        database = mysql_db
        table_name = 'USER_PERMISSION' #表名


mysql_db.create_tables([USER_PERMISSION])


