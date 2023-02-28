from peewee import Model,CharField,AutoField, IntegerField
from model.engine import mysql_db

class GENE_SNP(Model):
    GENE_ID = AutoField()
    GENE_CODE = CharField(max_length=90)
    GENE_CHR = IntegerField()
    GENE_LOCATION = CharField()
    GENE_REFER = CharField(max_length=1)
    GENE_COMPARE = CharField(max_length=1)
    CROP = CharField(max_length=90)

    class Meta:
        database = mysql_db
        table_name = 'GENE_SNP' #表名

mysql_db.create_tables([GENE_SNP])