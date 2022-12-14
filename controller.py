from typing import Any as _Any
from typing import Dict as _Dict

import __utils as _utils
from generateController import generator as _gen
from webUI import CallableInputType as _CallableInputType
from webUI import CallbackReturnType as _CallbackReturnType
from webUI import ResponseType as _ResponseType


def _getContentListTemplate() -> _Dict[str, _Any]:
    return {
        "new-content-list": [],
        "modified-content-list": [],
        "active-word-count": 0,
        "last-time-summarized": 0,
    }


def _getContentTemplate() -> _Dict[str, _Any]:
    return {
        "type": "",
        "id": 0,
        "content": "",
    }


def __promptToJson(prompt: _gen._PromptStack.Prompt) -> dict:
    newPromptJson: _Dict[str, _Any] = _getContentTemplate()
    if prompt.type == _gen._PromptStack.PromptType.INPUTED:
        newPromptJson["type"] = "user"
    else:
        newPromptJson["type"] = "generated"
    newPromptJson["id"] = prompt.getId()
    newPromptJson["content"] = prompt.getText()
    return newPromptJson


def __parseUserInput(mode: str, text: str) -> str:
    if text == "":
        return ""
    if mode.lower() == "say":
        text = text.strip("\"")
        text = "You say \"" + text[0].upper() + text[1:]
        if (text[-1] == "." and text[-1] == "!" and text[-1] == "?"):
            text += "\""
        else:
            text += ".\""
        return text
    elif mode.lower() == "do":
        text = _utils.firstToSecondPerson(text)
        return "You " + text[0].lower() + text[1:]
    elif mode.lower() == "story":
        return text[0].upper() + text[1:]
    else:
        raise Exception("Invalid user mode")


def startCallback(input: _CallableInputType) -> _CallbackReturnType:
    generator = _gen.Generator(input["uid"], input["save-name"])
    jsonToSend = _getContentListTemplate()
    for prompt in generator.promptStack.getFullPrompt():
        jsonToSend["new-content-list"].append(__promptToJson(prompt))
    return _ResponseType.JSON, jsonToSend


def inputCallback(input: _CallableInputType) -> _CallbackReturnType:
    generator = _gen.Generator(input["uid"], input["save-name"])
    jsonToSend = _getContentListTemplate()
    oldPromptIdList = []
    for prompt in generator.promptStack.getFullPrompt():
        oldPromptIdList.append(prompt.getId())
    userInput = __parseUserInput(input["user-mode"], input["user-input"])
    generator.addUserInputText(userInput)
    generator.generateText()
    for prompt in generator.promptStack.getFullPrompt():
        if prompt.getId() not in oldPromptIdList:
            jsonToSend["new-content-list"].append(__promptToJson(prompt))
    # TODO: implement active-word-count and last-time-summarized
    return _ResponseType.JSON, jsonToSend


def getSettingsCallback(input: _CallableInputType) -> _CallbackReturnType:
    generator = _gen.Generator(uid=input["uid"], saveName="")
    return _ResponseType.JSON, {
        "save-names": generator.getSaveNames(),
        "settings": generator.getSettings(),
        "engine-list": generator.getEngineList()
    }


def handleSaveCallback(input: _CallableInputType) -> _CallbackReturnType:
    success = False
    if input["save-name"] != "":
        generator = _gen.Generator(uid=input["uid"],
                                   saveName=input["save-name"])
        if input["operation"] == "create":
            success = generator.createSave()
        elif input["operation"] == "delete":
            success = generator.deleteSave()
    return _ResponseType.JSON, {"success": ("True" if success else "False")}


def handleOptionsCallback(input: _CallableInputType) -> _CallbackReturnType:
    success = False
    generator = _gen.Generator(uid=input["uid"], saveName="")
    generator.parseJsonConf(input)
    return _ResponseType.JSON, {"success": ("True" if success else "False")}


def retryCallback(input: _CallableInputType) -> _CallbackReturnType:
    generator = _gen.Generator(input["uid"], input["save-name"])
    generator.reGenerateLast()
    jsonToSend = _getContentListTemplate()
    jsonToSend["modified-content-list"].append(
        __promptToJson(generator.promptStack.getFullPrompt()[-1]))
    return _ResponseType.JSON, jsonToSend


def editCallback(input: _CallableInputType) -> _CallbackReturnType:
    generator = _gen.Generator(input["uid"], input["save-name"])
    generator.editById(int(input["id"]), input["new-content"])
    jsonToSend = _getContentListTemplate()
    for prompt in generator.promptStack.getFullPrompt():
        if prompt.getId() == int(input["id"]):
            jsonToSend["modified-content-list"].append(__promptToJson(prompt))
            break
    return _ResponseType.JSON, jsonToSend


# redirecting callback
def redirIndexCallback(input: _CallableInputType) -> _CallbackReturnType:
    return _ResponseType.RENDER, {"url": "login.html"}


def redirPlayCallback(input: _CallableInputType) -> _CallbackReturnType:
    return _ResponseType.RENDER, {"url": "play.html"}


def redirOptionsCallback(input: _CallableInputType) -> _CallbackReturnType:
    return _ResponseType.RENDER, {"url": "options.html"}


def redirRegisterCallback(input: _CallableInputType) -> _CallbackReturnType:
    return _ResponseType.RENDER, {"url": "register.html"}
