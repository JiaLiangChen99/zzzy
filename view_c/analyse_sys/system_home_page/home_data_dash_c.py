from server import app
from dash import Input,Output
from view.analyse_sys.system_home_page \
    import home_data_dash, home_gene_analyse_help,home_character_analyse_help,home_data_manage_help

@app.callback(
    Output('sys-right-show','children'),
    Input('system-home-menu-children','currentKey')
)
def system_children_function(key2):
    if key2 == '平台数据仪表盘':
        return home_data_dash.home_data_dash_page_ui()
    if key2 == '基因型分析使用文档':
        return home_gene_analyse_help.home_gene_analyse_help()
    if key2 == '表型分析使用文档':
        return home_character_analyse_help.home_character_analyse_help()
    if key2 == '如何进行数据管理':
        return home_data_manage_help.home_data_manage_help()



