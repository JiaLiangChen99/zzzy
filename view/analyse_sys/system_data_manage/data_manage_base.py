import dash
import feffery_antd_components as fac
from dash import html,Input,Output,State
from server import app
from view.analyse_sys.system_data_manage import data_manage_ui
#总体的渲染
def data_manage_base_ui(**kwargs):
    return [
            fac.AntdCol(
                html.Div(
                    fac.AntdMenu(
                                menuItems=[
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'团队管理',
                                            'title': f'团队管理'
                                        }
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'项目数据管理',
                                            'title': f'项目数据管理'
                                        }
                                    }
                                ],
                                mode='inline',
                                id='data-manage-menu-children',
                            ),
                    className='sys_body_left',
                    id='gene-left-show'
                ),
                flex='1'
            ),
            #当右侧点击栏刷新，修改html.Div的局部内容
            fac.AntdCol(
                html.Div(
                    children=[],
                    className='sys_body_right',
                    id = 'data-manage-right-show'
                ),
                flex='5'
            )
        ]

@app.callback(
    Output('data-manage-right-show','children'),
    Output('data-manage-menu-children','defaultSelectedKey'),
    Input('now-page-href','data'),
)
def gene_analyse_menu_set(data:str):
    analyse_uipage = {
        '团队管理': data_manage_ui.team_manage_ui,
        '项目数据管理':data_manage_ui.data_magene_ui, #todo
    }
    if data.startswith('数据管理'):
        analyse_function = data.split('|')[-1]
        return analyse_uipage[analyse_function](),analyse_function
    return dash.no_update,dash.no_update