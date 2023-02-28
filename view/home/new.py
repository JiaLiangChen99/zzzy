import feffery_antd_components as fac
from dash import html
import dash_bootstrap_components as dbc
from view.general_components.home_general_component \
    import HomeGeneralCom
from view_c.home import new_c

def home_new_UI(**kwargs):
    userid = kwargs.get('userid',None)
    new_ui = html.Div([
        HomeGeneralCom.header(userid=userid),
        HomeGeneralCom.header_bread(),
        dbc.Container(
            [
            dbc.Row(
                html.H1('新闻动态')
            ),
            dbc.Row(
                id = 'home_new_info'
            ),
            dbc.Row(
                fac.AntdPagination(
                    defaultPageSize=10,
                    total=100,
                    id = 'new_pagesize'
                ),id='new_page_com'
            )
            ]
        ),
        HomeGeneralCom.footer()
    ])
    return new_ui