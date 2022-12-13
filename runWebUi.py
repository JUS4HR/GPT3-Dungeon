from controller import generator
from webService import webUi, utils
from json import load as jsonLoad
from copy import deepcopy as copyDeep
import auth

sendContentListTemplate = {
    "new-content-list": [],
    "modified-content-list": [],
    "active-word-count": 0,
    "last-time-summarized": 0,
}

sendContentTemplate = {
    "type": "",
    "id": 0,
    "content": "",
}

startingPrompt = jsonLoad(open("startingPrompt.json", "r"))[0]["prompt"]

def parseUserInput(mode: str, text: str) -> str:
    if text == "":
        return ""
    if mode.lower() == "say":
        text = text.strip("\"")
        text = "You say \"" + text[0].upper() + text[1:]
        if (text[-1] == "." and text[-1] == "!" and text[-1] == "?"):
            text += "\""
        return text
    elif mode.lower() == "do":
        return "You " + utils.firstToSecondPerson(text)
    elif mode.lower() == "story":
        return text[0].upper() + text[1:]
    else:
        raise Exception("Invalid user mode")

def promptToJson(prompt: generator.PromptStack.Prompt) -> dict:
    webUi.log("parse prompt: " + prompt.getText())
    newPromptJson = copyDeep(sendContentTemplate)
    if prompt.type == generator.PromptStack.PromptType.INPUTED:
        newPromptJson["type"] = "user"
    else:
        newPromptJson["type"] = "generated"
    newPromptJson["id"] = prompt.getId()
    newPromptJson["content"] = prompt.getText()
    return newPromptJson

def startCallback() -> dict:
    jsonToSend = copyDeep(sendContentListTemplate)
    for prompt in generator.promptStack.getFullPrompt():
        jsonToSend["new-content-list"].append(promptToJson(prompt))
    return jsonToSend

def inputCallback(input: dict) -> dict:
    # supports commands until buttons are implemented
    jsonToSend = copyDeep(sendContentListTemplate)
    if len(input["user-input"]) > 0 and input["user-input"][0] == "/":
        command = input["user-input"][1:]
        webUi.log("command: " + command)
        pass  # TODO: implement commands
    else:
        oldPromptIdList = []
        for prompt in generator.promptStack.getFullPrompt():
            oldPromptIdList.append(prompt.getId())
        userInput = parseUserInput(input["user-mode"], input["user-input"])
        generator.addUserInputText(userInput)
        generator.generateText()
        for prompt in generator.promptStack.getFullPrompt():
            if prompt.getId() not in oldPromptIdList:
                jsonToSend["new-content-list"].append(promptToJson(prompt))
    # TODO: implement active-word-count and last-time-summarized
    return jsonToSend


webUi.setAuthTokenCallback(auth.authTokenCallback)
webUi.setAuthPasswdCallback(auth.authPasswordCallback)
webUi.setStartCallback(startCallback)
webUi.setInputCallback(inputCallback)

generator.debug = False
generator.parseAiSettings()
generator.setStartingText(startingPrompt)
generator.styleHintPrompt = "Describe the surroundings and character's behavior in detail. Do not mention what \"You\" have done."
# generator.generateText()

webUi.init(__name__)
webUi.run(10000, False)