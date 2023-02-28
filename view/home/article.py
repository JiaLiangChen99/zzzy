import feffery_antd_components as fac
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc
from view.general_components.home_general_component import HomeGeneralCom
from view_c.home import article_c

def article_UI(**kwargs):
    userid = kwargs.get('userid',None)

    article_ui = html.Div([
        HomeGeneralCom.header(userid=userid),
        HomeGeneralCom.header_bread(),
        HomeGeneralCom.enter_sys_btn(),
        HomeGeneralCom.change_locale(),
        dbc.Container(
            [
            dbc.Row(
                id='article_main'
            )
            ]
        ),
        HomeGeneralCom.footer()
    ])
    return article_ui