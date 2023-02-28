import dash_bootstrap_components as dbc
from dash import html,dcc
import feffery_antd_components as fac
from view_c.general_component import home_general_component_c

PLOTLY_LOGO = "http://www.gdzzyh.com/cms/gzkczx/images/logo.png"

class HomeGeneralCom:
    """
    首页组件类
    """
    @staticmethod
    def header(**kwargs):
        """
        页头设置：
        传入参数: userid  用户名
        :param kwargs:
        :return:
        """
        userid = kwargs.get('userid',None)
        navbar = html.Div([
            dbc.Row(
                dbc.Col(
                    html.Div([html.Span('欢迎来到湾区种质数字港'), html.A('在这里你可以看到我们的动态信息')],
                             className='index_header_introduce')
                    ,
                )
            ),
            dbc.Row(dbc.Navbar(
            [
                dcc.Store(id='index_login'),
                dcc.Store(id='index_logout'),
                html.Div(id='index_logout_route'),
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/home",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Row(
                        [
                            dbc.Col(dbc.DropdownMenu(
                                [dbc.DropdownMenuItem("种质资源", href='/home/analyse/seedresource'),
                                 dbc.DropdownMenuItem("表型分析", href='/home/analyse/Phenotyping'),
                                 dbc.DropdownMenuItem("基因型分析", href='/home/analyse/Genotyping'),
                                 dbc.DropdownMenuItem("多组学分析", href='/home/analyse/MultiOmicAnalysis')],
                                label="常用分析工具",
                                nav=True,
                            )),
                            dbc.Col(
                                dbc.DropdownMenu(
                                    [dbc.DropdownMenuItem("动态新闻", href='/home/about/new'),
                                     dbc.DropdownMenuItem("专业人员", href='/home/about/people'),
                                     dbc.DropdownMenuItem("合作伙伴", href='/home/about/partners'),
                                     dbc.DropdownMenuItem("设备信息", href='/home/about/equipment')],
                                    label="关于我们",
                                    nav=True,
                                )
                                ,
                                width="auto",
                            ),
                            dbc.Col(dbc.DropdownMenu(
                                [dbc.DropdownMenuItem("种质交易", href='/home/publice/seedtrade'),
                                 dbc.DropdownMenuItem("种质详情信息", href='/home/publice/seedinfo'),
                                 dbc.DropdownMenuItem("文献下载", href='/home/publice/literature')],
                                label="公共资源",
                                nav=True,
                            )),
                            dbc.Col([dbc.Button('登录', id='header_to_login')] if not userid else
                                    [html.Span(userid,), dbc.Button('登出',id='header_logout')]
                                    , style={'display': 'flex'})
                        ],
                        className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                        align="center",
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ]
            ,
            color="light"
        ))
        ])
        return navbar

    @staticmethod
    def footer():
        """
        首页页尾组件
        :return:
        """
        return dbc.Row([
                dbc.Col([html.Div([
                    html.Span('常用分析工具'),
                    html.P('表型分析')
                ]),
                    html.Div([
                        html.Span('关于我们'),
                        html.P('平台介绍')
                    ]),
                    html.Div([
                        html.Span('帮助'),
                        html.P('种质交易')
                    ]),
                ],style={'display':'flex'},width=6),
                dbc.Col([
                    html.Div([html.Div('图片')]),
                    html.Div(html.Div('合作伙伴:')),
                    html.Div(id='home_link_info')
                ],width=6)
            ])

    @staticmethod
    def header_bread():
        """
        首页面包屑
        :return:
        """
        # 首页面包屑
        return dbc.Row(
            html.Div([
                fac.AntdBreadcrumb(id='header_bread_component',items=[]),
                html.H3(id='header_bread_now')
            ])
            )

    @staticmethod
    def enter_sys_btn():
        """
        进入系统按钮
        :return:
        """
        return html.Button('进入系统', style={'position': 'sticky', 'left': '94%', 'top': '80px'},id='home-to-system-btn',className='float_enter_system_btn')

    @staticmethod
    def change_locale():
        """
        选择中英文按钮
        :return:
        """
        return html.Button('改变语言', style={'position': 'sticky', 'left': '94%',  'top': '160px'},
                           className='float_change_locale_btn')

