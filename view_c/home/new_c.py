import dash

from server import app
from dash import Input,Output,State
import feffery_antd_components as fac


@app.callback(
    Output('home_new_info','children'),
    Input('new_pagesize','current'),
    Input('new_pagesize', 'pageSize'),
)
def show_new(current,pageSize):
    return [
        fac.AntdText(f'内容项{i}')
        for i in range((current - 1) * pageSize, current * pageSize)
    ]

