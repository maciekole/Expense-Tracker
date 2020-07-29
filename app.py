from flask import *
from common import database


APP = Flask(__name__)
SESSIONS = {}


@APP.route('/')
def home():
    template = "/coming-soon/coming-soon.html"
    return render_template(template)


if __name__ == '__main__':
    database.Database(cfg_from_file=False)
    APP.run(debug=True)
