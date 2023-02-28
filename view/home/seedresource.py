import feffery_antd_components as fac
from dash import html
import dash_bootstrap_components as dbc
from view.general_components.home_general_component \
    import (header,footer,header_bread)

def seedresource_UI(**kwargs):
    userid = kwargs.get('userid',None)
    seedresource_ui = html.Div([
        header(userid=userid),
        header_bread(),
        dbc.Container(
            [
            dbc.Row(
                [
                dbc.Col(
                    html.Div(
                        [
                        html.H1('刘玉涛'),
                        html.P('刘玉涛，男，博士，广东省博士团团长。先后获得“首届广东省农村青年科技文化活动月先进个人”、“十百千万”优秀驻村干部、广东省科学技术奖一等奖、2016年度“中国农村新闻人物”等称号。具有丰富的农业项目统筹、协调管理经验，具有深厚的农业产业研究能力。')
                        ]
                    )
                ),
                dbc.Col(
                    html.Div(
                        [
                        html.H1('刘玉涛'),
                        html.P(
                            '刘玉涛，男，博士，广东省博士团团长。先后获得“首届广东省农村青年科技文化活动月先进个人”、“十百千万”优秀驻村干部、广东省科学技术奖一等奖、2016年度“中国农村新闻人物”等称号。具有丰富的农业项目统筹、协调管理经验，具有深厚的农业产业研究能力。')
                        ]
                    )
                )
                    ], id='expert_info'
             ),
            ]
        ),
        footer()
    ])
    return seedresource_ui