import flask as __f
from typing import Callable, Dict

__app = None


def __callbackPlaceholder(input: dict) -> dict:
    __app.logger.warning("Callback not set")
    return {}


__authTokenCallback = __callbackPlaceholder
__authPasswdCallback = __callbackPlaceholder
__startCallback = __callbackPlaceholder
__inputCallback = __callbackPlaceholder


def init(name: str):
    global __app
    __app = __f.Flask(name,
                      template_folder="webService/html",
                      static_folder="webService/static")

    @__app.route("/")
    def loadIndex():
        if __f.request.args.get("play") == "True":
            __app.logger.info("load play")
            return __f.render_template("play.html")
        else:
            __app.logger.info("load index")
            return __f.render_template("login.html")

    @__app.route("/auth-token", methods=["POST"])
    def authToken():
        form = __f.request.json
        return __f.jsonify(__authTokenCallback(form))

    @__app.route("/auth-password", methods=["POST"])
    def authPassword():
        form = __f.request.json
        return __f.jsonify(__authPasswdCallback(form))

    @__app.route("/start", methods=["POST"])
    def processStart():
        return __f.jsonify(__startCallback({}))

    @__app.route('/process', methods=['POST'])
    def processInput():
        form = __f.request.json
        return __f.jsonify(__inputCallback(form))


def log(*args, **kwargs):
    __app.logger.info(*args, **kwargs)


def setAuthTokenCallback(callback: Callable[[], dict]):
    global __authTokenCallback
    __authTokenCallback = callback


def setAuthPasswdCallback(callback: Callable[[], dict]):
    global __authPasswdCallback
    __authPasswdCallback = callback


def setStartCallback(callback: Callable[[], dict]):
    global __startCallback
    __startCallback = callback


def setInputCallback(callback: Callable[[dict], dict]):
    global __inputCallback
    __inputCallback = callback


def run(port: int, debug: bool = False):
    __app.debug = debug
    __app.run(host="0.0.0.0", port=port)


if __name__ == '__main__':
    __app.run(host="0.0.0.0", port=10000)