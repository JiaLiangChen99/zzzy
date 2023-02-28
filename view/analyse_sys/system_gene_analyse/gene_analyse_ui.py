import json

import dash
import feffery_antd_components as fac
from dash import html,dcc
from model.GENE_SNPPANEL import GENE_SNPPANEL
from server import app
from dash import Input,Output,State
from peewee import Database
import pandas as pd
import numpy as np
import plotly.graph_objects as go

#默认数据
def mydata():
    return pd.read_csv('model/panel_data/60样本data.csv',encoding='gbk')


#比对基因模块
def gene_compare_ui(**kwargs):
    return [

        dcc.Store(id='select-special-chr-store'),
        dcc.Store(id='select-project-data'),
        dcc.Store(id='compare_gene_init'),
        dcc.Store(id='compare_gene_table_alldata'), #进行比对后的表格数据store
        dcc.Store(id='chr_data'),  # 各个染色体的对比数据
        html.Div(id='form-error-info'),
        html.Div([
            fac.AntdHeader('品种基因型比较',className='sys-function-header'),
            fac.AntdRow(
                [
                    fac.AntdCol(
                        [
                            fac.AntdText('染色体',className='header_text'),
                            fac.AntdSelect(
                                placeholder='所有',
                                mode='multiple',
                                options=[],
                                style={
                                    # 使用css样式固定宽度
                                    'width': '200px'
                                },
                                id = 'compare-form-chr'
                            )
                        ]
                        ,span=8,
                        className='compare_gene_form_btn'
                    ),
                    fac.AntdCol(
                        [
                            fac.AntdText('标记编号',className='header_text'),
                            fac.AntdInput(style={
                                    # 使用css样式固定宽度
                                    'width': '200px'
                                },id='compare-form-snpcode')
                        ]
                    , span=8,
                        className='compare_gene_form_btn'
                    ),
                    fac.AntdCol(
                        [
                            fac.AntdText('Panel 组合',className='header_text'),
                            fac.AntdSelect(
                                options=[{'label': '4k Panel', 'value': '4k Panel'},
                                   ],
                                mode='multiple',
                                style={
                                    # 使用css样式固定宽度
                                    'width': '200px'
                                },
                                id='compare-form-panel'
                            )
                        ]
                        , span=8,
                        className='compare_gene_form_btn'
                    ),
                    fac.AntdCol(
                        [
                            fac.AntdText('起始标记位点',className='header_text'),
                            fac.AntdInputNumber(
                                style={
                                    'width': '200px',
                                    'marginBottom': '5px'
                                },
                                id='compare-form-startlocation'
                            )
                        ]
                        , span=8,
                        className='compare_gene_form_btn'
                    ),
                    fac.AntdCol(
                        [
                            fac.AntdText('末尾标记位点',className='header_text'),
                            fac.AntdInputNumber(
                                style={
                                    'width': '200px',
                                    'marginBottom': '5px'
                                },
                                id='compare-form-endlocation'
                            )
                        ]
                        , span=8,
                        className='compare_gene_form_btn'
                    ),
                    fac.AntdCol(
                        [
                            fac.AntdButton('重置'),
                            fac.AntdButton('检索',id='compare-form-search'),
                        ]
                        , span=8,
                        className='compare_gene_form_btn'
                    )
                ],
                justify='space-around',
                className='gene-analyse-header'
            ),
        fac.AntdModal([


        ],id='compare-gene-selectproject-model',
            width=700,
            centered=True,
            title=html.Div('项目选择')
        ),
        fac.AntdRow(
            [
                fac.AntdTabs(
                    [
                        fac.AntdTabPane(
                            [
                            fac.AntdRow(
                                fac.AntdCol([
                                    fac.AntdButton('比对项目',className='compare_file',id='compare-gene-selectproject')
                                ])
                            ),
                            fac.AntdRow(
                                fac.AntdCol(
                                    fac.AntdTable(
                                        columns=[],
                                        data=[],
                                        maxWidth=1000,
                                        bordered=True,
                                        className='compare_table_style',
                                        id = 'compare_gene_table'
                                    )
                                )
                            )
                            ],
                            tab='表格视图',
                            key='表格视图'
                        ),
                        fac.AntdTabPane(
                            tab='染色体视图',
                            key='染色体视图'
                        ),
                        fac.AntdTabPane(
                            [dcc.Graph(id='gene_compare_chart')],
                            tab='相似度比较',
                            key='相似度比较'
                        )
                    ],
                    tabPosition='left'
                ),
            ],
            className='gene_analyse_tab'
        )
        ],className='genecompare_hader')
    ]


#查询条件函数
def update_where_dict(where=None, **kwargs):
    if where is None:
        where = GENE_SNPPANEL.select(GENE_SNPPANEL.GENE_CODE,
                                    GENE_SNPPANEL.GENE_CHR,
                                    GENE_SNPPANEL.GENE_LOCATION,
                                    GENE_SNPPANEL.GEME_PRE,)
    for key, value in kwargs.items():
        #当不为空才有条件添加
        if value is not None:
            if isinstance(value,dict): #如果为dict 说明是多选项的值
                #说明要么是位点，要么是染色体 要么是panel
                if value['type'] == 'location':  #位点查询
                    if value['value'][1] == 'end':
                        where = where.where(getattr(GENE_SNPPANEL, key) > value['value'][0])
                    else:
                        where = where.where(getattr(GENE_SNPPANEL, key).between(value['value'][0], value['value'][1]))
                elif value['type'] == 'chr':
                    expression = None
                    for selectchr in value['value']:
                        selectchr = int(selectchr)
                        expression = expression | (getattr(GENE_SNPPANEL, key) == selectchr) if expression is not None else (
                                    getattr(GENE_SNPPANEL, key) == selectchr)
                    where = where.where(expression)
                elif value['type'] == 'panel':
                    expression = None
                    for selectchr in value['value']:
                        expression = expression | (getattr(GENE_SNPPANEL, key) == selectchr) if expression is not None else (
                                    getattr(GENE_SNPPANEL, key) == selectchr)
                    where = where.where(expression)
            else:
                where = where.where(getattr(GENE_SNPPANEL, key) == value)
    return where

'''
根据当前页面更新染色体数量
'''
@app.callback(
    Output('select-special-chr-store','data'), #染色体存放数据store
    Input('system-select-special-store','data'),
)
def get_special_chr_data(data):
    if data == '水稻':
        return 12
    else:
        return 1

'''
染色体数量修饰的组件
'''
#todo 后续还有其他组件需要用到染色体数量信息的，所以要添加的
@app.callback(
    Output('compare-form-chr','options'),
    Input('select-special-chr-store','data'),
)
def show_compare_form_chr(data):
    return [
        {'label': str(i) , 'value': str(i)} for i in range(1,data+1)]


'''
条件筛选
'''
@app.callback(
    Output('compare_gene_init','data'),
    Output('form-error-info','children'),
    Input('system-select-special-store','data'),  #全局的物种store！！！！
    Input('compare-form-search','nClicks'),
    State('compare-form-chr','value'),
    State('compare-form-snpcode','value'),
    State('compare-form-panel', 'value'),
    State('compare-form-startlocation', 'value'),
    State('compare-form-endlocation', 'value'),
)
def compare_table_init(data,
    nclicks,chr,snpcode,panel,startlocation,endlocation
                       ):
    """
    页面初始化时或者当进行表单查询是，对原始序列进行查询获取，并更新

    :param data:   当前物种数据
    :param nclicks:   对比基因模块：进行查询操作是的按钮事件
    :param chr:    选择的染色体
    :param snpcode:  选择的snp位点编号
    :param panel:   选择的panel
    :param startlocation:   起始位点
    :param endlocation:   终止位点
    :return:
    """
    if nclicks:
        '''
         比较多情况的是首尾数值的情况，需要传入list去做范围选取
        '''
        if startlocation and endlocation:
            if startlocation >= endlocation:
                return dash.no_update,fac.AntdMessage(
                                        content='起始位点应小于末尾位点',
                                        type='error'
                                    )
            betweenlist = {'type':'location','value':[startlocation,endlocation]}
        elif startlocation == None and endlocation!= None:
            '''当初始值为空而末尾值不为空  说明查询0-末尾的数据'''
            betweenlist = {'type':'location','value':[0,endlocation]}
        elif startlocation != None and endlocation == None:
            '''当末尾值为空而初始值不为空  说明查询大于初始值的的数据'''
            betweenlist = {'type':'location','value':[startlocation,'end']}
        else:
            betweenlist = None

        '''
        染色体情况
        '''
        if isinstance(chr,list):
            chr_data = {'type':'chr','value':chr}
        else:
            chr_data = chr
        '''
        Panel组合情况
        '''
        if isinstance(panel,list):
            panel_data = {'type':'panel','value':panel}
        else:
            panel_data = panel
        #首位位点判断
        query_dict = {
            'GENE_CODE':snpcode,
            'GENE_CHR' : chr_data,
            'PANEL_NAME':panel_data,
            'GENE_LOCATION':betweenlist
        }
        cursor = update_where_dict(**query_dict)
        return list(cursor.dicts()),dash.no_update
    if data:
        cursor = GENE_SNPPANEL.select(GENE_SNPPANEL.GENE_CODE,
                                    GENE_SNPPANEL.GENE_CHR,
                                    GENE_SNPPANEL.GENE_LOCATION,
                                    GENE_SNPPANEL.GEME_PRE,
                                    )
        return list(cursor.dicts()),dash.no_update


#根据返回的table data 对表格进行渲染
#todo  后续表格的修改都在这里
@app.callback(
    Output('compare_gene_table','data'),
    Output('compare_gene_table','columns'),
    Input('compare_gene_init','data'),
    Input('compare_gene_table_alldata','data'), #当进行序列比较之后，对table的数据进行更新
)
def data_to_compare_table(data,compare_data):
    '''
    :param data:  初始化时的数据，就是页面刚开始要用来渲染
    :param compare_data:  当读取了数据后，进行比对后，返回的需要渲染的数据 {'data':xx,'columns':xxx}
    :return:
    '''
    if dash.ctx.triggered_id == 'compare_gene_init':
        return [{'位点编号':i['GENE_CODE'],
                 '染色体': i['GENE_CHR'],
                 '标记位置': i['GENE_LOCATION'],
                 '参考值': i['GEME_PRE'],
                 } for i in data], [
                                            {
                                                'title': '位点编号',
                                                'dataIndex': '位点编号',
                                            },
                                            {
                                                'title': '染色体',
                                                'dataIndex': '染色体',
                                            },
                                            {
                                                'title': '标记位置',
                                                'dataIndex': '标记位置',
                                            },
                                            {
                                                'title': '参考值',
                                                'dataIndex': '参考值',
                                            },
                                        ]
    elif dash.ctx.triggered_id == 'compare_gene_table_alldata': #说明是渲染比对的数据
        return compare_data['data'],compare_data['columns'],

    else:
        return dash.no_update,dash.no_update

'''
更新表格样式
'''
#todo  正常来讲这里需要有比对的参考物种和比较的其他物种的，这里还没弄直接写死吧
@app.callback(
    Output('compare_gene_table','conditionalStyleFuncs'),
    Input('compare_gene_table_alldata','data'),
)
def compare_table_style(data):
    if data:
        compare_special = data['columns'][4]['title']
        otherspecial = [data['columns'][i]['title'] for i in range(5,len(data['columns']))]
        js_dict = {}
        js_dict[
            compare_special] = "(record, index) => {if (record['%(name)s'] == '-' ) {return {style : {backgroundColor: `#575352`,color : 'white'}};};if (record['%(name)s'] == 'H') {return {style : {backgroundColor: `#36b389`,color : 'white'}};};if (record['%(name)s'] != 'H' ) {return {style : {backgroundColor: `#FF6D00`,color : 'white'}};};}" % {
            'name': compare_special}
        for spe in otherspecial:
            js_dict[
                spe] = "(record, index) => {if (record['%(name)s'] == '-' ) {return {style : {backgroundColor: `#575352`,color : 'white'}};};if (record['%(name)s'] == record['%(compare)s']) {return {style : {backgroundColor: `red`,color : 'white'}};};if (record['%(name)s'] != record['%(compare)s'] ) {return {style : {backgroundColor: `green`,color : 'white'}};};}" % {
                'name': spe, 'compare': compare_special}
        return js_dict

'''
将基因比较页面的柱形图进行绘制
'''
@app.callback(
    Output('gene_compare_chart','figure'),
    Input('compare_gene_table_alldata', 'data'),
    State('select-special-chr-store','data'),
    prevent_initial_call=True
)
def show_compare_gene_figure(genedata, chrnum):
    if genedata:
        """
        :param genedata: 染色体data ['1','2','3']
        :param chrdata:   各个染色体样本量数据 {'1':{样本1:[ATCG],样本2:[ATCG]}}
        计算思路如下：
        将两个样本的参考基因进行zip合并，然后分别求相同值的个数，但是前提是两个值不为缺失值：如  参考样本的基因为-  样本的基因也为-, 那就没有计算意义了
        """
        #隐含的参数 参考物种和比较物种  这两个参数可以添加，这里写死
        chrnum = [str(i) for i in range(1,chrnum+1)]
        refer, compare = genedata['columns'][4]['title'],  [genedata['columns'][i]['title'] for i in range(5,len(genedata['columns']))]

        pddf = pd.DataFrame(genedata['data'])
        mygenedata = {}
        for i in chrnum:
            mygenedata[i] = {}
            mygenedata[i][refer] = list(pddf[(pddf['染色体'] == i)][refer].values)
            for com in compare:
                mygenedata[i][com] = list(pddf[(pddf['染色体'] == i)][com].values)

        chr_similar = {}  #{'chr1':{'样本1':0.334,'样本2':0.578.....},'chr2':{'样本1':'0.778'....}}
        print(chr_similar)
        for chr in chrnum:
            chr_similar[chr] = {}
            refer_gene = mygenedata[chr][refer]

            for com in compare:
                '''
                如何计算呢：  当两个样本都不为缺失值，才可以用来计算
                '''
                chr_similar[chr][com] = len([item for item in zip(refer_gene, mygenedata[chr][com]) if (item[0] == item[1]) and (item[1] != 'H')]) / len(refer_gene)
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


'''
当点击了项目比对后，现在假设没有数据的读入之类的操作先了

这里对数据进行预处理，并且返回表格的data数据和column的数据
'''
#todo  后续需要加上，数据的读取之类的,选择比对的物种之类的，这里用函数写死读取其中一个数据读取前十五列进行分析
@app.callback(
    Output('compare_gene_table_alldata','data'), #更新比对的所有数据，同步column的
    Input('compare-gene-selectproject','nClicks'),
    State('compare_gene_init','data'),
)
def show_compare_gene_selectproject_model(n,init_data):
    if n:
        df1 = mydata()
        newcolumn = [i for i in df1.columns if i not in ['GENE_CHR','GENE_LOCATION','SNP']]
        df1 = df1[newcolumn]
        df2 = pd.DataFrame(init_data)

        #数据处理 数据先合并了,且只读前xx列数据
        mergedf = pd.merge(right=df1, left=df2,right_on='GENE_CODE',left_on='GENE_CODE',how='left').fillna('-')
        print(mergedf)
        for i in mergedf.columns:
            if i not in ['GENE_CODE','GENE_CHR','GENE_LOCATION','GEME_PRE']:
                newlist = []
                for ref in mergedf[i]:
                    if ref == '-':
                        newlist.append(ref)
                    elif ref[0] != ref[1]:
                        newlist.append('H')
                    else:
                        newlist.append(ref[0])
                mergedf[i] = newlist
        '''
        数据英文翻译，如果需要翻译为英文，后期用cookie来判断
        '''
        coumns_name_dict = {'GENE_CODE':'位点编号','GENE_CHR':'染色体',
                            'GENE_LOCATION':'标记位置','GEME_PRE':'参考基因'}
        mergedf.rename(columns=coumns_name_dict,inplace=True)
        mergedf = mergedf.iloc[:,:15]
        #todo width失效问题？？？并未按照预期填充column格式
        return{'data':mergedf.to_dict(orient ='records'),
           'columns':[{'title':i, 'dataIndex':i, 'width':400} for i in mergedf.columns]}
    else:
        return dash.no_update