from webService import webUi
from json import load as jsonLoad
import __auth, __controller

startingPrompt = jsonLoad(open("startingPrompt.json", "r"))[0]["prompt"]

webUi.setAuthTokenCallback(__auth.authTokenCallback)
webUi.setAuthPasswdCallback(__auth.authPasswordCallback)
webUi.setGetSaveNamesCallback(__controller.getSaveNamesCallback)
webUi.setHandleSaveCallback(__controller.handleSaveCallback)
webUi.setHandleOptionsCallback(__controller.handleOptionsCallback)
webUi.setStartCallback(__controller.startCallback)
webUi.setInputCallback(__controller.inputCallback)

# generator.debug = False
# generator.parseAiSettings()
# generator.setStartingText(startingPrompt)
# generator.styleHintPrompt = "Describe the surroundings and character's behavior in detail. Do not mention what \"You\" have done."
# generator.generateText()

webUi.init(__name__)
webUi.run(10000, False)