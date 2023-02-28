import feffery_antd_components as fac
from dash import html

def home_data_manage_help(**kwargs):
    return [
            html.P('基因型分析帮助文档'),
            html.Div(id='sys-function-page')
        ]