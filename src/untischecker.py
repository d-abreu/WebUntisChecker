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

    fetcher.fileName = 'page.txt'
    fetcher.screenshotFileName = 'file.png'
    currentWeek = fetcher.fetch(settings["UntisUrl"], settings["Username"], settings["Password"],False)
    print('Current week fetched')

    fetcher.fileName = 'page_next.txt'
    fetcher.screenshotFileName = 'file_next.png'
    nextWeek = fetcher.fetch(settings["UntisUrl"], settings["Username"], settings["Password"],True)
    print('Next week fetched')

    print('Generating hash')
    currentWeekHash = parser.parse(currentWeek)
    nextWeekHash = parser.parse(nextWeek)
    print ('Current week hash: ' + currentWeekHash)
    print ('Next week hash: ' + nextWeekHash)

    comparer.src = 'hash.txt'
    hasChanged = comparer.hasChanges(currentWeekHash)
    if(hasChanged):
        print('Changes detected...notifiying!')
        notifier.src = 'file.png'
        for email in settings["EmailsToNotify"]:
            notifier.notify('Current week',settings["SmtpUsername"], email, settings["SmtpServer"], settings["SmtpPort"], settings["SmtpPassword"], settings["IsSmtpConnectionSafe"])
    else:
        print('No changes detected')

    
    comparer.src = 'next_hash.txt'
    hasChanged = comparer.hasChanges(currentWeekHash)
    if(hasChanged):
        print('Changes detected...notifiying!')
        notifier.src = 'file_next.png'
        for email in settings["EmailsToNotify"]:
            notifier.notify('Next week',settings["SmtpUsername"], email, settings["SmtpServer"], settings["SmtpPort"], settings["SmtpPassword"], settings["IsSmtpConnectionSafe"])
    else:
        print('No changes detected')


if __name__ == '__main__':
   execute()