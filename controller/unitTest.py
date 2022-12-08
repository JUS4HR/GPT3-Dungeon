from .__PromptStack import PromptStack, Prompt, PromptType
from .__OpenaiAdapter import init, generateResponse


# Unit tests
def testAiAdapter():
    print("Unit Test, don,t run this in any other curcumstances!")
    init(debug=True)
    # list = __ai.Model.list()
    # for item in list["data"]:
    #     if "instruct" in item["id"]:
    #         print(item["id"])
    print(generateResponse("Explain the gravity wave to a 10 years old."))


def testPromptStack():
    print("Unit Test, don,t run this in any other curcumstances!")
    basePrompt = Prompt(PromptType.STARTING, "aaa.")
    promptList = PromptStack(debug=True)
    promptList.addPrompt(basePrompt)
    promptList.addPrompt(Prompt(PromptType.INPUTED, "bbbbb."))
    promptList.addPrompt(Prompt(PromptType.GENERATED, "cccc."))
    promptList.addPrompt(Prompt(PromptType.INPUTED, "eeee"))
    print(promptList.getFullPromptText())
    print(promptList.getSummorizedPromptText())
    print(promptList.getWordCount())
    print(promptList.getSummorizedPromptTextExcept(2))
    print("Doing summorization")
    promptList.summorizeActivePrompt(Prompt(PromptType.SUMMORIZED, "dddddd."), 1)
    print(promptList.getSummorizedPromptText())
    print(promptList.getWordCount())