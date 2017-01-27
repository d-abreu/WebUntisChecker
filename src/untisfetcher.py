import time
from selenium import webdriver
import datetime

fileName = 'page.txt'
screenshotFileName = 'file.png'

def fetch(url,username,password,seekAhead):
    #driver = webdriver.Firefox()
    driver = webdriver.PhantomJS() 
    driver.set_window_size(1120, 1120)
    driver.get(url)
    driver.find_element_by_id('loginWidget.idusername').send_keys(username)
    driver.find_element_by_id('loginWidget.idpassword').send_keys(password)
    driver.find_element_by_id('dijit_form_Button_0').click()
    driver.get(url+'#Timetable?type=2&formatId=1&id=14')
    time.sleep(15) #wait for js to load
    if(seekAhead or datetime.datetime.today().weekday() == 5 or datetime.datetime.today().weekday() == 6):
        driver.find_element_by_class_name('fa-caret-right').click()
        time.sleep(10)
    try:
        elements = driver.find_elements_by_class_name('nowMarker')
        script = """
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """
        for elem in elements:
            driver.execute_script(script, elem)
    except Exception as ex:
        print(ex)
    text = driver.page_source
    file = open(fileName, mode='wt', encoding='utf-8')
    file.write(text)
    file.close()
    driver.save_screenshot(screenshotFileName)
    driver.close()
    driver.quit()
    return text
