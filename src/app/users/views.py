from flask import Blueprint, render_template, request, current_app, session, url_for, redirect
from src.app.users.models.user import User


users_bp = Blueprint(
    name="users",
    import_name=__name__,
    static_folder='static',
    template_folder='templates',
    url_prefix="/users"
)


@users_bp.route('/')
def index():
    current_app.logger.info(session.items())
    session_str = ""
    for key, value in session.items():
        session_str += f"{key}: {value}\n"
    current_app.logger.info(session_str)

    return 'You are logged in'


@users_bp.route('login-form', methods=['GET'])
def get_login_page():
    return render_template('login/login_form.html')


@users_bp.route('login/', methods=['POST'])
def handle_login_action():
    from src.app import db

    current_app.logger.info(f"request.method: {request.method.upper()}")
    if request.method.upper() == "POST":
        input_email = request.form['email']
        input_password = request.form['password']

        try:
            with db.atomic():
                current_app.logger.info(f"Start checking: If input_email: {input_email} in database")
                user = User.get(User.email==input_email, User.password==input_password)
                current_app.logger.info(f"User with such email in system: {input_email} sucessfully loged in")
                current_app.logger.info(f"session before: {session.keys()}")
                session[f"user_id"] = user.user_id
                current_app.logger.info(f"session after: {session.keys()}")

                return redirect(url_for("price_predictions.get_price_form"))

        except Exception as e:
            current_app.logger.error(e)
            current_app.logger.info('Something went wrong. Try to pass another email or password')

            return render_template('login/notification_bad_login.html')
    else:
        raise Exception('this request statust should be post')


@users_bp.route('registration-form', methods=['GET'])
def get_registration_page():
    return render_template("registration/registration_form.html")


@users_bp.route('registrate', methods=['POST'])
def handle_register_action():
    from src.app import db

    if request.method.upper() == "POST":
        input_name = request.form['name']
        input_email = request.form['email']
        input_password = request.form['password']
        try:
            with db.atomic():
                current_app.logger.info("Start checking: If input_email in database")
                user = User.get(User.email==input_email)
                current_app.logger.info(f"Print: Failed to registrate user. User with email: {input_email} is already in database")

                return render_template('registration/notification_bad_registration.html')
        except:
            user = User(
                name=input_name,
                email=input_email,
                password=input_password
            )
            current_app.logger.info(f"User was successfully created: {user.user_id}, {user.name}, {user.email}, {user.password}")
            user.save(force_insert=True)
            current_app.logger.info('User successfully saved in database')

            return render_template('registration/notification_sucessfull_registration.html')
    else:
        raise Exception('this request statust should be post')
