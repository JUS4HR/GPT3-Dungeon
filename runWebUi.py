from webService import webUi
from json import load as jsonLoad
import __auth_old, __controller_old

startingPrompt = jsonLoad(open("startingPrompt.json", "r"))[0]["prompt"]

webUi.setAuthTokenCallback(__auth_old.authTokenCallback)
webUi.setAuthPasswdCallback(__auth_old.authPasswordCallback)
webUi.setGetSaveNamesCallback(__controller_old.getSaveNamesCallback)
webUi.setHandleSaveCallback(__controller_old.handleSaveCallback)
webUi.setHandleOptionsCallback(__controller_old.handleOptionsCallback)
webUi.setStartCallback(__controller_old.startCallback)
webUi.setInputCallback(__controller_old.inputCallback)

# generator.debug = False
# generator.parseAiSettings()
# generator.setStartingText(startingPrompt)
# generator.styleHintPrompt = "Describe the surroundings and character's behavior in detail. Do not mention what \"You\" have done."
# generator.generateText()

webUi.init(__name__)
webUi.run(10000, False)