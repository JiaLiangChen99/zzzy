import dash
import feffery_antd_components as fac
from server import app
from dash import Input,Output,State,ALL
from dash import html
from view.analyse_sys.system_home_page import home_data_dash
from view.analyse_sys.system_gene_analyse import gene_analyse_base
from view.analyse_sys.system_data_manage import data_manage_base

"""
system页面通用回调
1、 在model框里更新可选物种情况
2、物种选择事件   点击按钮弹出对话框，选择相应的物种进行分析
3、页面状态store  根据store来刷新页面情况
4、机构选择事件   参考物种选择事件
"""

system_out_menu_page = {
    '主页' : {'defaultSelectedKey':'主页','children':home_data_dash.home_data_dash_ui},
    '基因型分析|分析工具' : {'defaultSelectedKey':'基因型分析','children':gene_analyse_base.gene_analyse_base_ui},
    '数据管理':{'defaultSelectedKey':'数据管理','children':data_manage_base.data_manage_base_ui}
}

@app.callback(
    Output('system-analyse-special-model','visible'),
    Input('system-select-special-btn','nClicks'),
    Input('system-select-special-store','data'),
)
def select_system_analyse_special(n,special):
    """
    :param n: 按钮点击事件
    :param special: 当前store存储的物种信息,页面初始化时应该为None
    :return: model是否打开

    触发事件回调情况
    1、点击了按钮打开了模态框
    2、当页面的store data为空 说明是初始化状态，需要自动打开物种选择对话框
    """
    if dash.ctx.triggered_id == 'system-select-special-btn':
        return True
    if not special:
        return True


@app.callback(
    Output('show-select-special','children'),
    Input('system-select-special-store','data'),
)
def select_system_analyse_special(special):
    """
    :param n: 按钮点击事件
    :param special: 当前store存储的物种信息,页面初始化时应该为None
    :return: model是否打开

    触发事件回调情况
    1、点击了按钮打开了模态框
    2、当页面的store data为空 说明是初始化状态，需要自动打开物种选择对话框
    """
    if special:
        return special



@app.callback(
    Output('system-select-special-store','data'),
    Input({'type':'special-select','index':ALL},'nClicks'),
    prevent_initial_call=True
)
def select_special_to_store(n):
    """
    物种选择模态框的点击事件
    当点击了具体那个物种后会将当前页面的物种store进行更新
    从而进行物种数据加载
    :param n:  点击事件：点击的次数，默认不点击为None
    :return: 物种Store的信息
    """
    if n:
        special = dash.ctx.triggered_id['index']
        return special
    return dash.no_update



@app.callback(
    Output('show-select-chrosm','children'),
    Input('system-select-chrosm-store','data'),
)
def return_chrosm(data):
    if data:
        return data
    return dash.no_update



#页面 pagestore
@app.callback(
    Output('now-page-href','data'),
    Input('sysheader-funtion-menu','currentKey'),
    prevent_initial_call=True
)
def up_data_system_page_store(key):
    if key:
        return key

@app.callback(
    Output('sysheader-funtion-menu','defaultSelectedKey'),
    Input('now-page-href','data'),
)
def init_sysheader_menu(data):
    """
    根据data来动态渲染 当前菜单项的选项
    :param data: 当前页面对应的store信息
    :return:
    """
    if data in system_out_menu_page.keys():
        return system_out_menu_page[data]['defaultSelectedKey']
    else:
        return dash.no_update

@app.callback(
    Output('sys-home-page','children'),
    Input('now-page-href','data'),
)
def store_to_show_function_page(data:str):
    """
    根据data来动态渲染 页面内容
    :param data: 当前页面对应的store信息
    :return:
    """

    print(data)
    if data.startswith('基因型分析|分析工具'):
        return system_out_menu_page['基因型分析|分析工具']['children']()
    if data.startswith('数据管理'):
        return system_out_menu_page['数据管理']['children']()
    return system_out_menu_page[data]['children']()
