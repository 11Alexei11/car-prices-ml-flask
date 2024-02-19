from flask import Blueprint, render_template, request

from src.app.users.models.user import User

users_bp = Blueprint("users", import_name=__name__, static_folder='static', template_folder='templates')


@users_bp.route('/user/login/form', methods=['GET'])
def get_login_page():
    return render_template('login_form.html')


@users_bp.route('/user/registration/form', methods=['GET'])
def get_registration_page():
    return render_template("registration_form.html")


@users_bp.route('/user/registration/registrate', methods=['POST'])
def handle_register_action():
    from src.app import db

    if request.method.upper() == "POST":
        input_name = request.form['name']
        input_email = request.form['email']
        input_password = request.form['password']
        try:
            with db.atomic():
                user = User.get(User.name==input_name, User.email==input_email, User.password==input_password)
                return render_template('notification_bad_registration.html')
        except:
            user = User(
                name=input_name,
                email=input_email,
                password=input_password
            )
            user.save()
            return render_template('notification_sucessfull_registration.html')
    else:
        raise Exception('this request statust should be post')