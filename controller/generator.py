from . import __OpenaiAdapter, __PromptStack as PromptStack, __utils
import json

# recommended workflow:
# | starting prompt
# | get response once according to starting prompt
# | user input (@ normal input / @ command)                              Loop back here <-------+
# | (if command, do as asked)                                                                   |
# | generate new response according to history                                                  |
# | if total word count too much, summorize all(or all but the last ones) into shorter version  |
# +---------------------------------------------------------------------------------------------+

confJsonPathPrefix = "config/generator/u-"
confJsonPathSuffix = ".json"

class generator:

    def __init__(self, key: str, uid: int, debug=False) -> None:
        self.__debug = debug
        self.__key = key
        self.__uid = uid
        
        self.__loadFromConfig()
        self.__parseDefaultConfig()
        
        self.__generatingPrompt = "\nContinue the story above. "
        self.__generateSuffix = "\nContinues: "
        self.__summarizingPrompt = "\nSummarize the story above into " + str(
            self.summarizingSentenceCount) + " sentences."
        self.__summarizeSuffix = "\nResult: "
        self.__configPath = confJsonPathPrefix + str(uid) + confJsonPathSuffix
        self.__openaiAdapter = __OpenaiAdapter.OpenAIAdapter(
            self.__key, self.__debug)
        
        self.promptStack = PromptStack.PromptStack(debug)

    # functions
    def __parseAiSettings(self) -> None:
        self.__openaiAdapter.setParams(
            engine=self.aiSettings["engine"],
            temperature=self.aiSettings["temperature"],
            max_tokens=self.aiSettings["max_tokens"],
            top_p=self.aiSettings["top_p"],
            frequency_penalty=self.aiSettings["frequency_penalty"],
            presence_penalty=self.aiSettings["presence_penalty"],
        )

    def setStartingText(self, text: str) -> None:
        if len(self.promptStack.getFullPrompt()) == 0:
            self.promptStack.addPrompt(
                PromptStack.Prompt(PromptStack.PromptType.STARTING, text))
        else:
            print("Starting text set when stack is not empty")

    def addUserInputText(self, text: str) -> None:
        self.promptStack.addPrompt(
            PromptStack.Prompt(PromptStack.PromptType.INPUTED, text))
        self.__dealWithPromptTooLong()

    def generateText(self) -> None:
        prompt = self.promptStack.getSummorizedPromptText()
        prompt += self.__generatingPrompt + self.styleHintPrompt + self.__generateSuffix
        generatedText = self.__openaiAdapter.generateResponse(prompt)
        self.promptStack.addPrompt(
            PromptStack.Prompt(PromptStack.PromptType.GENERATED,
                               generatedText))
        self.__dealWithPromptTooLong()

    def dealWithPromptTooLong(self) -> None:
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
                PromptStack.Prompt(PromptStack.PromptType.SUMMORIZED, summary),
                self.promptsToKeepWhenSummarizing)
            if self.__debug:
                print("summarizing from: [" + prompt + "]")
                print("into: [" + summary + "]")

    def __parseDefaultConfig(self):
        # config
        self.wordCountThreshold = 300
        self.promptsToKeepWhenSummarizing = 4
        self.styleHintPrompt = ""
        self.summarizingSentenceCount = 4
        self.aiSettings = {
            "engine": "curie-instruct-test",
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
            "wordCountThreshold": self.wordCountThreshold,
            "promptsToKeepWhenSummarizing": self.promptsToKeepWhenSummarizing,
            "styleHintPrompt": self.styleHintPrompt,
            "summarizingSentenceCount": self.summarizingSentenceCount,
            "aiSettings": self.aiSettings,
        }
        with open(self.__configPath) as f:
            json.dump(output, f)
    
    def __loadFromConfig(self) -> bool:
        try:
            with open(self.__configPath) as f:
                data = json.load(f)
                self.wordCountThreshold = data["wordCountThreshold"]
                self.promptsToKeepWhenSummarizing = data["promptsToKeepWhenSummarizing"]
                self.styleHintPrompt = data["styleHintPrompt"]
                self.summarizingSentenceCount = data["summarizingSentenceCount"]
                self.aiSettings = data["aiSettings"]
                self.__parseAiSettings()
                return True
        except Exception as e:
            if self.__debug:
                print("Error loading config:", e)
            return False