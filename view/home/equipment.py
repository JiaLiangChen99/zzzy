from dash import html
import dash_bootstrap_components as dbc
from view.general_components.home_general_component \
    import HomeGeneralCom
from view_c.home import equipment_c

def equipment_ui(**kwargs):
    userid = kwargs.get('userid',None)
    equipment_ui = html.Div([
        HomeGeneralCom.header(userid=userid),
        HomeGeneralCom.header_bread(),
        HomeGeneralCom.enter_sys_btn(),
        HomeGeneralCom.change_locale(),
        dbc.Container(
            [
            dbc.Row(
                [
                dbc.Col(
                    html.Div(
                        [html.Div(html.Img(src='/static/home/img/equipment/微滴式数字PCR系统.jpg')),
                         html.Div(
                             [
                                 html.H5('微滴式数字PCR系统'),
                                 html.P('能够对DNA进行直接绝对定量； 每个反应体系生成的微滴数≥20000个； 至少50个PCR反应后微滴仍能够保持稳定而不互相融合； 至少支持双重荧光检测； 自动化产生微滴，45分钟完成≥96个ddPCR反应的微滴制备； 精确度：≥90%。'),
                             ]
                         )
                         ]
                    )
                )
                    ], id='equipment_info'
             ),
            ]
        ),
        HomeGeneralCom.footer()
    ])
    return equipment_ui