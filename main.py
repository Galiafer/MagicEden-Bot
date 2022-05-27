import os
import json
import locale
from magiceden import MintBot


def getConfig():
    configFile = open("config.json", 'r', encoding='utf-8')
    return json.load(configFile)


def getTranslation():
    translationFile = open("translations.json", 'r', encoding='utf-8')
    return json.load(translationFile)


# get config
config = getConfig()
# get translations
translation = getTranslation()
# if Windows True, else False (mac, linux)
isWindows = True if os.name == 'nt' else False
# if language = 'ru' set translation to Russian, else English
language = 'ru' if locale.getdefaultlocale()[0] == "ru_RU" else 'en'

if "magiceden.io" in config['launchpadLink']:
    print(translation[language]['found'])
    bot = MintBot(config, translation, language, isWindows)

    bot.start()
else:
    print("Could not recognize link")
