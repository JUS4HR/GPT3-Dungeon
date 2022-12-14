from .__PromptStack import PromptStack, Prompt, PromptType
from .__OpenaiAdapter import OpenAIAdapter


# Unit tests
def testAiAdapter(prompt: str = None):
    print("Unit Test, don,t run this in any other curcumstances!")
    from os import getenv as __osGetenv
    key = __osGetenv("OPENAI_API_KEY")
    adapter = OpenAIAdapter(key, debug=True)
    adapter.setParams(
        engine="curie-instruct-beta",
        temperature=0.6,
        max_tokens=200,
        top_p=0.95,
        frequency_penalty=1.0,
        presence_penalty=0,
    )
    if not prompt:
        prompt = "Generate 4 sentences explaining how to make a sandwich."
    print(adapter.generateResponse(prompt))


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