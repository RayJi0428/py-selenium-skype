from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
from datetime import date
import os
import sys


def findElementForever(myBy, myValue):
    elem = None
    while elem == None:
        try:
            elem = browser.find_element(
                by=myBy, value=myValue)  # //標籤@屬性='值'
        except:
            print("找不到元素...")
            sleep(1)
    return elem


# 先切換到當前目錄，才能正常讀取檔案
cwd_dir = os.path.dirname(sys.argv[0])
os.chdir(cwd_dir)

params = []
if len(sys.argv) > 1:
    params = sys.argv[1].split(',')
else:
    params[0] = input("輸入帳號:")
    params[1] = input("輸入密碼:")
    params[2] = input("輸入發送對象:")
    params[3] = input("輸入訊息:")

# 帳密
account = params[0]
password = params[1]
target = params[2]
msg = params[3]

url = os.environ['SK_URL']
# 定義發送訊息
today = date.today()
msg = "{p_url}\n工作週報{p_date}".format(
    p_date=today.strftime("%m%d"), p_url=url)

# 要先安裝ChromeDriver才能使用
# https://chromedriver.chromium.org/downloads
s = Service('chromedriver_101.exe')
browser = webdriver.Chrome(service=s)
browser.set_window_size(200, 500)
browser.get('https://web.skype.com/')

# 確認帳號
loginElem = findElementForever(By.NAME, 'loginfmt')
loginElem.send_keys(account)
nextElem = findElementForever(By.ID, 'idSIButton9')
nextElem.click()
sleep(1)

# 確認密碼
pwdElem = findElementForever(By.NAME, 'passwd')
pwdElem.send_keys(password)
nextElem = findElementForever(By.ID, 'idSIButton9')
nextElem.click()
sleep(1)

# 確認記憶帳號
nextElem = findElementForever(By.ID, 'idSIButton9')
nextElem.click()
sleep(1)

# 尋找對話視窗
# Skype需要時間load有可能一開始元素不存在會跳錯
# 因為頁面可視範圍有限,把目標對話視窗放到"我的最愛"比較容易找到
groupElem = findElementForever(
    By.XPATH, "//div[@data-text-as-pseudo-element='{target}']".format(target=target))  # //標籤@屬性='值'

# https://blog.csdn.net/WanYu_Lss/article/details/84137519
# 有些想要點擊的元素藏在第二層, 改用網路找到的其他方法處理
browser.execute_script("arguments[0].click();", groupElem)
# groupElem.click()
sleep(1)

# 輸入訊息
inputElem = findElementForever(
    By.XPATH, "//div[@role='textbox']")  # //標籤@屬性='值'
inputElem.send_keys(msg)  # 發送訊息
sendElem = findElementForever(
    By.XPATH, "//button[@aria-label='傳送訊息']")  # //標籤@屬性='值'
sendElem.click()
sleep(3)

# 關閉程式
browser.quit()
