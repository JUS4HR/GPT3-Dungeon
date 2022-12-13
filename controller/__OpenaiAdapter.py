from importlib import import_module
from threading import Thread


class OpenAIAdapter:

    def __init__(self, key: str, debug: bool = False) -> None:
        self.__debug = False

        self.__engine = "curie-instruct-beta"
        self.__temperature = 0.75
        self.__max_tokens = 50
        self.__top_p = 0.95
        self.__frequency_penalty = 1.0
        self.__presence_penalty = 0
        self.__debug = debug
        # self.__key = __osGetenv("OPENAI_API_KEY")
        self.__key = key
        self.__lastOutput = ""
        if self.__debug:
            print("OpenAI API key set:", key)

    def setParams(
        self,
        engine: str = None,
        temperature: float = None,
        max_tokens: int = None,
        top_p: float = None,
        frequency_penalty: float = None,
        presence_penalty: int = None,
    ):
        if engine:
            self.__engine = engine
        if temperature:
            self.__temperature = temperature
        if max_tokens:
            self.__max_tokens = max_tokens
        if top_p:
            self.__top_p = top_p
        if frequency_penalty:
            self.__frequency_penalty = frequency_penalty
        if presence_penalty:
            self.__presence_penalty = presence_penalty

    def __generationThread(self, promptText: str) -> None:
        ai = import_module("openai")
        ai.api_key = self.__key
        response = ai.Completion.create(
            prompt=promptText,
            engine=self.__engine,
            temperature=self.__temperature,
            max_tokens=self.__max_tokens,
            top_p=self.__top_p,
            frequency_penalty=self.__frequency_penalty,
            presence_penalty=self.__presence_penalty,
        )
        if self.__debug:
            print("response got:")
            print(response)
        self.__lastOutput = response["choices"][0]["text"]

    def generateResponse(self, promptText: str) -> str:
        thread = Thread(target=self.__generationThread, args=(promptText, ))
        thread.start()
        thread.join()
        result = self.__lastOutput
        self.__lastOutput = ""
        return result
