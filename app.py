from flask import Flask, request, render_template_string

from flask_demo.views import simple_page
from flask_script import Shell, Manager

from werkzeug.routing import BaseConverter
from flask_demo import init_db


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.register_blueprint(simple_page)
init_db()
# manager = Manager(app)

if __name__ == '__main__':
    # manager.add_command('shell', Shell(make_context=make_shell_context))
    app.run(host="0.0.0.0",port=9100, debug=True)
