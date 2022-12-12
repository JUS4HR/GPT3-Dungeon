import re as __re

__firstToSecondMappings = [
    ("I'm", "you're"),
    ("Im", "you're"),
    ("Ive", "you've"),
    ("I am", "you are"),
    ("was I", "were you"),
    ("am I", "are you"),
    ("wasn't I", "weren't you"),
    ("I", "you"),
    ("I'd", "you'd"),
    ("i", "you"),
    ("I've", "you've"),
    ("was I", "were you"),
    ("am I", "are you"),
    ("wasn't I", "weren't you"),
    ("I", "you"),
    ("I'd", "you'd"),
    ("i", "you"),
    ("I've", "you've"),
    ("I was", "you were"),
    ("my", "your"),
    ("we", "you"),
    ("we're", "you're"),
    ("mine", "yours"),
    ("me", "you"),
    ("us", "you"),
    ("our", "your"),
    ("I'll", "you'll"),
    ("myself", "yourself"),
]


def __capitalize(word):
    return word[0].upper() + word[1:]


def __mappingVariationPairs(mapping):
    mapping_list = []
    mapping_list.append((" " + mapping[0] + " ", " " + mapping[1] + " "))
    mapping_list.append((" " + __capitalize(mapping[0]) + " ",
                         " " + __capitalize(mapping[1]) + " "))

    # Change you it's before a punctuation
    if mapping[0] == "you":
        mapping = ("you", "me")
    mapping_list.append((" " + mapping[0] + ",", " " + mapping[1] + ","))
    mapping_list.append((" " + mapping[0] + "\?", " " + mapping[1] + "\?"))
    mapping_list.append((" " + mapping[0] + "\!", " " + mapping[1] + "\!"))
    mapping_list.append((" " + mapping[0] + "\.", " " + mapping[1] + "."))

    return mapping_list


def __replaceOutsideQuotes(text, current_word, repl_word):
    text = standardizePunctuation(text)

    reg_expr = __re.compile(current_word + '(?=([^"]*"[^"]*")*[^"]*$)')

    output = reg_expr.sub(repl_word, text)
    return output


def __capitalizeHelper(string):
    string_list = list(string)
    string_list[0] = string_list[0].upper()
    return "".join(string_list)


def __capitalizeFirstLetters(text):
    first_letters_regex = __re.compile(r"((?<=[\.\?!]\s)(\w+)|(^\w+))")

    def cap(match):
        return __capitalizeHelper(match.group())

    result = first_letters_regex.sub(cap, text)
    return result

def firstToSecondPerson(text):
    text = " " + text
    text = standardizePunctuation(text)
    for pair in __firstToSecondMappings:
        variations = __mappingVariationPairs(pair)
        for variation in variations:
            text = __replaceOutsideQuotes(text, variation[0], variation[1])

    return __capitalizeFirstLetters(text[1:])


def standardizePunctuation(text):
    text = text.replace("’", "'")
    text = text.replace("`", "'")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    return text