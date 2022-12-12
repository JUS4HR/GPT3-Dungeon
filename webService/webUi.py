import flask as __f
from typing import Callable, Dict

__app = None


def __callbackPlaceholder(input: dict) -> dict:
    __app.logger.warning("Callback not set")
    return input


__callback = __callbackPlaceholder


def init(name: str):
    global __app
    __app = __f.Flask(name,
                      template_folder="webService/html",
                      static_folder="webService/html")

    @__app.route("/")
    def index():
        return __f.render_template("index.html")

    @__app.route('/process', methods=['POST'])
    def process_text():
        form = __f.request.json
        result = __callback(form)
        return __f.jsonify(result)


def log(*args, **kwargs):
    __app.logger.info(*args, **kwargs)


def setCallback(callback: Callable[[dict], dict]):
    global __callback
    __callback = callback


def run(port: int, debug: bool = False):
    __app.debug = debug
    __app.run(host="0.0.0.0", port=port)


if __name__ == '__main__':
    __app.run(host="0.0.0.0", port=10000)