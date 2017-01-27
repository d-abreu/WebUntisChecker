import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

class UntisFetcher():

    def __init__(self):
        self.fileName = 'page.txt'
        self.screenshotFileName = 'file.png'
        self.lastUpdate = ''
        self.driver = webdriver.PhantomJS()
        #self.driver = webdriver.Firefox() 
        self.loggedIn = False

    def on(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 1120)

    def off(self):
        self.driver.close()
        self.driver.quit()

    def fetch(self,url,username,password,seekAhead):
        if not self.loggedIn:
            self.logIn(url, username, password)
        self.getPage(url, username, password)
        self.lastUpdate = self.driver.find_element_by_class_name('grupetWidgetTimetableUpdateTimestamp').text
        if(seekAhead or datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6):
            self.moveToNextWeek()
        try:
            elements = self.driver.find_elements_by_class_name('nowMarker')
            script = """
                var element = arguments[0];
                element.parentNode.removeChild(element);
                """
            for elem in elements:
                self.driver.execute_script(script, elem)
        except Exception as ex:
            print(ex)
        text = self.driver.page_source
        file = open(self.fileName, mode='wt', encoding='utf-8')
        file.write(text)
        file.close()
        self.driver.save_screenshot(self.screenshotFileName)
        return text

    def getPage(self, url, username, password):
        count = 0
        while True:
            try:
                if count == 10:
                    break
                self.driver.get(url+'#Timetable?type=2&formatId=1&id=14')
                WebDriverWait(self.driver, 2)
                self.driver.find_element_by_id('dijit_layout_BorderContainer_0')
                break
            except:
                count = count+1

    def logIn(self, url, username, password):
        self.driver.get(url)
        count = 0
        while True:
            try:
                if count == 10:
                    break
                self.driver.get(url)
                WebDriverWait(self.driver, 2)
                self.driver.find_element_by_id('loginWidget.idusername')
                break
            except:
                count = count+1
        self.driver.find_element_by_id('loginWidget.idusername').send_keys(username)
        self.driver.find_element_by_id('loginWidget.idpassword').send_keys(password)
        self.driver.find_element_by_id('dijit_form_Button_0').click()
        self.loggedIn = True

    def moveToNextWeek(self):
        count = 0
        while True:
            try:
                if count == 10:
                    break
                WebDriverWait(self.driver, 2)
                self.driver.find_element_by_class_name('fa-caret-right').click()
                break
            except:
                count = count+1
