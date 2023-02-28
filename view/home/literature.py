import feffery_antd_components as fac
from dash import html,dcc
import dash_bootstrap_components as dbc
from view.general_components.home_general_component \
    import HomeGeneralCom
from view_c.home import literature_c

def literature_UI(**kwargs):
    userid = kwargs.get('userid',None)
    literature_ui = html.Div([
        dcc.Store(id='literature_from_store'),  #表单查询store
        dcc.Store(id='literature_page_store'), #页数选择store
        HomeGeneralCom.header(userid=userid),
        HomeGeneralCom.header_bread(),
        HomeGeneralCom.change_locale(),
        HomeGeneralCom.enter_sys_btn(),
        dbc.Container(
            [
            dbc.Row([
                fac.AntdInput(id='literature_form_name'),
                fac.AntdSelect(
                    placeholder='分类',
                    options=[
                        {'label': '水稻', 'value': '水稻'},
                        {'label': '花生', 'value': '花生'}],
                    style={
                        # 使用css样式固定宽度
                        'width': '200px'
                    },
                    id = 'literature_type'
                ),
                fac.AntdButton('搜索',id='search_literature')
            ]),
            dbc.Row(
                id = 'literature_info'
            ),
            dbc.Row(
                fac.AntdPagination(
                    defaultPageSize=10,
                    total=100,
                    id = 'literature_pagesize'
                ),id='new_literature_com'
            )
            ]
        ),
        HomeGeneralCom.footer()
    ])
    return literature_ui