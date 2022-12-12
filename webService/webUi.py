import flask as __f
from typing import Callable, Dict

app = __f.Flask(__name__, template_folder="html", static_folder="html")


def __callbackPlaceholder(input: dict) -> dict:
    return input


__callback = __callbackPlaceholder


@app.route("/")
def index():
    return __f.render_template("index.html")


@app.route('/process', methods=['POST'])
def process_text():
    form = __f.request.json

    result = __callback(form)
    return __f.jsonify(result)


def setCallback(callback: Callable[[dict], dict]):
    global __callback
    __callback = callback


def run(port: int):
    app.run(host="0.0.0.0", port=port)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)