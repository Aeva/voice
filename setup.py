from setuptools import setup

setup(name="voice",
      version="zero",
      description="",
      url="",
      author="Aeva Palecek",
      author_email="aeva.ntsc@gmail.com",
      license="GPLv3",
      packages=["voice"],
      zip_safe=False,

      entry_points = {
        "console_scripts" : [
            "say=voice.commands:say_command",
            "readtome=voice.commands:read_to_me",
            ],
        },

      install_requires = [
          "lxml",
          "sh",
          "requests",
        ])
      
