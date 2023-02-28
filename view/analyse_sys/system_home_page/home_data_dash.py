import dash
import feffery_antd_components as fac
from dash import html, Input, Output, dcc, State, ALL
from view_c.analyse_sys.system_home_page import home_data_dash_c
from server import app
from model.PERMISSION_TEAM_QUEEN import PERMISSION_TEAM_QUEEN
from model.PERMISSION_TEAM_INFO import PERMISSION_TEAM_INFO
from flask_login import current_user
import datetime



#默认页面内的UI组件渲染
def home_data_dash_page_ui(**kwargs):
    return [
            html.Div(
                [
                    dcc.Store(id='read_team_session_request_store'),  #如果是确认加入或者拒绝加入团队的store
                    dcc.Store(id='is_read_team_session_store'), #如果是点击已读消息触发
                    fac.AntdModal(
                        [
                            dcc.Store(id='read_team_session_store'),
                            html.Div(id='read_team_session_request'),
                            fac.AntdForm(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdInput(id='model_team_session_whoinvite',disabled=True),
                                        label='邀请人'
                                    ),
                                    fac.AntdFormItem(
                                        fac.AntdInput(id='model_team_session_teamname',disabled=True),
                                        label='团队名'
                                    ),
                                    fac.AntdFormItem(
                                        fac.AntdInput(id='model_team_session_teamcreate',disabled=True),
                                        label='团队创建者',
                                    ),
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='model_team_session_desc',
                                            mode='text-area',
                                            style={
                                                'width': '600px',
                                                'marginBottom': '5px',
                                                'height': '80px'
                                            },
                                            disabled=True
                                        ),
                                        label='邀请内容'
                                    ),
                                    fac.AntdFormItem([
                                        fac.AntdButton('同意加入',id='team_session_agress_btn',type='primary'),
                                        fac.AntdButton('拒绝加入',id='team_session_reject_btn',type='primary', danger=True)
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
                                }
                            )
                        ],
                        title=html.Div('团队邀请',className='create_model_title'),width=800,
                        id='team-read-session',className='create_body'), #读取消息model
                    fac.AntdHeader('平台数据仪表盘', className='sys-function-header'),
                    fac.AntdRow(
                        [
                            fac.AntdCol([
                                fac.AntdHeader('团队信息',className='system_home_session_header'),
                                html.Div([
                                ],id='recent_session_info'),  #存储团队消息
                            ],span=15,style={'height':'400px','overflow':'auto','background-color':'white'}),
                            fac.AntdCol([
                                fac.AntdHeader('分析队列',className='system_home_session_header'),
                                html.Div([
                                ], id='recent_analyse_session_info'), #存储分析任务消息
                            ],span=8,style={'height':'400px','overflow':'auto','background-color':'white','margin-left':'30px'}),
                        ],
                        className='home_session_left_div'
    )
                ]
            )
        ]

#总体的渲染
def home_data_dash_ui(**kwargs):
    return [

            #全局利用recent_session_info_store存储团队中未读信息
            dcc.Store(id='recent_session_info_store'),
            fac.AntdCol(
                html.Div(
                    fac.AntdMenu(
                                menuItems=[
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'平台数据仪表盘',
                                            'title': f'平台数据仪表盘'
                                        }
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'基因型分析使用文档',
                                            'title': f'基因型分析使用文档'
                                        }
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'表型分析使用文档',
                                            'title': f'表型分析使用文档'
                                        }
                                    },
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'如何进行数据管理',
                                            'title': f'如何进行数据管理'
                                        }
                                    },
                                ],
                                mode='inline',
                                id='system-home-menu-children',
                                defaultSelectedKey='平台数据仪表盘'
                            ),
                    className='sys_body_left',
                    id='sys-left-show'
                ),
                flex='1'
            ),
            #当右侧点击栏刷新，修改html.Div的局部内容
            fac.AntdCol(
                html.Div(
                    children=[],
                    className='sys_body_right',
                    id = 'sys-right-show'
                ),
                flex='5'
            )
        ]


'''
修改team消息的回调，
任何和消息有关的回调都在这里
'''
#todo 后续还需要加上，比如说啥时候删除data，啥时候恢复
@app.callback(
    Output('recent_session_info_store','data'),  #目前这个为团队消息
    Input('read_team_session_request_store','data'),  #当用户对团队的代办消息处理后，更新data来修改页面存储的消息队列信息
    Input('is_read_team_session_store','data'), #当用户对团队已读消息处理后触发
    State('recent_session_info_store','data'),
)
def get_recent_team_session(read_data,isread_data, team_data):
    '''
    :param read_data:  已经读取的团队消息id， 页面需要把这个消息id的队列进行删除，从而修改外面的页面
    :param team_data:  团队初始化的页面信息
    :return:
    '''
    if dash.ctx.triggered_id == 'read_team_session_request_store': #当用户读取了信息后，会触发这个store的回调
        if read_data != None:
            return [i for i in team_data if i['TEAM_ID'] != read_data]
    if dash.ctx.triggered_id == 'is_read_team_session_store': #当用户读取了信息后，会触发这个store的回调
        if isread_data != None:
            return [i for i in team_data if i['TEAM_ID'] != isread_data]
    if team_data == None:
        query = list(PERMISSION_TEAM_QUEEN.select().where(
            (PERMISSION_TEAM_QUEEN.QUEEN_GETTER == current_user.id) &
            ((PERMISSION_TEAM_QUEEN.TEAM_CODE == 0) | (PERMISSION_TEAM_QUEEN.TEAM_CODE == 2) | (PERMISSION_TEAM_QUEEN.TEAM_CODE == 3))
        ).dicts())
        return query
    else:
        return dash.no_update

'''
更新顶层消息提示的回调
还需要做的就是把任务队列的消息也一起合并起来，现在只做了团队信息的消息提示
'''
#todo 后续还需要加上任务消息队列，比如长耗时的分析任务
@app.callback(
    Output('sys_session_icon','style'),   #顶层消息的ICON样式，有消息时换颜色
    Output('queen_session_badge','count'),  #顶层消息提示标徽的数量，有消息显示66就好了
    Output('sys-session-tooltip','title'),   #顶层消息提示的字样，如果没有消息不用修改用默认的，有消息提示为有多少条代办消息
    Input('recent_session_info_store','data'),  #存储团队消息的data
)
def updata_top_session(data):
    if len(data) != 0:
        return {'color':'red'},66,f'你有{len(data)}条待办消息'
    else:
        return {'color':'black'},0,'消息提示'

'''
更新团队消息的回调函数
'''
@app.callback(
    Output('recent_session_info','children'),
    Input('recent_session_info_store','data'),
)
def show_session_topage(data):
    if data:
        children = []
        for i in data:
            if i['TEAM_CODE'] == 0: #说明时未读消息,且需要进行是否同意加入或者拒绝加入
                children.append(
                    html.Div([
                        fac.AntdRow([
                            fac.AntdCol([
                                html.Div([fac.AntdAvatar(
                                    mode='icon',
                                    style={
                                        'backgroundColor': 'rgb(16, 105, 246)'
                                    }
                                )]),
                            ], style={'width':'50px'}),
                            fac.AntdCol([
                                html.Div([
                                    fac.AntdHeader([html.Div(i['QUEEN_SENDER']),html.Div(i['SEND_TIME'].replace('T',' '),className='one_session_time')],className='one_session_header'),
                                    fac.AntdText(i['SEND_DESC'] if len(i['SEND_DESC'])<70 else i['SEND_DESC'][:70]+'......'),
                                ], className='session_info_div'),
                            ], style={'width':'600px'}),
                            fac.AntdCol([
                                html.Div([fac.AntdButton('查看',id={'type':'team_session_btn','index':i['TEAM_ID']})])
                            ], style={'width':'100px','height': '80px','display':'flex','align-items':'center','justify-content':'center'})
                        ]),
                    ], className='home_one_of_session')
                )
            elif i['TEAM_CODE'] == 2: #说明是要么同意要么不同意咯
                children.append(
                    html.Div([
                        fac.AntdRow([
                            fac.AntdCol([
                                html.Div([fac.AntdAvatar(
                                    mode='icon',
                                    style={
                                        'backgroundColor': 'rgb(16, 105, 246)'
                                    }
                                )]),
                            ], style={'width': '50px'}),
                            fac.AntdCol([
                                html.Div([
                                    fac.AntdHeader([html.Div(i['QUEEN_SENDER']),
                                                    html.Div(i['SEND_TIME'].replace('T', ' '),
                                                             className='one_session_time')],
                                                   className='one_session_header'),
                                    fac.AntdText(
                                        i['SEND_DESC'] if len(i['SEND_DESC']) < 70 else i['SEND_DESC'][:70] + '......'),
                                ], className='session_info_div'),
                            ], style={'width': '600px'}),
                            fac.AntdCol([
                                html.Div(
                                    [fac.AntdButton('确认已读', id={'type': 'team_isread_btn', 'index': i['TEAM_ID']})])
                            ], style={'width': '100px', 'height': '80px', 'display': 'flex', 'align-items': 'center',
                                      'justify-content': 'center'})
                        ]),
                    ], className='home_one_of_session')
                )
        return children
    return fac.AntdEmpty()



'''
确认已读消息的回调处理
'''
@app.callback(
    Output('is_read_team_session_store','data'),
    Input({'type': 'team_isread_btn', 'index': ALL},'nClicks'),
prevent_initial_call=True
)
def teamisread_session(n):
    if any(n):
        teamsessionid = dash.ctx.triggered_id['index']
        '''修改数据库的消息状态，改为1已读'''
        p2 = PERMISSION_TEAM_QUEEN.update({PERMISSION_TEAM_QUEEN.TEAM_CODE: 1}).where(
            PERMISSION_TEAM_QUEEN.TEAM_ID == teamsessionid)
        p2.execute()
        return teamsessionid
    else:
        return dash.no_update


'''
将团队邀请的信息填充进model的store进行管理
'''
@app.callback(
    Output('read_team_session_store','data'),
    Output('team-read-session','visible'),
    Input({'type':'team_session_btn','index':ALL},'nClicks'),
    State('recent_session_info_store','data'),
    prevent_initial_call=True
)
def to_check_team_queen(n,team_session_data):
    if any(n):
        team_session_id = dash.ctx.triggered_id['index']
        for i in team_session_data:
            if i['TEAM_ID'] == team_session_id:
                return [i['TEAM_ID'],i['QUEEN_SENDER'],i['TEAM_NAME'],i['TEAM_CREATER'],i['SEND_DESC']],True
    return dash.no_update,dash.no_update



'''
利用model的store刷新model的团队邀请信息
'''
@app.callback(
    Output('model_team_session_whoinvite','value'),
    Output('model_team_session_teamname','value'),
    Output('model_team_session_teamcreate','value'),
    Output('model_team_session_desc','value'),
    Input('read_team_session_store','data'),
    prevent_initial_call=True
)
def show_team_model_info(data):
    '''
    data存储相应的信息 ：消息id,邀请人，团队名，团队创建者，邀请描述
    :param data:
    :return:
    '''
    return data[1],data[2],data[3],data[4]


'''
当这里进行确认后，相应的要给页面的回调修改
'''
@app.callback(
    Output('read_team_session_request_store','data'),
    Output('read_team_session_request','children'),
    Input('team_session_agress_btn','nClicks'),
    Input('team_session_reject_btn','nClicks'),
    State('read_team_session_store','data'),
    State('system-select-chrosm-store','data'),
    prevent_initial_call=True
)
def agree_or_reject_team(n1,n2,data,unit):
    '''
    data存储相应的信息 ：消息id,邀请人，团队名，团队创建者，邀请描述
    :param n1:
    :param n2:
    :param data:
    :return:  当处理信息后，返回消息id给store处理就好了
    '''
    if n1 or n2:
        team_sessionid = data[0]  #团队消息表的相应id
        inviter = data[1]  #邀请我的人
        team_name = data[2]
        team_create = data[3]
        team_member = current_user.id
        TEAM_MEMBER_UNIT = unit
        query = list(PERMISSION_TEAM_INFO\
            .select(PERMISSION_TEAM_INFO.TEAM_DESCRIBE,PERMISSION_TEAM_INFO.TEAM_CREATE_MEMBER,PERMISSION_TEAM_INFO.TEAM_CREATE_TIME)\
            .where(PERMISSION_TEAM_INFO.TEAM_CREATE_MEMBER == team_create).dicts())
        TEAM_DESCRIBE = query[0]['TEAM_DESCRIBE']
        TEAM_CREATE_TIME = query[0]['TEAM_CREATE_TIME']
        if dash.ctx.triggered_id == 'team_session_agress_btn': #说明同意加入了
            ''' 团队表进行相应的更新 '''
            p = PERMISSION_TEAM_INFO(TEAM_NAME = team_name, TEAM_MEMBER=team_member,TEAM_MEMBER_CODE=1,
                                        TEAM_MEMBER_UNIT=TEAM_MEMBER_UNIT, TEAM_CREATE_TIME=TEAM_CREATE_TIME,
                                        TEAM_DESCRIBE=TEAM_DESCRIBE, TEAM_CREATE_MEMBER=team_create
                                        )
            p.save()
            '''修改这个信息的code  code改为1  说明已读'''
            p2 = PERMISSION_TEAM_QUEEN.update({PERMISSION_TEAM_QUEEN.TEAM_CODE:1}).where(PERMISSION_TEAM_QUEEN.TEAM_ID == team_sessionid)
            p2.execute()
            '''  发送新的消息给邀请你的人，code改为2  告诉对方答复'''
            p3 = PERMISSION_TEAM_QUEEN(TEAM_NAME=team_name, TEAM_CREATER=team_create, TEAM_CODE=2, QUEEN_SENDER=team_member,
                                  QUEEN_GETTER = inviter, SEND_TIME=datetime.datetime.now(), SEND_DESC=f'对方已同意加入你的团队{team_name}'
                                  )
            p3.save()
            return data[0],fac.AntdNotification(
            message='回复提示',
            description='您已同意对方的团队邀请，已为你发送消息，请关闭当前窗口',
            type='success',
        )
        elif dash.ctx.triggered_id == 'team_session_reject_btn': #当拒绝
            '''修改这个信息的code  code改为1  说明已读'''
            p2 = PERMISSION_TEAM_QUEEN.update({PERMISSION_TEAM_QUEEN.TEAM_CODE:1}).where(PERMISSION_TEAM_QUEEN.TEAM_ID == team_sessionid)
            p2.execute()
            '''发送新的消息给邀请你的人，code改为2  告诉对方答复 '''
            p3 = PERMISSION_TEAM_QUEEN(TEAM_NAME=team_name, TEAM_CREATER=team_create, TEAM_CODE=2, QUEEN_SENDER=team_member,
                                  QUEEN_GETTER = inviter, SEND_TIME=datetime.datetime.now(), SEND_DESC=f'对方已拒绝加入你的团队{team_name}'
                                  )
            p3.save()
            return data[0],fac.AntdNotification(
            message='回复提示',
            description='您已拒绝对方的团队邀请，已为你发送消息，请关闭当前窗口',
            type='success',
        )
    return dash.no_update,dash.no_update