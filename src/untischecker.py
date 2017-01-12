#!/usr/bin/python3

import os.path
import datetime
import untiscomparer as comparer
import untisfetcher as fetcher
import untisnotifier as notifier
import untisparser as parser
import simplejson as json

def execute():
    msg = 'Starting ' + str(datetime.datetime.now())
    print(msg)
    msg = 'Reading settings...'
    
    settingsFile = 'settings.txt'
    exists = os.path.isfile('settings.txt')
    if(not exists):
        settingsFile = 'settings.sample.txt'
    file = open('settings.txt', mode='rt', encoding='utf-8')
    jsonSettings = file.read()
    file.close()

    settings = json.loads(jsonSettings)

    text = fetcher.fetch(settings["UntisUrl"], settings["Username"], settings["Password"])
    print('Fetched')

    print('Reading file')
    file = open('page.txt', mode='rt', encoding='utf-8')
    text = file.read()
    file.close()
    print('Finished reading file')

    print('Generating hash')
    hashRes = parser.parse(text)
    print ('Hash: ' + hashRes)

    hasChanged = comparer.hasChanges(hashRes)
    if(hasChanged):
        print('Changes detected...notifiying!')
        for email in settings["EmailsToNotify"]:
            notifier.notify(settings["SmtpUsername"], email, settings["SmtpServer"], settings["SmtpPort"], settings["SmtpPassword"], settings["IsSmtpConnectionSafe"])
    else:
        print('No changes detected')

if __name__ == '__main__':
   execute()