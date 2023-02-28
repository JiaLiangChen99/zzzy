import json

from peewee import Model,CharField,AutoField, IntegerField
from model.engine import mysql_db

class GENE_SNPPANEL(Model):
    PANEL_ID = AutoField()
    GENE_CODE = CharField(max_length=90)
    PANEL_NAME = CharField(max_length=90)
    GENE_VERSION = IntegerField()
    GENE_CHR = CharField()
    GENE_LOCATION = CharField(max_length=90)
    GEME_PRE = CharField(max_length=1)
    GENE_COM = CharField(max_length=1)
    #CROP = CharField(max_length=90)
    class Meta:
        database = mysql_db
        table_name = 'GENE_SNPPANEL' #表名

#mysql_db.create_tables([GENE_SNPPANEL])


#插入 4panel数据
# import pandas as pd
# df = pd.read_csv('panel_data/4panel_data.csv',encoding='utf-8')
#
# from sqlalchemy import create_engine
# engine = create_engine("mysql+pymysql://root:123456@localhost:3306/zzzy")
# df.to_sql("gene_snppanel", engine, schema="zzzy", if_exists='replace', index=False,chunksize=None, dtype=None)


#dash组件生成
import pandas as pd
import dash
from dash import html, Input, Output, dcc
import feffery_antd_components as fac
import plotly.graph_objects as go
import numpy as np
app = dash.Dash(__name__)



app.layout = html.Div(
    [
        dcc.Location(id='genedata'),
        dcc.Store(id='table_data'),
        dcc.Store(id = 'chr_data'),
        dcc.Store(id='gene_data'),
        fac.AntdTable(
            columns=[],
            bordered=True,
            data=[],
            id = 'gene_table',
),
        dcc.Graph(id='chr_picture')
    ]
)



@app.callback(
    Output('gene_data','data'),
    Output('chr_data','data'),
    Output('table_data', 'data'),
    Input('genedata','pathname'),
)
def show_gene_data(pathname):
    if pathname:
        #测试数据 D:\file\digital_server\model\panel_data\4panel_data.csv
        _4panel = pd.read_csv('D:/file/digital_server/model/panel_data/4panel_data.csv',encoding='utf-8')[['GENE_CODE','GENE_CHR','GENE_LOCATION','GEME_PRE']]
        _60data = pd.read_csv('D:/file/digital_server/model/panel_data/60样本data.csv',encoding='utf-8')
        #去除60data的无关数据，用于表连接
        new_column = [i for i in _60data.columns if i not in ['GENE_CHR','GENE_LOCATION','SNP']]
        _60data = _60data[new_column]
        df = pd.merge(right=_60data, left=_4panel,right_on='GENE_CODE',left_on='GENE_CODE',how='left').iloc[:,:14]
        df = df.fillna('-')
        df['GENE_CHR'] = df['GENE_CHR'].astype('str')
        for i in df.columns:
            if i not in ['GENE_CODE','GENE_CHR','GENE_LOCATION','GEME_PRE']:
                newlist = []
                for ref in df[i]:
                    if ref == '-':
                        newlist.append(ref)
                    elif ref[0] != ref[1]:
                        newlist.append('H')
                    else:
                        newlist.append(ref[0])
                df[i] = newlist
        #返回结果为只有GENE_CODE，GENE_CHR，GENE_LOCATION，GEME_PRE，taixiangdao	，xiangyaxiangzhan的数据框

        chrnum = df['GENE_CHR'].unique() # 获取染色体数目

        # 获取到比对样本和其他样本数据，默认前四个信息为无关变量ENE_CODE，GENE_CHR，GENE_LOCATION，GEME_PRE 数据格式很重要
        special_gene = {}
        for chr in chrnum:
            special_gene[chr] = df[df['GENE_CHR'] == chr].iloc[:,4:].to_dict(orient ='list')
        #结果如下  {染色体1：{样本1：【a,g,c,t,.....】,'样本2':[c,g,a,t,t,a]....}}

        #table的列名参数
        table_column = [{
            'title': i,
            'dataIndex': i
        } for i in df.columns]

        #table的数据，转化为[{gene_code:1,'gene_chr':1....},{gene_code:2,'gene_chr':2....}]
        data_dict = df.to_dict(orient ='records')
        return json.dumps(special_gene, ensure_ascii=False), chrnum, {'column':table_column, 'data':data_dict}


@app.callback(
    Output('gene_table','conditionalStyleFuncs'),
    Output('gene_table','columns'),
    Output('gene_table','data'),
    Input('table_data','data'),
)
def make_table(data):
    #数据渲染
    if data:
        js_dict = {}
        compare_special = data['column'][4]['title']

        js_dict[compare_special] = "(record, index) => {if (record['%(name)s'] == '-' ) {return {style : {backgroundColor: `#575352`,color : 'white'}};};if (record['%(name)s'] == 'H') {return {style : {backgroundColor: `#36b389`,color : 'white'}};};if (record['%(name)s'] != 'H' ) {return {style : {backgroundColor: `#FF6D00`,color : 'white'}};};}" % {'name':compare_special}
        for i in data['column'][5:]:
            spe = i['title']
            js_dict[spe] = "(record, index) => {if (record['%(name)s'] == '-' ) {return {style : {backgroundColor: `#575352`,color : 'white'}};};if (record['%(name)s'] == record['%(compare)s']) {return {style : {backgroundColor: `red`,color : 'white'}};};if (record['%(name)s'] != record['%(compare)s'] ) {return {style : {backgroundColor: `green`,color : 'white'}};};}" % {'name':spe,'compare':compare_special}

        return js_dict ,data['column'], data['data']


@app.callback(
    Output('chr_picture','figure'),
    Input('gene_data', 'data'),
    Input('chr_data', 'data'),
)
def show_picture(genedata, chrdata):
    """
    :param genedata: 染色体data ['1','2','3']
    :param chrdata:   各个染色体样本量数据 {'1':{样本1:[ATCG],样本2:[ATCG]}}
    计算思路如下：
    将两个样本的参考基因进行zip合并，然后分别求相同值的个数，但是前提是两个值不为缺失值：如  参考样本的基因为-  样本的基因也为-, 那就没有计算意义了
    """
    #隐含的参数 参考物种和比较物种  这两个参数可以添加，这里写死
    genedata = json.loads(genedata)
    refer, compare = list(genedata['1'].keys())[0], list(genedata['1'].keys())[1:]
    chr_similar = {}  #{'chr1':{'样本1':0.334,'样本2':0.578.....},'chr2':{'样本1':'0.778'....}}
    for chr in chrdata:
        chr_similar[chr] = {}
        refer_gene = genedata[chr][refer]
        for com in compare:
            '''
            如何计算呢：  当两个样本都不为缺失值，才可以用来计算
            '''
            chr_similar[chr][com] = len([item for item in zip(refer_gene, genedata[chr][com]) if (item[0] == item[1]) and ((item[0] != '-') and (item[1] != '-'))]) / len(refer_gene)
        chr_similar[chr][refer] = 1
    #定义y轴的name值
    yaxis = []
    for com in [*compare,refer]:
        mean_list = []
        for i in chr_similar.values():
            mean_list.append(i[com])
        yaxis.append(f'{com}-{round(np.mean(mean_list) * 100,2)}%')

    fig = go.Figure()
    for chr in chr_similar:
        fig.add_trace(go.Bar(y=yaxis, x= [round(value*100,2) for value in chr_similar[chr].values()], name=f'染色体{chr}',orientation="h"))

    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})  # 字母表升序
    return fig

#app.run_server(debug=True)


