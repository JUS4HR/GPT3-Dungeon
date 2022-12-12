from controller import generator

startingPrompt = "It's a rainy day. You're searching in some dark forest. You see a light in the distance."

generator.debug = True
generator.parseAiSettings()
generator.setStartingText(startingPrompt)
generator.styleHintPrompt = "Describe the surroundings and character's behavior in detail. Do not mention what \"You\" have done."
generator.generateText()

for prompt in generator.promptStack.getFullPrompt():
    print(prompt.getText())

while True:
    userInput = input("> ")
    if len(userInput) > 0 and userInput[0] == "/":
        command = userInput[1:]
        if command == "retry" or command == "r":
            if generator.promptStack.removeBack() == -1:
                print("Regenerate last one")
                generator.generateText()
                print(generator.promptStack.getFullPrompt()[-1].getText())
            else:
                print("Error: cannot retry.")


    else:
        generator.addUserInputText(userInput)
        generator.generateText()
        print(generator.promptStack.getFullPrompt()[-1].getText())