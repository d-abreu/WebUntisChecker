import time
from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
import datetime

class UntisFetcher():

    def __init__(self):
        self.fileName = 'page.txt'
        self.screenshotFileName = 'file.png'
        self.lastUpdate = ''
        self.driver = webdriver.PhantomJS()
        #self.driver = webdriver.Firefox() 
        self.loggedIn = False    

    def loadSettings(self, settings):
        self.url = settings["UntisUrl"]
        self.username = settings["Username"]
        self.password = settings["Password"]

    def open(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 1120)
        self.driver.implicitly_wait(15)

    def close(self):
        self.driver.close()
        self.driver.quit()

    def fetchCurrentWeek(self):
        return self.__fetch(False)

    def fetchNextWeek(self):
        return self.__fetch(True)

    def __fetch(self,isNextWeek):
        if not self.loggedIn:
            self.__logIn()
        self.__getPlanPage()
        if(isNextWeek or datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6):
            self.__moveToNextWeek()
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

    def __getPlanPage(self):
        count = 0
        self.driver.get(self.url+'#Timetable?type=2&formatId=1&id=14')
        while True:
            try:
                if count == 10:
                    break
                self.lastUpdate = self.driver.find_element_by_class_name('grupetWidgetTimetableUpdateTimestamp').text
                break
            except:
                count = count+1

    def __logIn(self):
        self.driver.get(self.url)
        count = 0
        while True:
            try:
                if count == 10:
                    break
                self.driver.find_element_by_id('loginWidget.idusername').send_keys(self.username)
                self.driver.find_element_by_id('loginWidget.idpassword').send_keys(self.password)
                self.driver.find_element_by_id('dijit_form_Button_0').click()
                self.loggedIn = True
                break
            except:
                count = count+1
        

    def __moveToNextWeek(self):
        count = 0
        while True:
            try:
                if count == 10:
                    break
                self.driver.find_element_by_class_name('fa-caret-right').click()
                break
            except:
                count = count+1
