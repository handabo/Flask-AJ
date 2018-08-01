OK = 200
SUCCESS = {'code': 200, 'msg': '请求成功'}
DATABASE_ERROR = {'code': 500, 'msg': '数据库崩了'}

# 用户模块
USER_REGISTER_CODE_ERROR = {'code': 1000, 'msg': '验证码错误'}
USER_REGISTER_PARAMS_VALID = {'code': 1001, 'msg': '请填写完整的注册参数'}
USER_REGISTER_MOBILE_INVALID = {'code': 1002, 'msg': '手机格式不正确'}
USER_REGISTER_PASSWORD_ERROR = {'code': 1003, 'msg': '两次密码不正确'}
USER_REGISTER_MOBILE_EXSIST = {'code': 1004, 'msg': '手机号已存在，请登录'}

USER_LOGIN_PARAMS_VALID = {'code': 1005, 'msg': '请填写完整的登录信息'}
USER_LOGIN_PASSWORD_INVALID = {'code': 1006, 'msg': '登录密码不正确'}
USER_LOGIN_PHONE_INVALID = {'code': 1007, 'msg': '请填写正确的手机号'}

USER_USERINFO_PROFILE_ACATAR_INVALID = {'code': 1008, 'msg': '请上传正确的图片格式'}
USER_USERINFO_NAME_EXSITS = {'code': 1009, 'msg': '用户名已存在'}

USER_USERINFO_ID_NAME_CARD_INVALID = {'code': 1010, 'msg': '请填写完整的实名认证信息'}
USER_USERINFO_ID_CARD_INVALID = {'code': 1011, 'msg': '身份证信息错误'}

# 房屋模块
HOUSE_USER_INFO_ID_CARD_INVALID = {'code': 1100, 'msg': '用户没有实名认证'}
