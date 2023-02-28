import json

import dash

from server import app
from dash import Input, Output, dcc, State
from flask_login import logout_user




@app.callback(
    Output('index_logout_route','children'),
    Output('now_url','data'),
    Input('index_logout','data'),
    Input('index_login','data')
)
def index_upgrade(data1,data2):
    """
    Store管理  登录登出回调事件
    :param data1: 登出的路由  且需要返回到登出前的页面
    :param data2:  登录的路由
    :return:
    """
    if data1 or data2:
        if dash.ctx.triggered_id == 'index_logout':
            return dcc.Location(href=data1,id='index_logout_router'), data1
        elif dash.ctx.triggered_id == 'index_login':
            return dcc.Location(href='/login',id='index_login_router'), data2
    return dash.no_update


@app.callback(
    Output('index_login','data'),
    Input('header_to_login','n_clicks'),  #该组件位于header头组件中，需要去通用组件找他
    Input('index_login_btn','n_clicks'),
    State('app_page_store','data'),
    prevent_initial_call=True
)
def header_index_route_logout(n2,n3,pathname):
    """
    首页中 头部登录和下方登录按钮跳转事件：
    传递参数到中转 Store中，利用store管理回调
    """
    if n2 or n3:
        if dash.ctx.triggered_id == 'header_to_login':
            return pathname
        elif dash.ctx.triggered_id == 'index_login_btn':
            return dcc.Location(href='/login'), pathname
    return dash.no_update,dash.no_update


@app.callback(
    Output('index_logout','data'),
    Input('header_logout', 'n_clicks'),
    State('app_page_store','data'),
    prevent_initial_call=True
)
def header_index_logout(n,pathname):
    """
    登出按钮事件    点击后登出
    """
    if n:
        logout_user()
        return pathname

@app.callback(
    Output('selected-data', 'children'),
    Input('home_graph', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)