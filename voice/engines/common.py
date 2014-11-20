
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
