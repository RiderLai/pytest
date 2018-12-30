from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/')
def index():
    user_input = request.args.get('aa', '')
    return '<h1>hello</h1>' + user_input


if __name__ == '__main__':
    app.run(debug=True)