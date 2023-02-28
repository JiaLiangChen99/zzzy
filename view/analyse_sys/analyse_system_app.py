from server import app
import feffery_antd_components as fac
from dash import html, dcc, Input, Output
from view_c.analyse_sys import analyse_system_app_c
from model.USER_INFO import USER_INFO
from flask_login import current_user
import app_config



def system_app_main(**kwargs):
    if kwargs.get('userid',None):
        username = kwargs['userid']
        system_ui = html.Div([
            dcc.Store(id='system-select-chrosm-store',
                      data=list(USER_INFO.select(
                          USER_INFO.USER_NAME,USER_INFO.USER_UNIT)
                                .where(USER_INFO.USER_NAME==current_user.id)
                                .dicts())[0]['USER_UNIT']),  #存储用户的机构信息
            dcc.Store(id='now-page-href',data='主页'), #存储组件状态,想要改内容直接修改这里的值
            dcc.Store(id='system-select-special-store'),
            html.Div(
            [
                html.Div([
                    fac.AntdRow([
                        fac.AntdCol(
                            html.Div(
                                [
                                    html.Img(src='/static/system/img/system_logo.jpg', className='sys_header_logo'),
                                    html.Span('湾区数字港分析大厅平台', className='system_header_font')
                                ],
                                className='system_header_left'
                            )
                        ),
                        fac.AntdCol(
                            html.Div([
                                html.Div([
                                    fac.AntdTooltip(
                                        fac.AntdButton(
                                            fac.AntdIcon(icon='antd-question-circle'),
                                            type='primary',
                                            className='system_header_help_btn'
                                        ),
                                        title='帮助文档',
                                        placement='bottom'
                                    ),
                                    fac.AntdTooltip(
                                        [
                                            fac.AntdBadge([
                                                fac.AntdButton(
                                                    fac.AntdIcon(icon='antd-bell',id='sys_session_icon'),
                                                    type='primary',
                                                    className='system_header_help_btn',
                                                ),
                                            ],id='queen_session_badge',count=66,overflowCount=50)
                                        ],
                                        id='sys-session-tooltip',
                                        title='消息通知',
                                        placement='bottom'
                                    ),
                                    fac.AntdTooltip(
                                        fac.AntdButton(
                                            fac.AntdIcon(icon='antd-question-circle'),
                                            type='primary',
                                            className='system_header_help_btn',
                                        ),
                                        title='机构选择',
                                        placement='bottom'
                                    ),
                                    html.Div(id='show-select-chrosm'), #机构名称
                                    fac.AntdTooltip(
                                        fac.AntdButton(
                                            fac.AntdIcon(icon='antd-question-circle'),
                                            type='primary',
                                            className='system_header_help_btn',
                                            id = 'system-select-special-btn'
                                        ),
                                        title='物种选择',
                                        placement='bottom',
                                    ),
                                    html.Div(id='show-select-special'),  #选择的物种名称
                                ], className='sys_header_help_btn'),
                                html.Div([
                                    html.Span(username, className='header_userinfo'),
                                    html.Span('分析师', className='header_usercharacter')
                                ], className='sys_header_user_info')
                            ], className='system_header_right')
                        )
                    ], justify='space-between', className='system_header'),
                    fac.AntdModal(
                        children=html.Div(
                            [
                                fac.AntdButton('水稻', id={'type': 'special-select', 'index': '水稻'}),
                                fac.AntdButton('玉米', id={'type': 'special-select', 'index': '玉米'}),
                                fac.AntdButton('小麦', id={'type': 'special-select', 'index': '小麦'}),
                                fac.AntdButton('花生', id={'type': 'special-select', 'index': '花生'}),
                            ]
                            , style={'width': '760px', 'display': 'flex'}),
                        id='system-analyse-special-model',
                        visible=False,
                        renderFooter=False
                    ),
                    fac.AntdRow(
                        fac.AntdCol(
                            [html.Div([
                                html.Div(
                                    [fac.AntdButton(fac.AntdIcon(icon='antd-menu'), className='system_header_next_btn')]),
                                html.Div([
                                    fac.AntdMenu(
                                        menuItems=app_config.AnalyseSystemConfig.menuItems,
                                        mode='horizontal',
                                        className='sys_header_next_menu',
                                        id='sysheader-funtion-menu',
                                    )
                                ])
                            ], className='sys_header_next')
                            ]
                        )
                    )
                ],className='system_all_header_style'),
            fac.AntdRow(gutter=10,id='sys-home-page',className='system_main_style')
                ])

        ])
        return system_ui
    else:
        return dcc.Location(href='/login',id='system_exit_to_login')


# @app.callback(
#     Output()
#     Input('global_app_url','hash')
# )
