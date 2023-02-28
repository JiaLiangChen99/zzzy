import dash_bootstrap_components as dbc
from dash import html, dcc
import feffery_antd_components as fac
from view_c.home import index_c
from view.general_components.home_general_component import HomeGeneralCom
import plotly.express as px
import pandas as pd

home_df = pd.read_csv('static/home/data/gapminderDataFiveYear.csv')
filtered_df = home_df[home_df.year == 1952]

fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                 size="pop", color="continent", hover_name="country",
                 log_x=True, size_max=55)

fig.update_layout(transition_duration=500)

def index_page(**kwargs):
    userid = kwargs.get('userid',None)
    index = [
        HomeGeneralCom.header(userid=userid),
        HomeGeneralCom.enter_sys_btn(),
        HomeGeneralCom.change_locale(),
        dbc.Row([
            html.Div([
                html.Img(src='https://next-gen.materialsproject.org/assets/images/home/lattices.png'),
                html.H1('湾区种质数字港'),
                html.P(
                    '不但要在科学家和企业家之间构建平台、汇聚资源、媒介撮合，而且更重要的是要围绕双方合作，构建起产出来、卖出去、活起来的全链要素汇聚、资源匹配（生产、加工、品牌、物流、商流、金融等等16个环节）闭环支撑体系：通过“市场导向”引导健康的“产学研”研究，通过“超级媒介”撮合科学家和企业家谈成恋爱，通过“要素匹配”为双方合作赠送“嫁妆”，为他们的“联姻”送彩礼、扶一把、助一程。'),
                html.Div([html.Button('登录或注册',id='index_login_btn'), html.Button('查看平台更多信息')]
                         if not userid else
                         [html.Button('查看平台更多信息')]
                         )
            ])
        ]),
        dbc.Row(
            dbc.Container(
                [
                    dbc.Row(html.H3('数字港共享数据')),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([fac.AntdStatistic(
                                    title='统计数值示例',
                                    value=1332971
                                )], width=6),
                                dbc.Col([fac.AntdStatistic(
                                    title='统计数值示例',
                                    value=1332971
                                )], width=6),
                                dbc.Col([fac.AntdStatistic(
                                    title='统计数值示例',
                                    value=1332971
                                )], width=6),
                                dbc.Col([fac.AntdStatistic(
                                    title='统计数值示例',
                                    value=1332971
                                )], width=6),
                            ])
                        ], width=6),
                        dbc.Col([dcc.Graph(id='home_graph',figure=fig),
                                 html.Div(id='selected-data')], width=6)
                    ])
                ]
            )
        ),
        dbc.Container(
            dbc.Row([
                dbc.Col([html.Div([html.H3('种质资源管理'), html.P(
                    '种质资源管理模块，庞大的种质资源信息库，能够容纳数以万亿的品种资源；库存管理系统方便进行日常的出入库流程操作；配置有智能预警监测，24小时无人值守。')])],
                        width=6),
                dbc.Col([html.Img(src='/static/home/img/equipment/微滴式数字PCR系统.jpg')], width=6)
            ])
        ),
        dbc.Container(
            dbc.Row([
                dbc.Col([html.Div([html.H3('表型管理分析'), html.P(
                    '系统功能上涵盖表型试点管理、试验管理等模块；分析板块集成了以数据驱动的可视化设计：如柱状图、折线图、雷达图等。')])],
                        width=6),
                dbc.Col([html.Img(src='http://www.gdzzyh.com/cms/gzkczx/images/index/darb_bg.jpg')], width=6)
            ])
        ),
        dbc.Container(
            dbc.Row([
                dbc.Col([html.Div([html.H3('基因型管理分析'), html.P(
                    '基因型数据管理模块，采用分布式数据库架构，可以轻松管理和使用多种可视化基因分析视图工具，功能涵盖SNP管理、基因数据管理、基因分析等。')])],
                        width=6),
                dbc.Col([html.Img(src='http://www.gdzzyh.com/cms/gzkczx/images/index/germ_bg.jpg')], width=6)
            ])
        ),
        HomeGeneralCom.footer()
    ]
    return index
