
from functools import wraps

from flask import session, redirect, url_for


def get_sqlalchemy_uri(DATABASE):

    return '%s+%s://%s:%s@%s:%s/%s' % (DATABASE['ENGINE'],
                                       DATABASE['DRIVER'],
                                       DATABASE['USER'],
                                       DATABASE['PASSWORD'],
                                       DATABASE['HOST'],
                                       DATABASE['PORT'],
                                       DATABASE['DB']
                                       )


def is_login(func):

    @wraps(func)
    def check_login(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))

    return check_login

