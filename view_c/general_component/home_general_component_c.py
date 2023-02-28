from server import app
from dash import Input, Output, State, html, dcc
from model.PERMISSION_LINK import PERMISSION_LINK
from flask_login import current_user
import feffery_antd_components as fac

def translation_map() -> dict:
    return {
                'home': '主页',
                'about': '关于我们',
                'new': '新闻',
                'article': '文章',
                'people': '专家',
                'partners': '合作伙伴',
                'cite': '如何引用',
                'analyse': '分析工具',
                'seedresource': '种质资源',
                'Phenotyping': '表型分析',
                'Genotyping': '基因型分析',
                'MultiOmicAnalysis': '多组学分析',
                'publice': '公开信息',
                'literature': '文献下载',
                'seedtrade': '种质交易',
                'seedinfo': '种质信息',
                'equipment': '设备信息'
            }

'''
面包屑更新
'''
@app.callback(
    Output('header_bread_now','children'),
    Output('header_bread_component', 'items'),
    Input('app_page_store', 'data'),
)
def url_for_header_bread_component(pathname:str):
    path_info = pathname.split('/')
    items_map = translation_map()
    items = [
        {
            'title': items_map[i]
        } for i in path_info if i != ''
    ]
    return items_map[path_info[-1]], items


'''
首页页尾合作伙伴更新
'''
@app.callback(
    Output('home_link_info','children'),
    Input('app_page_store', 'data'),
)
def link_infomation(data):
    query_result = PERMISSION_LINK.select(PERMISSION_LINK.LINK_NAME,
                                               PERMISSION_LINK.LINK_URL,
                                               )
    return [
        html.A(item.LINK_NAME,href=item.LINK_URL) for item in query_result
    ]

'''
进入系统按钮回调事件
'''
@app.callback(
    Output('home_enter_sys_route','children'),
    Input('home-to-system-btn','n_clicks'),
    prevent_initial_call=True
)
def home_enter_sys_route(n):
    print(n)
    if n:
        if current_user.is_authenticated:
            return dcc.Location(href='/analysesystem',id = 'home_enter_sys_route_dcc')
        else:
            return fac.AntdMessage(
                    content='请先进行登录',
                    type='error'
                )