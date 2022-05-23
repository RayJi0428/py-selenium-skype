from selenium import webdriver
from time import sleep
from datetime import date
import os
import sys

# 先切換到當前目錄，才能正常讀取檔案
cwd_dir = os.path.dirname(sys.argv[0])
os.chdir(cwd_dir)

# 帳密
accout = os.environ['SK_ACCOUNT']
password = os.environ['SK_PWD']
url = os.environ['SK_URL']

# 定義發送訊息
today = date.today()
msg = "{p_url}\n跨部門新增{p_date}".format(
    p_date=today.strftime("%m%d"), p_url=url)
# 要先安裝ChromeDriver才能使用
# https://chromedriver.chromium.org/downloads
browser = webdriver.Chrome('chromedriver_101.exe')
browser.set_window_size(200, 500)
browser.get('https://web.skype.com/')
loginElem = browser.find_element_by_name('loginfmt')
loginElem.send_keys(accout)
nextElem = browser.find_element_by_id('idSIButton9')  # 確認帳號
nextElem.click()
sleep(1)
pwdElem = browser.find_element_by_name('passwd')
pwdElem.send_keys(password)
nextElem = browser.find_element_by_id('idSIButton9')  # 確認密碼
nextElem.click()
sleep(1)
nextElem = browser.find_element_by_id('idSIButton9')  # 確認記憶帳號
nextElem.click()
# pwdElem.submit()
sleep(5)  # 需要讀取時間
groupElem = browser.find_element_by_xpath(
    "//div[@data-text-as-pseudo-element='我']")  # //標籤@屬性='值'
# https://blog.csdn.net/WanYu_Lss/article/details/84137519
browser.execute_script("arguments[0].click();", groupElem)
# groupElem.click()
sleep(1)
inputElem = browser.find_element_by_xpath(
    "//div[@role='textbox']")  # //標籤@屬性='值'
inputElem.send_keys(msg)  # 發送訊息
sendElem = browser.find_element_by_xpath(
    "//button[@aria-label='Send message']")  # //標籤@屬性='值'
sendElem.click()

sleep(1)
browser.quit()  # 關閉
