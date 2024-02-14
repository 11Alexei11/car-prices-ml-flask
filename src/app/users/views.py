from flask import Blueprint, render_template


users_bp = Blueprint("users", import_name=__name__, static_folder='static', template_folder='templates')


@users_bp.route('/user/login', methods=['GET'])
def get_login_page():
    return render_template('login_form.html')