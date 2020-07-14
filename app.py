from flask import *
from common import database


app = Flask(__name__)


@app.route('/')
def home():
    template = "/coming-soon/coming-soon.html"
    return render_template(template)


if __name__ == '__main__':
    database.Database()
    app.run(debug=True)
