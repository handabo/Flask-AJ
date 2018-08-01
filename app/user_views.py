
import random
import re
import os

from flask import Blueprint, render_template, jsonify,\
    session, request

from app.models import db, User
from utils import status_code
from utils.functions import is_login
from utils.settings import upload_folder

# 实例化user蓝图
user_blueprint = Blueprint('user', __name__)


# 创建数据库表
@user_blueprint.route('/create_db/', methods=['GET'])
def create_db():
    db.create_all()
    return '创建数据库表成功'


# 生成验证码
@user_blueprint.route('/get_code/', methods=['GET'])
def get_code():
    code = ''
    s='1234567890qwertyuiopasdfghjklzxcvbnm'
    for i in range(4):
        code += random.choice(s)
    session['code'] = code
    return jsonify(code=200, msg='请求成功', data=code)


# 进入注册页面
@user_blueprint.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


# 注册函数
@user_blueprint.route('/register/', methods=['POST'])
def my_register():
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')

    # 验证参数是否完整
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify(status_code.USER_REGISTER_PARAMS_VALID)
    # 验证图片验证码是否正确
    if session.get('code') != imagecode:
        return jsonify(status_code.USER_REGISTER_CODE_ERROR)
    # 验证手机号，^1[3456789]\d{9}$
    if not re.match(r'^1[3456789]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_INVALID)
    # 验证密码
    if passwd != passwd2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_ERROR)
    # 验证手机号是否存在
    if User.query.filter(User.phone==mobile).count():
        # 数据库中已存在
        return jsonify(status_code.USER_REGISTER_MOBILE_EXSIST)
    # 数据库中不存在该手机号
    user = User()
    user.phone = mobile
    user.password = passwd
    user.name = mobile
    try:
        user.add_update()
        return jsonify(status_code.SUCCESS)
    except:
        return jsonify(status_code.DATABASE_ERROR)


# 进入登陆页面
@user_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


# 登陆函数
@user_blueprint.route('/login/', methods=['POST'])
def my_login():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    # 校验完整参数
    if not all([mobile, password]):
        return jsonify(status_code.USER_LOGIN_PARAMS_VALID)
    # 验证手机号，^1[3456789]\d{9}$
    if not re.match(r'^1[3456789]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_INVALID)

    user = User.query.filter(User.phone == mobile).first()
    # 校验用户，查看用户是否存在
    if user:
        if user.check_pwd(password):
            # 密码校验成功
            session['user_id'] = user.id
            return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.USER_LOGIN_PASSWORD_INVALID)
    else:
        return jsonify(status_code.USER_LOGIN_PHONE_INVALID)


# 退出函数
@user_blueprint.route('/logout/', methods=['GET'])
def logout():
    session.clear()
    return jsonify(status_code.SUCCESS)


# 进入我的页面
@user_blueprint.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


# 获取用户名和手机号函数
@user_blueprint.route('/user_info/', methods=['GET'])
@is_login
def user_info():
    user_id = session['user_id']
    user = User.query.get(user_id)
    user_info = user.to_basic_dict()
    return jsonify(user_info=user_info, code=status_code.OK)


# 进入修改页面
@user_blueprint.route('/profile/', methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


# 修改头像和用户名函数
@user_blueprint.route('/profile/', methods=['PATCH'])
@is_login
def my_profile():
    # 修改头像
    avatar = request.files.get('avatar')
    name = request.form.get('name')
    if avatar:
        # 验证图片  mimetype='image/jpeg' 'image/png'
        if not re.match(r'image/*', avatar.mimetype):
            return jsonify(status_code.USER_USERINFO_PROFILE_ACATAR_INVALID)
        # 图片保存  static/media/upload/xxx.jpg
        avatar.save(os.path.join(upload_folder, avatar.filename))
        # 修改用户的acatar字段
        user = User.query.get(session['user_id'])
        avatar_addr = os.path.join('upload', avatar.filename)
        user.avatar = avatar_addr
        try:
            user.add_update()
            return jsonify(code=status_code.OK, avatar=avatar_addr)
        except:
            return jsonify(status_code.DATABASE_ERROR)

    if name:
        # 修改用户名
        if User.query.filter(User.name==name).count():
            return jsonify(status_code.USER_USERINFO_NAME_EXSITS)
        user = User.query.get(session['user_id'])
        user.name = name
        try:
            user.add_update()
            return jsonify(code=status_code.OK)
        except:
            return jsonify(status_code.DATABASE_ERROR)


# 进入实名认证页面
@user_blueprint.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


# 实名认证函数
@user_blueprint.route('/auth/', methods=['PATCH'])
def my_auth():
    read_name = request.form.get('read_name')
    id_card = request.form.get('id_card')

    if not all([read_name, id_card]):
        return jsonify(status_code.USER_USERINFO_ID_NAME_CARD_INVALID)

    if not re.match(r'[1-9]\d{16}[0-9X]',id_card):
        return jsonify(status_code.USER_USERINFO_ID_CARD_INVALID)

    user = User.query.get(session['user_id'])
    user.id_name = read_name
    user.id_card = id_card
    try:
        user.add_update()
        return jsonify(code=status_code.OK)
    except Exception as e:
        print(e)
        return jsonify(status_code.DATABASE_ERROR)


# 已经实名认证进入该页面不在进行认证
@user_blueprint.route('/read_user_info/', methods=['GET'])
def read_user_info():
    user = User.query.get(session['user_id'])
    user = user.to_auth_dict()
    return jsonify(code=status_code.OK, user=user)
