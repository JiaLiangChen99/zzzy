import dash
import feffery_antd_components as fac
from dash import html,dcc,Input,Output,State
import pandas as pd
import numpy as np
from server import app
import plotly.graph_objects as go
import plotly.express as px
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import fcluster
import random
#任务表格
def gene_distance_ui(**kwargs):
    return [
        html.Div([
            dcc.Store(id='analyse_task'),
            fac.AntdModal(
                [dcc.Graph(id='distance_heatmap',style={'height':'700px'})],
                id='model-distance-analyse',
                          width=1200,
                          centered=True,
                          title=html.Div('遗传距离')
                          ),
            fac.AntdModal(
                [html.Div(
                    [   html.Div([
                        fac.AntdText('3DView'),
                        fac.AntdSpin(
                            dcc.Graph(id='pca_3Dscater', style={'height': '600px','width':'650px'}),
                            text='正在生成'),
                        ]),
                        html.Div([
                            fac.AntdText('2DView'),
                            fac.AntdSpin(
                                dcc.Graph(id='pca_2Dscater', style={'height': '600px', 'width': '650px'})
                            ,text='正在生成'),

                        ]),


                    ],style={'display':'flex','justify-content':'space-between'}
                )
                   ],
                id='model-pca-analyse',
                width=1400,
                centered=True,
                title=html.Div('PCA分析')
            ),
            fac.AntdHeader('遗传距离',className='sys-function-header'),
            fac.AntdRow(
                [
                    fac.AntdCol(
                        [
                            fac.AntdText('任务名称',className='header_text'),
                            fac.AntdInput(style={
                                    # 使用css样式固定宽度
                                    'width': '200px'
                                })
                        ]
                        ,span=8,
                        className='compare_gene_form_btn'
                    ),
                    fac.AntdCol(
                        [
                            fac.AntdText('任务状态', className='header_text'),
                            fac.AntdInput(style={
                                    # 使用css样式固定宽度
                                    'width': '200px'
                                })
                        ]
                        , span=8,
                        className='compare_gene_form_btn'
                    ),
                    fac.AntdCol(
                        [
                            fac.AntdButton('查询结果')
                        ]
                        , span=8,
                        className='compare_gene_form_btn'
                    ),
                ],
                justify='space-around',
                className='gene-analyse-header'
            ),
        fac.AntdRow(
            [
                fac.AntdTable(
                    id='table-comprehensive-analyse',  #所有分析结果的表格
                    columns=[
                        {
                            'title': '任务名',
                            'dataIndex': '任务名',
                        },
                        {
                            'title': '文件名称',
                            'dataIndex': '文件名称',
                            'renderOptions': {
                                    'renderType': 'link',
                                    'renderLinkText': '点击跳转'
                                },
                        },
                        {
                            'title': '文件大小',
                            'dataIndex': '文件大小',
                        },
                        {
                            'title': '创建时间',
                            'dataIndex': '创建时间',
                        },
                        {
                            'title': '任务状态',
                            'dataIndex': '任务状态',
                        },
                        {
                            'title': '分析结果',
                            'dataIndex': '分析结果',
                            'renderOptions': {'renderType': 'button'},
                        },
                    ],
                    data=[
                        {
                            'key': 1,
                            '任务名':'测试数据',
                            '文件名称':{
                                    'href': 'https://github.com/CNFeffery/feffery-antd-components'
                                },
                            '文件大小':'1024kb',
                            '创建时间':'2021-12-12 21:33:45',
                            '任务状态':'success',

                            '分析结果': [{
                                'content': '遗传距离',
                                'type': 'primary'
                            },
                                {
                                    'content': 'PCA分析',
                                    'type': 'primary'
                                }
                            ],
                        }
                    ],
                    bordered=True
                ),

            ],
            className='gene_analyse_tab'
        )
        ],className='genecompare_hader')
    ]


@app.callback(
    Output('analyse_task','data'),
    Input('table-comprehensive-analyse','nClicksButton'),
    State('table-comprehensive-analyse','clickedContent'),
    State('table-comprehensive-analyse','recentlyButtonClickedRow'),
prevent_initial_call=True
)
def change_model(n,a1,a2):
    '''
    当table点击了任务分析时的回调
    :param n: 点击
    :param a1: 返回的是那个按钮事件  如遗传距离,PCA分析
    :param a2: 返回点击的按钮的具体行信息 如
    {'key': 1, '任务名': '测试数据',
    '文件名称': {'href': 'https://github.com/CNFeffery/feffery-antd-components'},
     '文件大小': '1024kb',
     '创建时间': '2021-12-12 21:33:45',
      '任务状态': 'success',
       '分析结果': [{'content': '遗传距离', 'type': 'primary'},
        {'content': 'PCA分析', 'type': 'primary'}]}
    通过a2和a1,来获取到是那个按钮任务被触发以及按钮的具体信息
    '''
    if n:
        #todo 加上一些别的判断
        return {'taskname':a1,'taskid': a2['key']} #task那么是分析名字，taskid为任务id


'''
以下两个函数都为遗传距离的回调
'''
@app.callback(
    Output('model-distance-analyse','visible'),
    Input('analyse_task','data'),
)
def openmodel(data):
    '''
    根据data返回model的组件
    :param data:
    :return:
    '''
    if data:
        if data['taskname'] == '遗传距离':
            #获取任务类型和任务id
            tasktype = data['taskname']
            taskid = data['taskid']
            return True
        else:
            return dash.no_update
    else:
        return dash.no_update

@app.callback(
    Output('distance_heatmap','figure'),
    Input('analyse_task','data'),
)
def show_heatmap_figure(data):
    if data:
        if data['taskname'] == '遗传距离':
            taskid = data['taskid']
            # todo 读取任务文件就好了
            testdf = pd.read_csv(r'D:/file/digital_server/model/panel_data/distance_test.csv', index_col=0)
            heatmap_value = np.round(testdf.values, 3)  # 数据框数组转换
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_value,
                x=testdf.columns.tolist(),
                y=testdf.index.tolist(),
            ))  # 缺失值处理参数
            # fig.show()
            fig.update_layout(xaxis_tickangle=45)
            # # 字体大小设置
            # for i in range(len(fig.layout.annotations)):
            #     fig.layout.annotations[i].font.size = 12
            # 根据任务id去读取文件之类的操作，然后返回图表
            return fig
        else:
            return dash.no_update
    else:
        return dash.no_update


'''
以下函数为PCA的回调
'''
@app.callback(
    Output('model-pca-analyse','visible'),
    Input('analyse_task','data'),
)
def openmodel(data):
    '''
    根据data返回model的组件
    :param data:
    :return:
    '''
    if data:
        if data['taskname'] == 'PCA分析':
            return True
        else:
            return dash.no_update
    else:
        return dash.no_update

@app.callback(
    Output('pca_2Dscater','figure'),
    Output('pca_3Dscater','figure'),
    Input('analyse_task','data'),
)
def show_heatmap_figure(data):
    if data:
        if data['taskname'] == 'PCA分析':
            taskid = data['taskid']
            # todo 读取任务文件就好了
            distance_df = pd.read_csv(f'D:/file/digital_server/model/panel_data/wKg9b2OOmKGAXHTgABbmqEay3Ec844 .csv')
            allspecial = distance_df.columns[4:]

            def caculate(array, colname):
                Ref = array['SNP'][0]
                Snpbase = array['SNP'][2]
                if len(array[colname]) != 2:
                    return random.randint(0, 2)
                if array[colname][0] != array[colname][1]:  # 说明杂合
                    return 1
                elif array[colname][0] == Ref:
                    return 0
                elif array[colname][0] == Snpbase:
                    return 2

            for i in allspecial:
                distance_df[i] = distance_df.apply(caculate, colname=i, axis=1)

            # 计算距离矩阵
            def caculate_same(df: pd.DataFrame):
                dict = {}
                column = df.columns
                for i in column:
                    list1 = []
                    refer = list(df[i])
                    for k in column:
                        compare = list(df[k])
                        # 分子，即AB两个品种相同位点上不同基因的个数
                        notsimilar = [item1 for item1, item2 in zip(refer, compare) if item1 != item2]
                        # 遗传距离   不同基因/所有基因
                        distance = len(notsimilar) / len(compare)
                        list1.append(distance)
                    dict[i] = list1
                return pd.DataFrame(dict, index=column)

            distance_shape = caculate_same(distance_df.iloc[:, 4:])
            # 进行聚类分析


            # 通过linkage函数进行聚类
            Z = linkage(distance_shape, method='ward')

            # 对聚类结果进行评估
            cluster_labels = fcluster(Z, criterion='maxclust', t=15)

            #计算情缘关系G矩阵
            specialname = distance_df.iloc[:, 4:].columns
            M = distance_df.iloc[:, 4:].T - 1  # M矩阵
            p1 = np.round((np.sum(M, axis=0) + M.shape[0]) / (M.shape[0] * 2), 3)
            # 计算P矩阵
            p = 2 * (p1 - 0.5)
            P = np.tile(p, (M.shape[0], 1))
            # # 就是那Z矩阵
            Z = M - P
            # # 计算G矩阵公式的分母
            c = p1 * (1 - p1)
            d = 2 * np.sum(c)
            # # 计算G矩阵公式的分子
            ZZt = np.dot(Z, Z.T)
            # # 计算G矩阵
            G = ZZt / d
            Gpandas = pd.DataFrame(np.round(G, 3), columns=specialname, index=specialname)
            # 将G矩阵变量gene作为PCA的输入
            '''PCA二维'''
            pca = PCA(n_components=2)
            # 进行PCA分析
            pca_result = pca.fit_transform(Gpandas)
            pca2_df = pd.DataFrame(pca_result, index=specialname, columns=['PC1', 'PC2'])
            pca2_df['cluster'] = cluster_labels
            pca2_df['scasize'] = 10
            pca2_df.sort_values(by=['cluster'])
            pca2_df['cluster'] = pca2_df['cluster'].astype('str')
            pca2d = px.scatter(pca2_df,  # 数据集
                             x='PC1',  # x轴
                             y='PC2',  # y轴
                             color="cluster",  # 指定颜色
                             size='scasize',
                             hover_name=pca2_df.index
                             )
            # 将G矩阵变量gene作为PCA的输入
            pca3 = PCA(n_components=3)

            # 进行PCA分析
            pca_result3 = pca3.fit_transform(Gpandas)
            pca3_df = pd.DataFrame(pca_result3, index=specialname, columns=['PC1', 'PC2', 'PC3'])
            pca3_df['scasize'] = 10
            pca3_df['cluster'] = cluster_labels
            pca3_df.sort_values(by=['cluster'])
            pca3_df['cluster'] = pca3_df['cluster'].astype('str')
            pca3d = px.scatter_3d(pca3_df,  # 数据集
                                x='PC1',  # x轴
                                y='PC2',  # y轴
                                z='PC3',
                                color="cluster",  # 指定颜色
                                size='scasize',
                                hover_name=pca3_df.index
                                )
            return pca2d,pca3d
        else:
            return dash.no_update
    return dash.no_update
