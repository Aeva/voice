

import common
from sh import festival, echo


class Festival(common.SpeechEngine):
    """
    Wraper for the Festival speach engine.
    """
    def __init__(self):
        self.name = "festival"
        self._voices = []
        voice_list = self._get_list("(voice.list)")
        priority_list = self._get_list("default-voice-priority-list")
        for voice in priority_list:
            if voice in voice_list:
                self._voices.append(voice)
        for voice in voice_list:
            if voice not in self._voices:
                self._voices.append(voice)
        self._voices = priority_list

        # set the default voice
        self.default_voice = self._voices[0]
        nice_defaults = [
            #"nitech_us_clb_arctic_hts",
            ]
        for voice in nice_defaults:
            if voice in self._voices:
                self.default_voice = voice
                break
            
    def _get_list(self, atom):
        output = festival(echo("(print {0})".format(atom)), _bg=False)
        return output.stdout.strip()[1:-1].split(" ")

    def voices(self):
        return self._voices
        
    def say(self, message, voice=None, block=True):
        if not voice:
            voice = self.default_voice

        voice_part = '(voice_{0})'.format(voice)
        text_part = '(SayText "{0}")'.format(common.sterilize(message))
        command = voice_part + text_part
        festival(echo(command), _bg=not block)

