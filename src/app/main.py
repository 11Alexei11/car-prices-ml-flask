from flask import Flask

import sys
for p in sys.path:
    print(p)

from users.views import users_bp


def main():
    app = Flask(__name__)
    app.register_blueprint(users_bp)

    app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == "__main__":
    main()