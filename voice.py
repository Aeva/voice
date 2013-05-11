#!/usr/bin/env python

from glob import glob
from os.path import join, split
from sh import festival, espeak, echo


class SpeechEngine:
    def voices(self):
        return []
    def say(self, message, voice=None, block=True):
        pass


class Festival(SpeechEngine):
    def voices(self):
        found = [split(lang)[-1] for lang in 
                 glob("/usr/share/festival/voices/*/*")]
        found.sort()
        return found
        
    def say(self, message, voice=None, block=True):
        text = '(SayText "{0}")'.format(message.replace('"', ''))
        if voice and voice in self.voices():
            text = "(voice_{0})".format(voice) + text
        festival(echo(text), _bg=not block)


class Espeak(SpeechEngine):
    def voices(self):
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
        if voice and voice in self.voices():
            espeak(echo(message), "-v", voice, _bg=not block)
        else:
            espeak(echo(message), _bg=not block)


def voice_builder(engine=Festival, voice=None, blocking=True):
    eng = engine()
    def say(message):
        eng.say(message, voice, blocking)
    return say
