import openai as __ai
from os import getenv as __osGetenv

__initialized = False
__debug = False

__engine = "curie-instruct-beta"
__temperature = 0.75
__max_tokens = 50
__top_p = 0.95
__frequency_penalty = 1.0
__presence_penalty = 0


def isInitialized() -> bool:
    return __initialized


def init(debug: bool = False) -> None:
    global __debug
    __debug = debug
    if not __initialized:
        key = __osGetenv("OPENAI_API_KEY")
        __ai.api_key = key
        if __debug:
            print("OpenAI API key set:", key)
    elif __debug:
        print("OpenAI adapter already initialized.")


def setParams(
    engine: str = None,
    temperature: float = None,
    max_tokens: int = None,
    top_p: float = None,
    frequency_penalty: float = None,
    presence_penalty: float = None,
):
    if engine:
        __engine = engine
    if temperature:
        __temperature = temperature
    if max_tokens:
        __max_tokens = max_tokens
    if top_p:
        __top_p = top_p
    if frequency_penalty:
        __frequency_penalty = frequency_penalty
    if presence_penalty:
        __presence_penalty = presence_penalty


def generateResponse(promptText: str) -> str:
    response = __ai.Completion.create(
        engine=__engine,
        prompt=promptText,
        temperature=__temperature,
        max_tokens=__max_tokens,
        top_p=__top_p,
        frequency_penalty=__frequency_penalty,
        presence_penalty=__presence_penalty,
    )
    if __debug:
        print("response got:")
        print(response)
    return response["choices"][0]["text"]
