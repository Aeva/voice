

import sys
import argparse

import requests
import lxml.html

import voice


def get_input():
    """
    Returns the input to the command, be it from sys.argv or piped.
    """
    message = None
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = raw_input()
    return message


def say_command():
    """
    This is a wrapper for voice.say to enable a 'say' shell command.
    """
    message = get_input()
    if message:
        voice.say(message)


def read_to_me():
    """
    Implements the "readtome" shell command.  Given a url and maybe
    something like an xpath query or just a dom id, the command will
    download the page and then read the contents.
    """

    bio = """
    Readtome is a tool for downloading a webpage and piping its textual
    content to a text-to-speech engine."""

    parser = argparse.ArgumentParser(description=bio)
    parser.add_argument(
        "url", metavar="url", type=str, nargs='?',
        help="Url to be read aloud.")
    parser.add_argument(
        '--id', metavar="dom_id", type=str, nargs=1, default="",
        help="Dom id to be used as the root element for reading from.")
    parser.add_argument(
        '--xpath', metavar="xpath", type=str, nargs=1, default="",
        help="Xpath query for the root element to read from.")
    parser.add_argument(
        '--engine', metavar="engine", type=str, nargs=1, default="any",
        help="Override the default speech engine.")
    parser.add_argument(
        '--voice', metavar="voice", type=str, nargs=1, default="any",
        help="Override the default voice for the speech engine.")
    parser.add_argument(
        '--list-engines', default=False, action="store_true",
        help="List available speech engines.")
    parser.add_argument(
        '--list-voices', default=False, action="store_true",
        help="List available voices for the given or default engine.")

    def clean_arg(arg, anyable=False):
        """
        Extract a string value from an arg.  I'm probably using the lib
        wrong, but it seems like the arg can be anything from a
        string, a list with a single string in it, or None.
        """
        found = ""
        if arg:
            if type(arg) == list:
                found = arg[0]
            else:
                found = arg
            if anyable:
                if found == "any":
                    found = None
        return found

    # parse args
    args = parser.parse_args()

    # string args
    url = clean_arg(args.url)
    dom_id = clean_arg(args.id)
    xpath = clean_arg(args.xpath)
    use_engine = clean_arg(args.engine, True)
    use_voice = clean_arg(args.voice, True)

    # bool args
    list_engines = args.list_engines
    list_voices = args.list_voices

    if use_engine == "any":
        use_engine = None
    if use_voice == "any":
        use_voice = None

    if list_engines:
        print "These are the available text-to-speech engines:"
        for engine in voice.ENGINES:
            print " - " + engine.name
        exit()

    if list_voices:
        print "These are the available voices for the current engine:"
        for voice_name in voice.get_voices(engine=use_engine):
            print " - " + voice_name
        exit()

    if not url:
        print "You must provide a url."
        exit()
        
    print "Downloading {0} ...".format(url)
    req = requests.get(url)
    if not req.status_code == requests.codes.ok:
        import httplib
        status_text = httplib.responses[req.status_code]
        print "Error {0}: {1}".format(req.status_code, status_text)
        exit()

    print "Parsing text from webpage..."
    dom = lxml.html.fromstring(req.text)
    read = ""

    if dom_id:
        query = "//*[@id='{0}']".format(dom_id)
        found = dom.xpath(query)
        if found:
            read = found[0].text_content().strip()
    elif xpath:
        found = dom.xpath(xpath)
        if found:
            read = found[0].text_content().strip()
    else:
        body = dom.find("body")
        read = body.text_content().strip()
    if read:
        print "Sending message to text-to-speech engine!"
        voice.say(read, use_voice, use_engine)
    else:
        print "Nothing to say :("
