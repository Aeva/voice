

import common
from sh import espeak, echo


class Espeak(common.SpeechEngine):
    """
    Wraper for the Espeak speach engine.
    """
    def __init__(self):
        self.name = "espeak"

    def voices(self):
        # is there a way to generate this automatically and correctly?
        mods = ["+m%s"%i for i in range(1,8)]
        mods += ["+f%s"%i for i in range(1,8)] 
        mods += ["+croak", "+whisper"]
        voices = ["english-us"]
        found = []
        for voice in voices:
            for mod in mods:
                found.append(voice+mod)
        return found

    def say(self, message, voice=None, block=True):
        msg = common.sterilize(message)
        if voice and voice in self.voices():
            espeak(echo(msg), "-v", voice, _bg=not block)
        else:
            espeak(echo(msg), _bg=not block)

