from flask import *
from common.database import Database
from common.user import User


APP = Flask(__name__)
SESSIONS = {}


@APP.route('/')
def home():
    template = "/coming-soon/coming-soon.html"
    return render_template(template)


if __name__ == '__main__':
    Database(cfg_from_file=False)
    APP.run(debug=True)
