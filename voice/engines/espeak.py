
# This file is part of Voice
#
# Voice is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Voice is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Waterworks.  If not, see <http://www.gnu.org/licenses/>.

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

