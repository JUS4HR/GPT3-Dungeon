from tempfile import NamedTemporaryFile as __tempNamedFile
from subprocess import call as __subCall
from os import environ as __osEnv

# static vars
__defaultEditor = "vim"


def editText(text: str, editor: str = None) -> str:
    if not editor:
        editor = __osEnv.get('EDITOR', __defaultEditor)

    with __tempNamedFile(suffix=".dungeonTmp") as temp:
        temp.write(text.encode())
        temp.flush()
        __subCall([editor, temp.name])

        temp.seek(0)
        result = temp.read().decode()

    return result

    