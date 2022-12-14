from . import __OpenaiAdapter as _OpenaiAdapter, __PromptStack as _PromptStack
import json

# recommended workflow:
# | starting prompt
# | get response once according to starting prompt
# | user input (@ normal input / @ command)                              Loop back here <-------+
# | (if command, do as asked)                                                                   |
# | generate new response according to history                                                  |
# | if total word count too much, summorize all(or all but the last ones) into shorter version  |
# +---------------------------------------------------------------------------------------------+

_confJsonPathPrefix = "config/generator/u-"
_confJsonPathSuffix = ".json"
_saveJsonPathPrefix = "saves/save-u-"
_saveJsonPathSuffix = ".json"


class Generator:

    def __init__(self, uid: int, saveName: str, debug=False) -> None:
        self.__debug = debug
        self.__uid = uid
        self.__saveName = saveName
        self.__configPath = _confJsonPathPrefix + str(
            self.__uid) + _confJsonPathSuffix
        self.__savePath = _saveJsonPathPrefix + str(
            self.__uid) + _saveJsonPathSuffix

        if not self.__loadFromConfig():
            self.__openaiAdapter = _OpenaiAdapter.OpenAIAdapter(
                self.key, self.__debug)
            self.__parseDefaultConfig()
            self.serializeToConfig()
        if self.__saveName == "" or not self.__loadFromSave(self.__saveName):
            self.promptStack = _PromptStack.PromptStack(debug)

        self.__generatingPrompt = "\nContinue the story above. "
        self.__generateSuffix = "\nContinues: "
        self.__summarizingPrompt = "\nSummarize the story above into " + str(
            self.summarizingSentenceCount) + " sentences."
        self.__summarizeSuffix = "\nResult: "

    # functions
    def __parseAiSettings(self) -> None:
        self.__openaiAdapter.setParams(
            engine=self.aiSettings["engine"],
            temperature=float(self.aiSettings["temperature"]),
            max_tokens=int(self.aiSettings["max_tokens"]),
            top_p=float(self.aiSettings["top_p"]),
            frequency_penalty=float(self.aiSettings["frequency_penalty"]),
            presence_penalty=int(self.aiSettings["presence_penalty"]),
        )

    def setStartingText(self, text: str) -> None:
        if len(self.promptStack.getFullPrompt()) == 0:
            self.promptStack.addPrompt(
                _PromptStack.Prompt(_PromptStack.PromptType.STARTING, text))
        else:
            print("Starting text set when stack is not empty")

    def addUserInputText(self, text: str) -> None:
        self.promptStack.addPrompt(
            _PromptStack.Prompt(_PromptStack.PromptType.INPUTED, text))
        self.__dealWithPromptTooLong()

    def generateText(self) -> None:
        prompt = self.promptStack.getSummorizedPromptText()
        prompt += self.__generatingPrompt + self.styleHintPrompt + self.__generateSuffix
        generatedText = self.__openaiAdapter.generateResponse(prompt)
        self.promptStack.addPrompt(
            _PromptStack.Prompt(_PromptStack.PromptType.GENERATED,
                               generatedText))
        self.__dealWithPromptTooLong()
        self.serializeToSave()

    def __dealWithPromptTooLong(self) -> None:
        if self.__debug:
            print("Word count now:", self.promptStack.getWordCount())
        if self.promptStack.getWordCount() > self.wordCountThreshold:
            prompt = self.promptStack.getSummorizedPromptTextExcept(
                self.promptsToKeepWhenSummarizing)
            prompt += self.__summarizingPrompt + self.__summarizeSuffix
            self.__openaiAdapter.setParams(
                max_tokens=self.aiSettings["max_tokens_summary"])
            summary = self.__openaiAdapter.generateResponse(prompt)
            self.__openaiAdapter.setParams(
                max_tokens=self.aiSettings["max_tokens"])
            self.promptStack.summorizeActivePrompt(
                _PromptStack.Prompt(_PromptStack.PromptType.SUMMORIZED, summary),
                self.promptsToKeepWhenSummarizing)
            if self.__debug:
                print("summarizing from: [" + prompt + "]")
                print("into: [" + summary + "]")

    def __parseDefaultConfig(self):
        # config
        self.key = ""
        self.wordCountThreshold = 300
        self.promptsToKeepWhenSummarizing = 4
        self.styleHintPrompt = "Describe the surroundings and character's behavior in detail. Do not mention what [You] have done"
        self.summarizingSentenceCount = 4
        self.aiSettings = {
            "engine": "curie-instruct-beta",
            "temperature": 0.6,
            "max_tokens": 200,
            "max_tokens_summary": 500,
            "top_p": 0.95,
            "frequency_penalty": 1.0,
            "presence_penalty": 0,
        }
        # end of config

    def serializeToConfig(self):
        output = {
            "key": self.key,
            "wordCountThreshold": self.wordCountThreshold,
            "promptsToKeepWhenSummarizing": self.promptsToKeepWhenSummarizing,
            "styleHintPrompt": self.styleHintPrompt,
            "summarizingSentenceCount": self.summarizingSentenceCount,
            "aiSettings": self.aiSettings,
        }
        with open(self.__configPath, "w") as f:
            json.dump(output, f)

    def __loadFromConfig(self) -> bool:
        try:
            with open(self.__configPath) as f:
                data = json.load(f)
                self.key = data["key"]
                self.wordCountThreshold = int(data["wordCountThreshold"])
                self.promptsToKeepWhenSummarizing = int(
                    data["promptsToKeepWhenSummarizing"])
                self.styleHintPrompt = data["styleHintPrompt"]
                self.summarizingSentenceCount = int(
                    data["summarizingSentenceCount"])
                self.aiSettings = data["aiSettings"]
                self.__openaiAdapter = _OpenaiAdapter.OpenAIAdapter(
                    self.key, self.__debug)
                self.__parseAiSettings()
                return True
        except Exception as e:
            # if self.__debug:
            print("Error loading config:", e)
            return False

    def serializeToSave(self, ) -> None:
        data = self.promptStack.getJson()
        with open(self.__savePath, "r") as f:
            oldData = json.load(f)
            for save in oldData:
                if save["name"] == self.__saveName:
                    oldData.remove(save)
                    break
            oldData.append({
                "name": self.__saveName,
                "data": data,
            })
        with open(self.__savePath, "w") as f:
            json.dump(oldData, f)

    def getSaveNames(self) -> list:
        try:
            with open(self.__savePath) as f:
                data = json.load(f)
                return [x["name"] for x in data]
        except Exception as e:
            if self.__debug:
                print("Error loading saves:", e)
            return []

    def getSettings(self) -> dict:
        return {
            "key": self.key,
            "wordCountThreshold": self.wordCountThreshold,
            "promptsToKeepWhenSummarizing": self.promptsToKeepWhenSummarizing,
            "styleHintPrompt": self.styleHintPrompt,
            "summarizingSentenceCount": self.summarizingSentenceCount,
            "aiSettings": self.aiSettings,
        }

    def getEngineList(self) -> list:
        return self.__openaiAdapter.getEngineList()

    def __loadFromSave(self, saveName: str):
        try:
            with open(self.__savePath) as f:
                data = json.load(f)
                for x in data:
                    if x["name"] == saveName:
                        self.promptStack = _PromptStack.PromptStack(
                            self.__debug)
                        self.promptStack.parseJson(x["data"])
                        return True
        except Exception as e:
            print("Error loading save:", e)
            return False

    def createSave(self):
        try:
            with open(self.__savePath, "r") as f:
                oldSaves = json.load(f)
                for saves in oldSaves:
                    if saves["name"] == self.__saveName:
                        return False
        except:
            oldSaves = []
        oldSaves.append({
            "name": self.__saveName,
            "data": self.promptStack.getJson(),
        })
        with open(self.__savePath, "w") as f:
            json.dump(oldSaves, f)
        return True

    def deleteSave(self):
        with open(self.__savePath, "r") as f:
            oldSaves = json.load(f)
            for saves in oldSaves:
                if saves["name"] == self.__saveName:
                    oldSaves.remove(saves)
                    break
        with open(self.__savePath, "w") as f:
            json.dump(oldSaves, f)
        return True

    def parseJsonConf(self, input: dict):
        if "key" in input:
            self.key = input["key"]
        if "wordCountThreshold" in input:
            self.wordCountThreshold = input["wordCountThreshold"]
        if "promptsToKeepWhenSummarizing" in input:
            self.promptsToKeepWhenSummarizing = input[
                "promptsToKeepWhenSummarizing"]
        if "styleHintPrompt" in input:
            self.styleHintPrompt = input["styleHintPrompt"]
        if "summarizingSentenceCount" in input:
            self.summarizingSentenceCount = input["summarizingSentenceCount"]
        if "aiSettings" in input:
            self.aiSettings = input["aiSettings"]
        self.__parseAiSettings()
        self.serializeToConfig()
        return True