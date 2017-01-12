# WebUntisChecker
Checks for updates of the time table in the WebUntis platform. Very basic implementation, first project with python.

# Dependencies
python3

selenium

smtplib

html.parser

simplejson

phantomJS

geckodriver (optional, for firefox)

# Usage
Adjust settings.sample.txt accordingly.

Run python3 untischecker.py

# Selenium Webdriver
PhantomJS webdriver is used by default. To changed the browser replace "driver = webdriver.PhantomJS()" with another driver in untisfetcher.py 
