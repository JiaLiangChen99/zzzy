import dash

from server import app, User
from dash import Input, Output, State,dcc
import hashlib
from model.USER_INFO import USER_INFO
from model.USER_PERMISSION import USER_PERMISSION
import re
from model.engine import mysql_db
from datetime import datetime
from flask_login import login_user

def check_phone_number(number):
    pattern = re.compile(r'^(13[0-9]|14[0|5|6|7|9]|15[0|1|2|3|5|6|7|8|9]|'
                         r'16[2|5|6|7]|17[0|1|2|3|5|6|7|8]|18[0-9]|'
                         r'19[1|3|5|6|7|8|9])\d{8}$')
    if re.match(pattern, number):
        return True
    else:
        return False

# 验证邮箱是否有效，有效返回 True, 无效返回 False
def check_email(email):
    regex = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"
    if re.match(regex, email):
        return True
    else:
        return False

def md5_to_password(password):
    hl = hashlib.md5()
    hl.update(password.encode(encoding='utf8'))
    md5 = hl.hexdigest()
    return md5


def check_user_notin_register(user_name):
    """
    判断该用户是否存在，如果不存在返回True  存在返回False
    :param user_name:
    :return:
    """
    if USER_INFO.select().where(USER_INFO.USER_NAME == user_name).exists():
        return False
    return True



#用户注册





#注册弹出注册卡
@app.callback(
    Output('register_model','visible'),
    Input('register_btn','nClicks'),
    prevent_initial_call=True
)
def toshow_register_model(n):
    if n:
        return True

#状态跳转
@app.callback(
    Output('login_page_router', 'children'),
    Input('login_code','data'),
    Input('register_code','data'),
    State('now_url', 'data'),
)
def login_page_router(data,data2,pathname):
    if data or data2:
        if dash.ctx.triggered_id == 'login_code':
            print(pathname)
            return dcc.Location(href=pathname,id='login_router_index')
        elif dash.ctx.triggered_id == 'register_code':
            return dcc.Location(href=pathname,id='register_router_index')
        return dash.no_update


#注册
@app.callback(
    [Output('form_register_username', 'validateStatus'),
    Output('form_register_username', 'help'),
    Output('form_register_password','validateStatus'),
    Output('form_register_password', 'help'),
    Output('form_register_repeat_password', 'validateStatus'),
    Output('form_register_repeat_password', 'help'),
    Output('form_register_repeat_phone', 'validateStatus'),
    Output('form_register_repeat_phone', 'help'),
    Output('register_code','data')],
    Input('register','nClicks'),
    State('register_username','value'),
    State('register_password','value'),
    State('register_repeat_password', 'value'),
    State('register_phone','value'),
    State('register_email','value'),
    State('register_unit', 'value'),
    prevent_initial_call=True
)
def to_register(n,username:str,password:str,repeat_password:str,
                phone, email, unit ):
    """
    判断用户的注册用户名是否大于20为  用户名是否重复
    判断用户密码是否小于20为
    判断用户密码是否和重复密码一样
    判断手机号是否有效
    判断email是否有效
    """
    if n:
        if len(username) > 20:
            return ['error', '用户名注册非法'] + [None] * 6 + [dash.no_update]
        if not check_user_notin_register(user_name=username):
            return ['error','用户名已存在，请重新输入用户名'] + [None] * 6 + [dash.no_update]
        if len(password) > 20:
            return [None]*2 + ['error','密码超过20位'] + [None] * 4 + [dash.no_update]
        if repeat_password != password:
            return [None]* 4 + ['error', '密码不一致'] + [None] * 2 + [dash.no_update]
        if not check_phone_number(phone):
            return [None] * 6 + ['error','号码为符合格式'] + [dash.no_update]
        with mysql_db.atomic():
            USER_INFO.create(USER_NAME=username, USER_PASSWORD = repeat_password,
                             USER_PASSWORD_MD5 = md5_to_password(password=repeat_password),
                             USER_PHONE = phone, USER_EMAIL = email,
                             USER_UNIT = unit, CREAT_TIME = datetime.now()
                             )
            USER_PERMISSION.create(USER_NAME=username,GENE_ANALYSE_CODE=0,PHENOTYPE_ANALYSE_CODE=0,
                                    SEED_RESOURCE_CODE = 0, REPEAT_SEQUENCE = 0,
                                   HOME_REVIEW = 0
                                   )
        new_user = User()
        new_user.id = username
        login_user(new_user)
        return [None]*8 + ['success']


@app.callback(
    [Output('form_login_username','validateStatus'),
    Output('form_login_username', 'help'),
    Output('form_login_password', 'validateStatus'),
    Output('form_login_password', 'help'),
    Output('form_login_captcha', 'children'),
    Output('login_code','data')],
    Input('login_btn','nClicks'),
    State('login_username','value'),
    State('login_password', 'value'),
    State('to_login_captcha','value'),
    State('login_captcha', 'captcha'),
    prevent_initial_call=True
)
def check_login(n,username,password,to_login_code,login_captcha,):
    """
    1、先判断验证码，
    2、检查用户名是否存在
    3、检查密码是否正确
    :return:
    """
    if n:
        if to_login_code != login_captcha:
            return [None]*4 + ['验证码输入错误'] + [dash.no_update]
        if not username:
            return ['error','未输入账号'] + [None]*4 + [dash.no_update]
        if not password:
            return [None] * 2 + ['error' , '未输入密码'] + [None]  + [dash.no_update]
        if username:
            if check_user_notin_register(user_name=username):
                return ['error','该用户不存在'] + [None] * 3 + [dash.no_update]
        if password:

            query = USER_INFO.select(USER_INFO.USER_NAME).where(USER_INFO.USER_NAME == username,
                                            USER_INFO.USER_PASSWORD_MD5 == md5_to_password(password))
            try:
                database_username = query[0].USER_NAME
            except:
                return [None] * 2 + ['error','密码错误'] + [None,dash.no_update]
            new_user = User()
            new_user.id = database_username
            login_user(new_user)
            return [None] * 5 + ['success']

