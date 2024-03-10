from functools import wraps

from flask import request, session, redirect, url_for, current_app


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            current_app.logger.warning("There is no user under current session. You should be loged in")
            return redirect(url_for('users.get_login_page', next=request.url))
        return f(*args, **kwargs)
    return decorated_function