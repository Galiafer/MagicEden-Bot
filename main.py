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


config = getConfig()
translation = getTranslation()
language = 'ru' if locale.getdefaultlocale()[0] == "ru_RU" else 'en'

if "magiceden.io" in config['launchpadLink']:
    print(translation[language]['found'])
    bot = MintBot(config, translation, language)

    bot.start()
else:
    print("Please paste correct url")
