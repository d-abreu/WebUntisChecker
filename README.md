# UntisChecker
Checks for updates of the time table in the WebUntis platform. Very basic implementation, first project with python.

# Dependencies
selenium
smtplib
html.parser
simplejson
phantomJS (optional)

# Usage
Adjust settings.sample.txt accordingly.

Run python3 untischecker.py

# Webdriver
Firefox webdriver is used by default. Also works with PhantomJS. Replace driver = webdriver.Firefox() with driver = webdriver.PhantomJS() in untisfetcher.py 
