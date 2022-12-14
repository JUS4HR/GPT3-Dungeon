from json import load as jsonLoad

import authenticate
import controller
from webUI import App

app = App(name=__name__,
          template_folder="webService/html",
          static_folder="webService/static")

app.setIndexCallback(controller.redirIndexCallback)

# auth
app.addCallback("auth-password", authenticate.authPasswordCallback)
app.addCallback("auth-token", authenticate.authTokenCallback)

# redirect
app.addCallback("login", controller.redirIndexCallback)
app.addCallback("play", controller.redirPlayCallback)
app.addCallback("options", controller.redirOptionsCallback)

# handle
app.addCallback("handle-save", controller.handleSaveCallback)
app.addCallback("handle-options", controller.handleOptionsCallback)
app.addCallback("start", controller.startCallback)
app.addCallback("process", controller.inputCallback)
app.addCallback("get-settings", controller.getSettingsCallback)
app.addCallback("content-retry", controller.retryCallback)
app.addCallback("content-edit", controller.editCallback)

app.run(port=10000)