

class SpeechEngine:
    """
    Speach engine base class.
    """
    def __init__(self):
        self.name == "unknown"

    def voices(self):
        return []

    def say(self, message, voice=None, block=True):
        pass


def sterilize(message):
    """
    Attempt to strip a message down to just plaintext.
    """
    sterilize = ""
    ok_chars = [":", ";", ",", "."]
    whitespace = [" ", "/t", "/n", "/r"]
    for char in message:
        # cache the char if it is an alphabetical character in the
        # 'ok_chars' list:
        if 97 <= ord(char.lower()) <= 122 or char in ok_chars:
            sterilize += char
        if char == "&":
            sterilize += " and "
        if char in whitespace and not sterilize.endswith(" "):
            sterilize += " "
    return sterilize
