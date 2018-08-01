from flask_script import Manager

from utils.app import create_app

# 创建flask对象app
app = create_app()

# 使用Manager去管理flask对象app
manage = Manager(app)

if __name__ == '__main__':

    # app.run(debug=True, port=8000, host='127.0.0.1')
    manage.run()