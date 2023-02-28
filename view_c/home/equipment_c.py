from dash import Input,Output,html
from model.PERMISSION_EQUIPMENT import PERMISSION_EQUIPMENT
from server import app
import dash_bootstrap_components as dbc

@app.callback(
    Output('equipment_info','children'),
    Input('equipment_store','data'),
)
def show_expert(data):
    if data:
        query_result = PERMISSION_EQUIPMENT.select(PERMISSION_EQUIPMENT.EQUIPMENT_NAME, PERMISSION_EQUIPMENT.EQUIPMENT_DESCRIBE,
                                                   PERMISSION_EQUIPMENT.IMAGE_ID,
                                                   )
        return [
            dbc.Col(
                [html.Div(
                    [html.Div(html.Img(src=item.IMAGE_ID)),  #图片图片路径
                     html.Div(
                         [
                             html.H5(item.EQUIPMENT_NAME),  #设备名
                             html.P(item.EQUIPMENT_DESCRIBE),  #描述信息
                         ]
                     )
                     ]
                )],width=12
            ) for item in query_result
        ]