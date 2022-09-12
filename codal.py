from ctypes import sizeof
from requests import delete
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from notifypy import Notify



options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = options)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver.get("https://www.codal.ir/")
elements = driver.find_elements(By.TAG_NAME, "tr")




def newsNotif():
    for elem in elements:
        trElem = elem.find_elements(By.TAG_NAME , "td")
        if len(trElem) != 0:
            if "افشای اطلاعات بااهمیت" in trElem[3].text:
                notification = Notify()
                notification.title = trElem[0].text + "(" + trElem[1].text + ")"
                notification.message = trElem[3].text
                notification.send()
            else:
                pass


def symNotif():
    for elem in elements:
        trElem = elem.find_elements(By.TAG_NAME , "td")
        if len(trElem) != 0:
            if "فروی" in trElem[0].text:
                notification = Notify()
                notification.title = trElem[0].text + "(" + trElem[1].text + ")"
                notification.message = trElem[3].text
                notification.send()
            else:
                pass


newsNotif()
symNotif()
