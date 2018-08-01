import os

# 项目的路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 静态文件的路径
static_folder = os.path.join(BASE_DIR, 'static')

# 模板文件的路径
template_folder = os.path.join(BASE_DIR, 'templates')

# 上传图片地址
media_folder = os.path.join(static_folder, 'media')
upload_folder = os.path.join(media_folder, 'upload')

# 数据库配置
MYSQL_DATABASE = {
    # 引擎
    'ENGINE': 'mysql',
    # 驱动
    'DRIVER': 'pymysql',
    # 用户名
    'USER': 'root',
    # 密码
    'PASSWORD': '123456',
    # 地址
    'HOST': '127.0.0.1',
    # 端口
    'PORT': '3306',
    # 数据库
    'DB': 'aj',
}

# 配置redis
REDIS_DATABASE = {
    'HOST': '127.0.0.1',
    'PORT': 6379
}
