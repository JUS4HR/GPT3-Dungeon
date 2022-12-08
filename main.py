import openai
# import argparse
import os

starting_prompt = "It's a rainy day. You're searching in some dark forest. You see a light in the distance."
stack = []
style_hint = "Use a detailed and descriptive style"

def init_openai():
    key = os.getenv("OPENAI_API_KEY")
    openai.api_key = key
    print("OpenAI API key set:" , key)
    
def parse_choice(raw_choice: str) -> str:
    if len(raw_choice) == 0:
        return ""
    all_quote_marks = ["”", "“", "\""]
    if raw_choice[0] in all_quote_marks and raw_choice[-1] in all_quote_marks:
        return "You say, " + raw_choice
    return "You " + raw_choice

def parse_response(response: str) -> str:
    # remove unfinished sentence at the end
    all_finish_tokens = [".", "!", "?"]
    response = response.strip()
    if len(response) > 0:
        while response[-1] not in all_finish_tokens:
            response = response[:-1]
    return response

def parse_prompt() -> str:
    prompt = "The story so far:\n["
    prompt += "\n".join(stack)
    prompt += "]\ncontinue writing the story. "
    prompt += style_hint
    prompt += "\n"
    return prompt

def debug_print(*args, **kwargs):
    print("DEBUG:")
    print(*args, **kwargs)
    input("END DEBUG, press enter to continue...")

def main():
    init_openai()

    engine = "davinci"
    temperature = 0.9
    max_tokens = 30
    top_p = 1
    frequency_penalty = 0
    presence_penalty = 0
    prompt = "This is a test"
    
    stack.append(starting_prompt.strip())

    # generate once to get the first response
    response = openai.Completion.create(
        engine=engine,
        prompt=parse_prompt(),
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )["choices"][0]["text"]
    stack.append(parse_response(response))
    for item in stack:
        print(item)

    while True:
        raw_choice = input("> ")
        # detect commands
        if len(raw_choice) > 0 and raw_choice[0] == "/":
            # parse command
            command_text = raw_choice[1:]
            if command_text == "quit" or command_text == "exit":
                break
            # todo: do things
        choice = parse_choice(raw_choice)
        print("\033[F\033[K", end="") # clear line
        print(choice)
        stack.append(choice.strip())
        prompt = parse_prompt()
        
        debug_print(prompt)
        
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )["choices"][0]["text"]
        stack.append(parse_response(response))
        print(stack[-1])

if __name__ == "__main__":
    main()
