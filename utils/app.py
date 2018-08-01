import redis
from flask import Flask
from flask_session import Session
from flask_debugtoolbar import DebugToolbarExtension

from app.user_views import user_blueprint
from app.order_view import order_blueprint
from app.house_view import house_blueprint
from app.models import db
from utils.functions import get_sqlalchemy_uri

from utils.settings import static_folder, template_folder, MYSQL_DATABASE, REDIS_DATABASE


def create_app():
    # 创建flask对象app
    app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

    # 创建总路由
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(house_blueprint, url_prefix='/house')
    app.register_blueprint(order_blueprint, url_prefix='/order')

    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = get_sqlalchemy_uri(MYSQL_DATABASE)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # 配置redis-->session
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host=REDIS_DATABASE['HOST'], port=REDIS_DATABASE['PORT'])
    se = Session()
    se.init_app(app)

    # 配置debug模式
    # app.config['SECRET_KEY'] = 'secret_key'
    # app.debug = True
    # bar = DebugToolbarExtension()
    # bar.init_app(app)

    return app