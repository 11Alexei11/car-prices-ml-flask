from flask import Blueprint, render_template, request


users_bp = Blueprint("users", import_name=__name__, static_folder='static', template_folder='templates')


@users_bp.route('/user/login/form', methods=['GET'])
def get_login_page():
    return render_template('login_form.html')


# @users_bp.route('/user/registration', methods=['POST'])
# def handle_register_action():
#     if request.method.POST:
#         name = request.method.POST['name']
#         email = request.method.POST['email']
#         password = request.method.POST['password']

#         if not User.objects.filter(NAME=name, EMAIL=email, PASSWORD=password).exists():
#             user = User(
#                 NAME=name,
#                 EMAIL=email,
#                 PASSWORD=password
#             )
#             user.save()
#             print('new user')
#             return redirect('login-form')
#         else:
#             print('existing user')
#             return redirect('registration-form')
#     else:
#         print(request.GET)
#         raise Exception('this requesregister_statust should be post')