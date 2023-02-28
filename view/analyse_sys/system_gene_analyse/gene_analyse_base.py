import dash
import feffery_antd_components as fac
from dash import html,Input,Output,State
from server import app
from view.analyse_sys.system_gene_analyse import gene_analyse_ui,gene_distance_ui
#总体的渲染
def gene_analyse_base_ui(**kwargs):
    return [
            fac.AntdCol(
                html.Div(
                    fac.AntdMenu(
                                menuItems=[
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'品种基因型比较',
                                            'title': f'品种基因型比较'
                                        }
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'进化树',
                                            'title': f'进化树'
                                        }
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'遗传距离',
                                            'title': f'遗传距离'
                                        }
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'PCA分析',
                                            'title': f'PCA分析'
                                        }
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'ADMIXTURE分析',
                                            'title': f'ADMIXTURE分析'
                                        }
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'目标基因分析',
                                            'title': f'目标基因分析'
                                        }
                                    },
                                ],
                                mode='inline',
                                id='gene-analyse-menu-children',
                            ),
                    className='sys_body_left',
                    id='gene-left-show'
                ),
                span=4
            ),
            #当右侧点击栏刷新，修改html.Div的局部内容
            fac.AntdCol(
                html.Div(
                    children=[],
                    className='sys_body_right',
                    id = 'gene-right-show'
                ),
                span=20
            )
        ]


'''
侧边栏点击时刷新渲染
'''
@app.callback(
    Output('gene-right-show','children'),
    Output('gene-analyse-menu-children','defaultSelectedKey'),
    Input('now-page-href','data'),
)
def gene_analyse_menu_set(data:str):
    analyse_uipage = {
        '品种基因型比较': gene_analyse_ui.gene_compare_ui,
        '遗传距离':gene_distance_ui.gene_distance_ui
    }
    if data.startswith('基因型分析|分析工具'):
        analyse_function = data.split('|')[-1]
        print(analyse_function)
        return analyse_uipage[analyse_function](),analyse_function
    return dash.no_update,dash.no_update

