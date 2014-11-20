
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

ENGINES = []
__festival_installed = False
__espeak_installed = False

# check to see if external commands needed are available
try:
    from sh import festival
    __festival_installed = True
    del festival
except ImportError:
    pass
try:
    from sh import espeak
    __espeak_installed = True
    del espeak
except ImportError:
    pass


# build the list of available speech engines
if __festival_installed:
    import engines.festival
    ENGINES.append(engines.festival.Festival())
if __espeak_installed:
    import engines.espeak
    ENGINES.append(engines.espeak.Espeak())
if not ENGINES:
    raise RuntimeError(
        "Neither festival or espeak seems to be installed.")


def get_speech_engine(name=None):
    """
    Returns a speech engine if one is installed.  If no name is given
    (or there is no engine by that name), then the 'best' engine
    installed will be returned.
    """
    global ENGINES
    if name:
        for engine in ENGINES:
            if engine.name == name:
                return engine
    return ENGINES[0]


def get_voices(engine=None):
    """
    Return a list of available voices for a given engine.  If no engine
    is provided, then it will give a list of voices for the best
    engine available.
    """
    engine = get_speech_engine(engine)
    return engine.voices()


def say(message, voice=None, engine=None, blocking=True):
    """
    Say something.
    """
    engine = get_speech_engine(engine)
    engine.say(message, voice, blocking)
