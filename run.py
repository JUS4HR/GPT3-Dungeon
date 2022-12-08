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
    generator.addUserInputText(input("> "))
    generator.generateText()
    print(generator.promptStack.getFullPrompt()[-1].getText())