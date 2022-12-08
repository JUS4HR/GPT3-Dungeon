from . import __OpenaiAdapter, __PromptStack, __utils

# recommended workflow:
# | starting prompt
# | get response once according to starting prompt
# | user input (@ normal input / @ command)                              Loop back here <-------+
# | (if command, do as asked)                                                                   |
# | generate new response according to history                                                  |
# | if total word count too much, summorize all(or all but the last ones) into shorter version  |
# +---------------------------------------------------------------------------------------------+

# vars
debug = False
wordCountThreshold = 300
promptsToKeepWhenSummarizing = 4

promptStack = __PromptStack.PromptStack(debug)

generatingPrompt = "\nContinue the story above. "
styleHintPrompt = ""
generateSuffix = "\nContinues: "

summarizingSentenceCount = 4
summarizingPrompt = "\nSummarize the story above into " + str(
    summarizingSentenceCount) + " sentences."
summarizeSuffix = "\nResult: "

aiSettings = {
    "engine": "davinci-instruct-test",
    "temperature": 0.6,
    "max_tokens": 200,
    "max_tokens_summary": 500,
    "top_p": 0.95,
    "frequency_penalty": 1.0,
    "presence_penalty": 0,
}


# functions
def parseAiSettings():
    __OpenaiAdapter.setParams(
        engine=aiSettings["engine"],
        temperature=aiSettings["temperature"],
        max_tokens=aiSettings["max_tokens"],
        top_p=aiSettings["top_p"],
        frequency_penalty=aiSettings["frequency_penalty"],
        presence_penalty=aiSettings["presence_penalty"],
    )


def setStartingText(text: str):
    if len(promptStack.getFullPrompt()) == 0:
        promptStack.addPrompt(
            __PromptStack.Prompt(__PromptStack.PromptType.STARTING, text))
    else:
        print("Starting text set when stack is not empty")


def addUserInputText(text: str):
    promptStack.addPrompt(
        __PromptStack.Prompt(__PromptStack.PromptType.INPUTED, text))
    __dealWithPromptTooLong()


def generateText():
    prompt = promptStack.getSummorizedPromptText()
    prompt += generatingPrompt + styleHintPrompt + generateSuffix
    generatedText = __OpenaiAdapter.generateResponse(prompt)
    promptStack.addPrompt(
        __PromptStack.Prompt(__PromptStack.PromptType.GENERATED,
                             generatedText))
    __dealWithPromptTooLong()


def __dealWithPromptTooLong():
    if debug:
        print("Word count now:", promptStack.getWordCount())
    if promptStack.getWordCount() > wordCountThreshold:
        prompt = promptStack.getSummorizedPromptTextExcept(
            promptsToKeepWhenSummarizing)
        prompt += summarizingPrompt + summarizeSuffix
        __OpenaiAdapter.setParams(max_tokens=aiSettings["max_tokens_summary"])
        summary = __OpenaiAdapter.generateResponse(prompt)
        __OpenaiAdapter.setParams(max_tokens=aiSettings["max_tokens"])
        promptStack.summorizeActivePrompt(
            __PromptStack.Prompt(__PromptStack.PromptType.SUMMORIZED, summary),
            promptsToKeepWhenSummarizing)
        if debug:
            print("summarizing from: [" + prompt + "]")
            print("into: [" + summary + "]")
