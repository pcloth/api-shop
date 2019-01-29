from flask import Flask, request, render_template_string

from bule.views import simple_page

from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
app.register_blueprint(simple_page)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
