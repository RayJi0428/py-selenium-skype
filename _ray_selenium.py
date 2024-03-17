from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
from datetime import date, timedelta
import os
import sys

browser = None
sk_account = os.environ['SK_ACCOUNT']
sk_pwd = os.environ['SK_PWD']


# 尋找物件
def findElementForever(myBy, myValue):
    elem = None
    while elem == None:
        try:
            elem = browser.find_element(
                by=myBy, value=myValue)  # //標籤@屬性='值'
            if elem.is_displayed() == False:
                raise Exception('尚未displayed')
        except Exception as arg:
            print(f"找不到元素...{myValue}")
            sleep(1)
    return elem


# 建立瀏覽器
def createBrowser():
    global browser
    s = Service('chromedriver.exe')
    browser = webdriver.Chrome(service=s)
    browser.set_window_size(200, 1000)
    browser.get('https://web.skype.com/')
    return browser


# 登入
def login():
    # 確認帳號
    loginElem = findElementForever(By.NAME, 'loginfmt')
    loginElem.send_keys(sk_account)
    nextElem = findElementForever(By.ID, 'idSIButton9')
    nextElem.click()
    sleep(1)

    # 確認密碼
    pwdElem = findElementForever(By.NAME, 'passwd')
    pwdElem.send_keys(sk_pwd)
    nextElem = findElementForever(By.ID, 'idSIButton9')
    nextElem.click()
    sleep(1)

    # 確認記憶帳號
    nextElem = findElementForever(By.ID, 'acceptButton')
    nextElem.click()
    sleep(1)
