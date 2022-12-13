from controller import generator
from copy import deepcopy as copyDeep
import __utils

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


def __promptToJson(prompt: generator.PromptStack.Prompt) -> dict:
    newPromptJson = copyDeep(sendContentTemplate)
    if prompt.type == generator.PromptStack.PromptType.INPUTED:
        newPromptJson["type"] = "user"
    else:
        newPromptJson["type"] = "generated"
    newPromptJson["id"] = prompt.getId()
    newPromptJson["content"] = prompt.getText()
    return newPromptJson


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
        return "You " + __utils.firstToSecondPerson(text)
    elif mode.lower() == "story":
        return text[0].upper() + text[1:]
    else:
        raise Exception("Invalid user mode")


def startCallback() -> dict:
    jsonToSend = copyDeep(sendContentListTemplate)
    for prompt in generator.promptStack.getFullPrompt():
        jsonToSend["new-content-list"].append(__promptToJson(prompt))
    return jsonToSend


def inputCallback(input: dict) -> dict:
    # supports commands until buttons are implemented
    jsonToSend = copyDeep(sendContentListTemplate)
    if len(input["user-input"]) > 0 and input["user-input"][0] == "/":
        command = input["user-input"][1:]
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
