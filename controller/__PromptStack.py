from enum import Enum

# static variables
_endOfSentenceCommaList = [
    ".",
    "?",
    "!",
]
_promptJoinString = " "
__idCounter = 0


# functions
def _getNewId() -> int:
    global __idCounter
    __idCounter += 1
    return __idCounter - 1


# enums
class PromptType(Enum):
    GENERATED = 0
    SUMMORIZED = 1
    INPUTED = 2
    STARTING = 3


# classes
class Prompt:

    def __init__(self, type: PromptType, text: str, debug: bool = False):
        self.type = type
        self.__text = self.__processText(text)
        if len(self.__text) == 0:
            self.__wordCount = 0
            self.__id = 0
            return
        self.__calcWordCount()
        self.__id = _getNewId()

    def __processText(self, text: str) -> str:
        # remove the last incomplete sentence
        while len(text) > 0 and text[-1] not in _endOfSentenceCommaList:
            text = text[:-1]
        return text.strip()

    def __calcWordCount(self) -> int:
        self.__wordCount = len(self.__text.split(" "))

    def getWordCount(self) -> int:
        return self.__wordCount

    def getId(self):
        return self.__id

    def getText(self):
        return self.__text

    def updateText(self, text: str) -> None:
        self.__text = text

    def getJson(self) -> dict:
        return {
            "type": self.type.name,
            "text": self.__text,
            "id": self.__id,
        }


class PromptStack:

    def __init__(self, debug: bool = False):
        self.__debug = debug
        self.__activePrompts = []
        self.__allPromptHistory = []
        self.__wordCount = 0

    def parseJson(self, json: dict) -> None:
        self.__debug = False
        self.__activePrompts = []
        self.__allPromptHistory = []
        self.__wordCount = 0
        for item in json["all"]:
            self.__allPromptHistory.append(
                Prompt(PromptType[item["type"]], item["text"]))
        for item in json["active"]:
            self.__activePrompts.append(
                Prompt(PromptType[item["type"]], item["text"]))
        self.__recalculateWordCount()

    def addPrompt(self, prompt: Prompt):
        if prompt.getWordCount() == 0:
            if self.__debug:
                print("Got empty prompt")
            return
        self.__activePrompts.append(prompt)
        self.__allPromptHistory.append(prompt)
        self.__recalculateWordCount()

    def __recalculateWordCount(self):
        count = 0
        for prompt in self.__activePrompts:
            count += prompt.getWordCount()
        self.__wordCount = count

    def getWordCount(self) -> int:
        return self.__wordCount

    def getFullPrompt(self) -> list[Prompt]:
        return self.__allPromptHistory

    def getFullPromptText(self) -> str:
        strList = (item.getText() for item in self.__allPromptHistory)
        return _promptJoinString.join(strList)

    def getSummorizedPromptText(self) -> str:
        strList = (item.getText() for item in self.__activePrompts)
        return _promptJoinString.join(strList)

    def getSummorizedPromptTextExcept(self, count: int) -> str:
        strList = (item.getText() for item in self.__activePrompts[:-count])
        return _promptJoinString.join(strList)

    def summorizeActivePrompt(self, summary: Prompt, exceptCount: int = 0):
        target = [summary]
        for prompt in self.__activePrompts[-exceptCount:]:
            target.append(prompt)
        self.__activePrompts = target
        self.__recalculateWordCount()

    def removeBack(self, count: int = 1) -> int:
        for i in range(count):
            if self.__activePrompts[-1].type != PromptType.SUMMORIZED:
                self.__activePrompts = self.__activePrompts[:-1]
                self.__allPromptHistory = self.__allPromptHistory[:-1]
            else:
                return i
        return -1  # -1 is normal instead

    def getJson(self) -> list[dict]:
        return {
            "all": [item.getJson() for item in self.__allPromptHistory],
            "active": [item.getJson() for item in self.__activePrompts],
        }
