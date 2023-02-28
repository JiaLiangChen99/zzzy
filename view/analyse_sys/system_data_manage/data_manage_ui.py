import json
import time

import dash
import feffery_antd_components as fac
from dash import html,dcc
from server import app
from dash import Input,Output,State
from model.USER_INFO import USER_INFO
from flask_login import current_user
from model.PERMISSION_TEAM_INFO import PERMISSION_TEAM_INFO
import datetime
from model.PERMISSION_MECHANISM import PERMISSION_MECHANISM
from model.USER_INFO import USER_INFO
from model.PERMISSION_TEAM_QUEEN import PERMISSION_TEAM_QUEEN
#团队管理
'''
首先，一个用户  可以创建一个团队或者多个团队，必要情况需要拉人进入团队进行管理

可以展示的：
1、团队数量
2、合作伙伴
3、研究作物
4、团队member


'''

#cache 缓存之类的
def all_mechanism():
    return [
    {'label': '惠州学院', 'value': '惠州学院'},
    {'label': '广州科创中心', 'value': '广州科创中心'},
    {'label': '华南农业大学', 'value': '华南农业大学'},
]


def gettable():
    teamdict = {}
    Myteam = list(PERMISSION_TEAM_INFO.select(PERMISSION_TEAM_INFO.TEAM_NAME,
                                              PERMISSION_TEAM_INFO.TEAM_MEMBER,
                                              PERMISSION_TEAM_INFO.TEAM_DESCRIBE,
                                              PERMISSION_TEAM_INFO.TEAM_CREATE_TIME
                                              )
                  .where(PERMISSION_TEAM_INFO.TEAM_MEMBER == current_user.id).dicts())
    for i in Myteam:
        teamdict[i['TEAM_NAME']] = {'TEAM_DESCRIBE': i['TEAM_DESCRIBE'], 'TEAM_CREATE_TIME': i['TEAM_CREATE_TIME']}
    for team in teamdict.keys():
        query = list(PERMISSION_TEAM_INFO.select(PERMISSION_TEAM_INFO.TEAM_NAME,
                                                 )
                     .where(PERMISSION_TEAM_INFO.TEAM_NAME == team).dicts())
        teamdict[team]['number'] = len(query)
    # print(teamdict) #{'test01': {'TEAM_DESCRIBE': '种质资源十九个测试', 'TEAM_CREATE_TIME': datetime.datetime(2023, 2, 26, 13, 8, 57), 'number': 1}, '测试机': {'TEAM_DESCRIBE': None, 'TEAM_CREATE_TIME': datetime.datetime(2023, 2, 26, 13, 38, 37), 'number': 2}, '新的团队': {'TEAM_DESCRIBE': None, 'TEAM_CREATE_TIME': datetime.datetime(2023, 2, 26, 13, 42, 47), 'number': 1}}
    data = []
    for key, value in teamdict.items():
        data.append({'团队名称': key, '团队成员数量': value['number'], '团队描述': value['TEAM_DESCRIBE']})
    return data

def team_manage_ui(**kwargs):
    return [
        html.Div(id='infomation_store'),
        dcc.Store(id='create_success'),
        dcc.Store(id='del_team'),
        dcc.Store(id='exit_team_store'),
        dcc.Store(id='set_up_team_store'),
        html.Div([
            fac.AntdHeader('团队管理',className='sys-function-header'),
            dcc.Store(id='updata_team'),
            fac.AntdRow(
                [
                    fac.AntdCol(
                        fac.AntdSpace(
                            [
                                fac.AntdAvatar(
                                    mode='icon',
                                    size=60,
                                    icon=item['icon'],
                                    style={
                                        'backgroundColor': '#f2f3f5',
                                        'fontSize': '36px'
                                    }
                                ),
                                fac.AntdSpace(
                                    [
                                        fac.AntdText(
                                            item['title']
                                        ),
                                        html.Span(
                                            [
                                                fac.AntdText(
                                                    item['value'],
                                                    strong=True,
                                                    style={
                                                        'fontSize': '28px',
                                                        'paddingRight': '10px'
                                                    }
                                                ),
                                                fac.AntdText(
                                                    item['unit']
                                                )
                                            ]
                                        )
                                    ],
                                    direction='vertical',
                                    size=0
                                )
                            ]
                        ),
                        span=6,
                        style={
                            'height': '100%',
                            'borderRight': '1px solid #e5e6eb' if col < 3 else 'none',
                            'display': 'flex',
                            'justifyContent': 'center'
                        }
                    )
                    for col, item in enumerate(
                    # 示例数据
                    [
                        {
                            'icon': 'fc-document',
                            'title': '团队数量',
                            'value': '3',
                            'unit': '队'
                        },
                        {
                            'icon': 'fc-conference-call',
                            'title': '合作伙伴',
                            'value': '368',
                            'unit': '人'
                        },
                        {
                            'icon': 'fc-positive-dynamic',
                            'title': '项目数量',
                            'value': '1',
                            'unit': '个'
                        },
                        {
                            'icon': 'fc-search',
                            'title': '研究物种',
                            'value': '1',
                            'unit': '种'
                        }
                    ]
                )
                ],style={
                            'height': '70px',
                            'background-color':'white'
                        }),
            fac.AntdRow([
                fac.AntdButton('创建团队',id='datamanage-createteam-btn'),
                fac.AntdButton('编辑团队',id='set_up_team_store'),
                fac.AntdButton('退出团队', id='exit-team-btn'),
                fac.AntdButton('删除团队', id='del-team-btn'),
            ],id='my_team_show',className='CreateTeam'),
            fac.AntdTable(
                id='my_team_table',
                rowSelectionType='radio',
                columns=[
                    {
                        'title': '团队名称',
                        'dataIndex': '团队名称'
                    },
                    {
                        'title': '团队成员数量',
                        'dataIndex': '团队成员数量'
                    },
                    {
                        'title': '团队描述',
                        'dataIndex': '团队描述'
                    },
                    {
                        'title': '创建人',
                        'dataIndex': '创建人'
                    },
                    {
                        'title': '团队创建日期',
                        'dataIndex': '团队创建日期'
                    },
                ]
            )
            ,
            #添加团队模态框样式
            fac.AntdModal([
                    fac.AntdForm([
                        fac.AntdFormItem(
                            [
                                fac.AntdInput(id='create_team_title')
                            ],
                            label='团队名称',
                            required=True,
                            id = 'create_team_form_title'
                        ),
                        fac.AntdFormItem([
                            fac.AntdInput(
                                id='model_createteam_desc',
                                mode='text-area',
                                style={
                                    'width': '600px',
                                    'marginBottom': '5px',
                                    'height': '80px'
                                }
                            )],
                            label='团队介绍'
                        ),
                        fac.AntdFormItem([
                            fac.AntdButton('创建团队',id='create_team_model_btn')],
                            id= 'create_data_success'
                        )
                    ],className='create_model_form',
                        labelCol={
                            'span': 4
                        },
                        wrapperCol={
                            'span': 8
                        }
                    )
            ],title=html.Div('创建团队',className='create_model_title')
                ,width=800,id='Team_manage',className='create_body'
            ),
            fac.AntdModal([
                dcc.Store(id='team_user_info_table'),
                dcc.Store(id='team_user_list'), #存储当前team的用户信息
                fac.AntdForm([
                    fac.AntdFormItem(
                        [
                            fac.AntdInput(id='setup_team_name'),
                        ],label='团队名称'
                    ),
                    fac.AntdFormItem(
                        [
                            fac.AntdInput(id='setup_team_desc',mode='text-area',)
                        ],label='团队描述'
                    ),
                    fac.AntdFormItem(
                        [fac.AntdInput(id='create_time',disabled=True)
                         ],label='创建事件'
                    ),
                ],labelCol={
                        'span': 4
                    },
                    wrapperCol={
                        'span': 8
                    }),
                fac.AntdModal([
                    fac.AntdForm([
                        fac.AntdFormItem([
                            fac.AntdSelect(id='invite_mechine',mode='multiple',),
                        ],label='机构名称'),
                    ]),
                    fac.AntdTransfer(id='invite-user-id',
                                     titles=['待选成员', '邀请成员']
                                     ),
                    fac.AntdFormItem([
                        fac.AntdInput(id='invite_desc', mode='text-area'),
                    ],label='邀请信息编辑'),
                    fac.AntdButton('邀请成员',id='to_invite_user'),
                    html.Div(id='invite-message-info')
                ],id='invite-user-model',
                    title=html.Div('邀请成员', className='create_model_title')
                ),
                fac.AntdRow([
                    fac.AntdButton('邀请成员',id='invite-user-btn'),
                    fac.AntdButton('删除成员'),
                    fac.AntdButton('权限设置',id='team_user_root')
                ]),
                fac.AntdTable(id='my_team_userinfo_table',
                              rowSelectionType='checkbox'
                              ,columns=[
                                        {
                                            'title': '团队成员',
                                            'dataIndex': '团队成员'
                                        },
                                        {
                                            'title': '所属机构',
                                            'dataIndex': '所属机构'
                                        },
                                        {
                                            'title': '加入时间',
                                            'dataIndex': '加入时间'
                                        }
                                    ]
                              ),
                fac.AntdButton('确认修改')
            ], title=html.Div('团队编辑', className='create_model_title')
                , width=800, id='Team_setup', className='create_body'
            )
        ])]



@app.callback(
    Output('Team_manage','visible'),
    Input('datamanage-createteam-btn','nClicks')
)
def show_teammanage_model(n):
    """
    按钮打开创建团队的模态框
    :param n:
    :return:
    """
    if n:
        return True



@app.callback(
    Output('create_team_form_title','validateStatus'),
    Output('create_team_form_title','help'),
    Output('updata_team','data'),
    Input('create_team_model_btn','nClicks'),
    State('create_team_title','value'),
    State('model_createteam_desc','value'),
    prevent_initial_call=True
)
def create_team_func(n,title,desc):
    """
    创建团队
    :param n: 点击事件
    :param title:  团队名字
    :param desc: 团队描述
    :return:
    """
    if n:
        if title:
            if title not in [i['TEAM_NAME']  for i in
                             list(
                                 PERMISSION_TEAM_INFO
                                         .select(PERMISSION_TEAM_INFO.TEAM_NAME,
                                                 PERMISSION_TEAM_INFO.TEAM_MEMBER,
                                                 PERMISSION_TEAM_INFO.TEAM_MEMBER_CODE,
                                                 )
                                         .where(
                                     (PERMISSION_TEAM_INFO.TEAM_MEMBER_CODE == 0) &
                                     (PERMISSION_TEAM_INFO.TEAM_MEMBER == current_user.id)
                                 ).dicts())]:
                query = USER_INFO.select(USER_INFO.USER_NAME,
                                         USER_INFO.USER_UNIT
                                         ).where(USER_INFO.USER_NAME == current_user.id)
                UNIT = list(query.dicts())[0]['USER_UNIT'] #获取机构

                Team = PERMISSION_TEAM_INFO(
                                            TEAM_NAME = title,
                                            TEAM_MEMBER = current_user.id,
                                            TEAM_MEMBER_CODE = 0,
                                            TEAM_MEMBER_UNIT = UNIT,
                                            TEAM_CREATE_TIME = datetime.datetime.now(),
                                            TEAM_DESCRIBE = desc,
                                            TEAM_CREATE_MEMBER = current_user.id
                                            )
                Team.save()
                return 'success','创建成功','success'

            else:
                return 'error','团队名已存在',None
        else:
            return None, None,None






@app.callback(
    Output('my_team_table','data'),
    Input('updata_team','data'),
    Input('del_team','data'),
    Input('exit_team_store','data'),
    Input('now-page-href','data'),
    State('my_team_table','data'),
)
def updata_team_table(data,dell,exit,href,tabledata):
    """
    模态框更新，以及页面初始化回调
    :param data:
    :param href:
    :return:
    """
    if dash.ctx.triggered_id == 'updata_team':
        #当要更新table，输入的为store
        if data == 'success':
            #首先我先获取到我有哪些team以及相应的描述
            teamdict = {}
            Myteam = list(PERMISSION_TEAM_INFO.select(PERMISSION_TEAM_INFO.TEAM_NAME,
                                                     PERMISSION_TEAM_INFO.TEAM_MEMBER,
                                                      PERMISSION_TEAM_INFO.TEAM_DESCRIBE,
                                                      PERMISSION_TEAM_INFO.TEAM_CREATE_MEMBER,
                                                      PERMISSION_TEAM_INFO.TEAM_CREATE_TIME
                                                     )
                         .where(PERMISSION_TEAM_INFO.TEAM_MEMBER == current_user.id).dicts())
            print(Myteam)
            for i in Myteam:
                teamdict[i['TEAM_NAME']] = {'TEAM_DESCRIBE':i['TEAM_DESCRIBE'],'TEAM_CREATE_MEMBER':i['TEAM_CREATE_MEMBER'],'TEAM_CREATE_TIME':i['TEAM_CREATE_TIME']}
            for team in teamdict.keys():
                query = list(PERMISSION_TEAM_INFO.select(PERMISSION_TEAM_INFO.TEAM_NAME,
                                                         )
                             .where(PERMISSION_TEAM_INFO.TEAM_NAME == team).dicts())
                teamdict[team]['number'] = len(query)
            #print(teamdict) #{'test01': {'TEAM_DESCRIBE': '种质资源十九个测试', 'TEAM_CREATE_TIME': datetime.datetime(2023, 2, 26, 13, 8, 57), 'number': 1}, '测试机': {'TEAM_DESCRIBE': None, 'TEAM_CREATE_TIME': datetime.datetime(2023, 2, 26, 13, 38, 37), 'number': 2}, '新的团队': {'TEAM_DESCRIBE': None, 'TEAM_CREATE_TIME': datetime.datetime(2023, 2, 26, 13, 42, 47), 'number': 1}}
            data = []
            for key,value in teamdict.items():
                data.append({'团队名称':key,'团队成员数量':value['number'],'团队描述':value['TEAM_DESCRIBE'],'创建人':value['TEAM_CREATE_MEMBER'],'团队创建日期':value['TEAM_CREATE_TIME'].strftime('%Y-%m-%d %H:%M:%S') })
            return data
    elif dash.ctx.triggered_id == 'del_team':
        #返回的是操作的团队，当这里触发是，exit参数返回的是退出团队，操作和下面一样的
        return [table_row_data for table_row_data in tabledata if table_row_data['团队名称'] != dell]
    elif dash.ctx.triggered_id == 'exit_team_store':
        #返回的是操作的团队，当这里触发是，exit参数返回的是退出团队，这里把页面的data同步然后删除就好了
        return [table_row_data for table_row_data in tabledata if table_row_data['团队名称'] != exit]
    else: #否则的话，说明是刚进入页面，直接刷新所有数据给表格就好了
        teamdict = {}
        Myteam = list(PERMISSION_TEAM_INFO.select(PERMISSION_TEAM_INFO.TEAM_NAME,
                                                  PERMISSION_TEAM_INFO.TEAM_MEMBER,
                                                  PERMISSION_TEAM_INFO.TEAM_DESCRIBE,
                                                  PERMISSION_TEAM_INFO.TEAM_CREATE_MEMBER,
                                                  PERMISSION_TEAM_INFO.TEAM_CREATE_TIME
                                                  )
                      .where(PERMISSION_TEAM_INFO.TEAM_MEMBER == current_user.id).dicts())
        for i in Myteam:
            teamdict[i['TEAM_NAME']] = {'TEAM_DESCRIBE': i['TEAM_DESCRIBE'],'TEAM_CREATE_MEMBER':i['TEAM_CREATE_MEMBER'], 'TEAM_CREATE_TIME': i['TEAM_CREATE_TIME']}
        #计算每个团队的人数
        for team in teamdict.keys():
            query = list(PERMISSION_TEAM_INFO.select(PERMISSION_TEAM_INFO.TEAM_NAME,
                                                     )
                         .where(PERMISSION_TEAM_INFO.TEAM_NAME == team).dicts())
            teamdict[team]['number'] = len(query)
        # print(teamdict) #{'test01': {'TEAM_DESCRIBE': '种质资源十九个测试', 'TEAM_CREATE_TIME': datetime.datetime(2023, 2, 26, 13, 8, 57), 'number': 1}, '测试机': {'TEAM_DESCRIBE': None, 'TEAM_CREATE_TIME': datetime.datetime(2023, 2, 26, 13, 38, 37), 'number': 2}, '新的团队': {'TEAM_DESCRIBE': None, 'TEAM_CREATE_TIME': datetime.datetime(2023, 2, 26, 13, 42, 47), 'number': 1}}
        data = []
        for key, value in teamdict.items():
            data.append({'团队名称': key, '团队成员数量': value['number'], '团队描述': value['TEAM_DESCRIBE'],
                         '创建人':value['TEAM_CREATE_MEMBER'],
                         '团队创建日期': value['TEAM_CREATE_TIME'].strftime('%Y-%m-%d %H:%M:%S')})
        return data


'''
删除团队和退出团队时才会触发的回调，修改相应的store和消息提示
'''
@app.callback(
    Output('infomation_store', 'children'),  # 消息提醒
    Output('del_team','data'),
    Output('exit_team_store','data'),
    Input('exit-team-btn','nClicks'),
    Input('del-team-btn','nClicks'),
    State('my_team_table','selectedRows'),
    prevent_initial_call=True
)
def set_up_team(exit,dell,select):
    if select:  #[{'团队名称': 'test01', '团队成员数量': 1, '团队描述': '种质资源十九个测试', '团队创建日期': '2023-02-26 13:08:57', 'key': '0'}]
        team_name = select[0]['团队名称']
        print(team_name)
        if dash.ctx.triggered_id == 'exit-team-btn': #退出团队
            Myteam = list(PERMISSION_TEAM_INFO.select(PERMISSION_TEAM_INFO.TEAM_NAME,
                                                      PERMISSION_TEAM_INFO.TEAM_MEMBER,
                                                      PERMISSION_TEAM_INFO.TEAM_MEMBER_CODE
                                                      )
                          .where((PERMISSION_TEAM_INFO.TEAM_NAME == team_name)
                                 & (PERMISSION_TEAM_INFO.TEAM_MEMBER_CODE == 0)
                                 ).dicts())
            if len(Myteam) == 1 and Myteam[0]['TEAM_MEMBER'] == current_user.id:
                return fac.AntdMessage(
                            content='该团队仅只有您拥有管理权限，请转让管理权限后再推出团队',
                            type='error'
                        ),dash.no_update,dash.no_update
            else:
                #数据库删除
                PERMISSION_TEAM_INFO.delete().where((PERMISSION_TEAM_INFO.TEAM_NAME == team_name)
                                                    &(PERMISSION_TEAM_INFO.TEAM_MEMBER==current_user.id)).execute()
                return fac.AntdMessage(
                            content='退出成功',
                            type='success'
                        ),dash.no_update,team_name
        if dash.ctx.triggered_id == 'del-team-btn':
            PERMISSION_TEAM_INFO.delete().where(PERMISSION_TEAM_INFO.TEAM_NAME == team_name).execute()
            return fac.AntdMessage(
                content='删除成功',
                type='success'
            ), team_name, dash.no_update
    return dash.no_update,dash.no_update,dash.no_update


'''
编辑权限中的table信息
'''
@app.callback(
    Output('setup_team_name','value'),
    Output('setup_team_name','disable'),
    Output('setup_team_desc','value'),
    Output('setup_team_desc','disable'),
    Output('create_time','value'),
    Output('my_team_userinfo_table','data'),
    Output('team_user_list','data'),
    Input('team_user_info_table','data'),
    prevent_initial_call=True
)
def get_team_user_model_init(data:list):
    """
    data就是外层table选择的栏的信息
    selectedRows：
    [
        {
        "字段示例1": 1,
        "字段示例2": 1,
        "字段示例3": 1,
        "key": "1"
        }
    ]
    """
    if dash.ctx.triggered_id == 'team_user_info_table':
        teamname = data[0]['团队名称']
        desc = data[0]['团队描述']
        createtime = data[0]['团队创建日期']
        '''先获取当前用户的权限情况，判断是否可以修改团队名字等等'''
        query = list(PERMISSION_TEAM_INFO.select(
                PERMISSION_TEAM_INFO.TEAM_MEMBER,
                PERMISSION_TEAM_INFO.TEAM_MEMBER_CODE,
                PERMISSION_TEAM_INFO.TEAM_NAME
            ).where(
                (PERMISSION_TEAM_INFO.TEAM_NAME == teamname)&
                (PERMISSION_TEAM_INFO.TEAM_MEMBER == current_user.id)
            ).dicts())
        TEAM_MEMBER_CODE = query[0]['TEAM_MEMBER_CODE']
        '''获取table的data信息'''
        database_get_member_data = list(PERMISSION_TEAM_INFO.select(
                PERMISSION_TEAM_INFO.TEAM_MEMBER,
                PERMISSION_TEAM_INFO.TEAM_MEMBER_UNIT,
                PERMISSION_TEAM_INFO.TEAM_CREATE_TIME,
                PERMISSION_TEAM_INFO.TEAM_NAME,
            ).where(PERMISSION_TEAM_INFO.TEAM_NAME == teamname
            ).dicts())
        tabledata = [{'团队成员':data['TEAM_MEMBER'],
                      '所属机构':data['TEAM_MEMBER_UNIT'],
                      '加入时间':data['TEAM_CREATE_TIME'].strftime('%Y-%m-%d %H:%M:%S')
                      }
                     for data in database_get_member_data]

        team_now_user = [data['TEAM_MEMBER'] for data in database_get_member_data]
        if TEAM_MEMBER_CODE == 0: #说明是团队管理员，可以编辑
            return teamname, False, desc, False, createtime, tabledata, team_now_user
        else:
            return teamname, True, desc, True, createtime,tabledata, team_now_user

'''
编辑权限了，需要弹出Model框，同时需要根据选的select来获取团队的具体信息了，另外可以发送邀请
'''
@app.callback(
    Output('team_user_info_table','data'),
    Output('Team_setup','visible'),
    Input('set_up_team_store','nClicks'),
    State('my_team_table','selectedRows'),
    prevent_initial_call=True
)
def set_up_team_info_model(n,selected):
    if n:
        if selected:
            return selected,True
        else:
            return dash.no_update
'''
首先，用户点击了邀请按钮，才会弹出邀请人员的model
'''
@app.callback(
    Output('invite-user-model','visible'),
    Input('invite-user-btn','nClicks'),
    prevent_initial_call=True
)
def invite_user(n):
    if n:
        return True

'''
当弹出邀请人员model时，需要对组件进行更新值
这里需要更新选择框的机构
'''
@app.callback(
    Output('invite_mechine','options'),
    Input('invite-user-model','visible'),
    prevent_initial_call=True
)
def invite_model_get_mechine(visible):
    if visible == True:
        mechanism = list(PERMISSION_MECHANISM.select(PERMISSION_MECHANISM.MECHANISM).dicts())
        return [{'label': me['MECHANISM'], 'value': me['MECHANISM']} for me in mechanism]
    else:
        return dash.no_update

'''
根据选择的机构，将可以邀请的成员名单拉进来
'''

@app.callback(
    Output('invite-user-id','dataSource'),
    Input('invite_mechine','value'),
    State('team_user_list','data'),
    prevent_initial_call=True
)
def invite_model_get_username(value:list,nowuser:list):
    '''

    :param value:   邀请用户时选择的机构，通过机构获取该机构下的所有用户信息
    :param nowuser: dccStore存储当前team的所有用户信息，构建穿梭框会用到
    :return:
    '''
    data = []
    for i in value:
        useridlist = list(USER_INFO.select(
                            USER_INFO.USER_UNIT,
                            USER_INFO.USER_NAME
                             ).where(
                USER_INFO.USER_UNIT == i
            ).dicts())
        for name in useridlist:
            if name['USER_NAME'] not in nowuser:
                data.append({'key': name['USER_NAME'], 'title': name['USER_NAME']})
    return data

"""
穿梭框选择好用户后，需要给该用户发送邀请信息

"""
@app.callback(
    Output('invite-message-info','children'),
    Input('to_invite_user','nClicks'),
    State('invite_desc','value'),
    State('invite-user-id','targetKeys'),
    State('team_user_info_table','data'),
    prevent_initial_call=True
)
def send_invite(n, desc, getter, tabledata):
    """
    :param n: 点击事件
    :param desc: 邀请话
    :param getter: 邀请人名单列表
    :param tabledata:  外层选择框的信息，比如团队名称之类的会用上
    :return:
    """
    if n:
        if getter:
            teamname = tabledata[0]['团队名称']
            creater = tabledata[0]['创建人']
            desc = desc if desc else f'{teamname}团队邀请您加入,请及时回复!'
            for inviter in getter:
                PERMISSION_TEAM_QUEEN.create(
                    TEAM_NAME=teamname,
                    TEAM_CREATER=creater,
                    TEAM_CODE=0,
                    QUEEN_SENDER=current_user.id,
                    QUEEN_GETTER=inviter,
                    SEND_TIME=datetime.datetime.now(),
                    SEND_DESC = desc
                )
            return fac.AntdNotification(
                message='发送成功提示',
                description='邀请消息发送成功，请关闭对话框',
                type='success'
            )
        else:
            return fac.AntdNotification(
                message='错误提示',
                description='检测到并未选择邀请人',
                type='error'
            )


#todo 数据管理模块
'''
数据管理模块的函数和方法
'''
def data_magene_ui(**kwargs):
    return [
        html.Div([
            fac.AntdHeader('数据管理', className='sys-function-header'),
            fac.AntdRow(
                [
                    fac.AntdHeader('基因型分析数据'),
                ],
                className='gene_data_manage_row'),
            fac.AntdRow(
                [
                    fac.AntdHeader('表型分析数据')
                ],
                className='character_data_manage_row'
            )
        ])]
