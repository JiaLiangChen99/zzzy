import feffery_antd_components as fac
from dash import html, dcc
import feffery_utils_components as fuc
from view_c import login_c


def login_ui(**kwargs):
    if kwargs.get('userid',None) == None:
        login_com = html.Div([
            html.Div([
                html.Div(id='login_page_router'),
                dcc.Store(id='register_code'),
                dcc.Store(id='login_code'),
                fac.AntdModal(
                    [
                        fac.AntdForm(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(id = 'register_username',maxLength=20),
                                    label='用户名',
                                    id = 'form_register_username'
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        mode='password',
                                        id='register_password'
                                    ),
                                    label='密码',
                                    id='form_register_password'
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        mode='password',
                                        id='register_repeat_password'
                                    ),
                                    label='确认密码',
                                    id='form_register_repeat_password'
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='register_phone'
                                    ),
                                    label='联系方式',
                                    id='form_register_repeat_phone'

                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='register_email'
                                    ),
                                    label='邮箱',
                                    id='form_register_repeat_email'
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='register_unit'
                                    ),
                                    label='工作单位',
                                    id = 'form_register_repeat_unit'
                                ),
                                fac.AntdFormItem(
                                    fac.AntdButton(
                                        '注册',
                                        id = 'register',
                                        type='primary'
                                    )
                                )
                            ],
                            wrapperCol={
                                'span': 12
                            },
                            layout='vertical'
                        ),
                    ],
                    id='register_model',
                    visible=False,
                    title=html.Span(
                        [
                            fac.AntdIcon(icon='fc-search'),
                            '注册测试'
                        ]
                    ),
                    renderFooter=True
                )
            ]),
            html.Div([
                fac.AntdForm(
                    [
                        fac.AntdFormItem(
                            fac.AntdInput(id='login_username'),
                            label='用户名',
                            id = 'form_login_username'
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='login_password',
                                mode='password'
                            ),
                            label='密码',
                            id = 'form_login_password'
                        ),
                        html.Div(
                            [
                                fuc.FefferyCaptcha(id='login_captcha'),
                                fac.AntdInput(id='to_login_captcha'),
                                html.Div(id='form_login_captcha')
                            ]
                        ),
                        fac.AntdFormItem(
                            [fac.AntdButton(
                                '登录',
                                id = 'login_btn',
                                type='primary'
                            ),
                                fac.AntdButton(
                                    '注册',
                                    id='register_btn',
                                    type='primary'
                                ),
                            ],
                            wrapperCol={
                                'offset': 4
                            }
                        )
                    ],
                    labelCol={
                        'span': 4
                    },
                    wrapperCol={
                        'span': 8
                    },
                    labelAlign='left'
                )

            ],className='login_form')
        ])
        return login_com
    else:
        return dcc.Location(href='/login',id='is_login_to_index_route')