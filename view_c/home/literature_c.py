import dash
from server import app
from dash import Input,Output,State
import feffery_antd_components as fac

@app.callback(
    Output('literature_page_store','data'),
    Input('literature_pagesize','current'),
    Input('literature_pagesize', 'pageSize'),
    prevent_initial_call=True
)
def select_literature_page_store(current,pageSize):
    return {'current':current, 'pagesize': pageSize}


@app.callback(
    Output('literature_from_store','data'),
    Input('search_literature','nClicks'),
    State('literature_form_name','value'),
    State('literature_type','value'),
    prevent_initial_call=True
)
def search_form_literature_store(n,article,type):
    if n:
        if article or type:
            return {'input':article,'select':type}
        return dash.no_update

@app.callback(
    Output('literature_info','children'),
    Input('literature_store','data'),
    Input('literature_page_store','data'),
    Input('literature_from_store','data'),
)
def show_literature_info(data1,data2,data3):
    if data1 or data2 or data3:
        if dash.ctx.triggered_id == None:
            return '初始化'
        elif dash.ctx.triggered_id == 'literature_from_store':
            return '表单搜索'
        elif dash.ctx.triggered_id == 'literature_page_store':
            print(data3)
            return '页码搜素'

@app.callback(
    Output('new_literature_com','children'),
    Input('search_literature','nClicks'),
    prevent_initial_call=True
)
def form_search_change_page(n):
    if n:
        return fac.AntdPagination(
                    defaultPageSize=10,
                    total=100,
                    id = 'literature_pagesize'
                )