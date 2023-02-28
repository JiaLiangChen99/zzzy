import dash

from server import app, server
from dash import html, dcc, Input, Output
from app_config import AppInitConfig
from view import _404page
from flask_login import current_user

app.layout = html.Div([
    dcc.Store(id='now_url',storage_type='session'),
    dcc.Store(id='system_hash'),
    html.Div(id='home_enter_sys_route'),#首页进入系统按钮跳转
    html.Div([
        dcc.Store(id= 'app_page_store'),
        dcc.Store(id = 'article_page_store'),
        dcc.Store(id='expert_page_store'),
        dcc.Store(id='equipment_store'),
        dcc.Store(id='literature_store'),
    ]),  # 借由url触发的中转
    dcc.Location(id='global_app_url'),
    html.Div(id='global_app_route'),
    html.Div(id='main'),
])




@app.callback(
    Output('main','children'),
    Input('app_page_store','data')
)
def app_run(pathname):
    '''
    检查url的合法性
    :param pathname:
    :return:
    '''
    pass_url = AppInitConfig.PASS_URL  #注册的路由
    if pathname not in pass_url.keys():
        return _404page._404page()
    if current_user.is_authenticated:
        return pass_url[pathname](userid=current_user.id)
    else:
        return pass_url[pathname]()



@app.callback(
    Output('app_page_store','data'),
    Output('article_page_store','data'),
    Output('expert_page_store','data'),
    Output('equipment_store','data'),
    Output('literature_store','data'),
    Output('system_hash','data'),
    Input('global_app_url','pathname'),
    Input('global_app_url','hash'),
)
def article_page_store(pathname, hash):
    if pathname == '/home/about/people':
        return pathname, dash.no_update, pathname, dash.no_update,dash.no_update, dash.no_update
    if pathname == '/home/about/new/article':
        return pathname, hash, dash.no_update, dash.no_update,dash.no_update, dash.no_update
    if pathname == '/home/about/equipment':
        return pathname, dash.no_update, dash.no_update, pathname, dash.no_update, dash.no_update
    if pathname == '/home/publice/literature':
        return pathname, dash.no_update, dash.no_update, dash.no_update, pathname ,dash.no_update
    if pathname == '/analysesystem':
        return pathname, dash.no_update, dash.no_update, dash.no_update, dash.no_update ,hash
    return pathname, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update



if __name__ == '__main__':
    app.run_server(debug=True,port = '3001')