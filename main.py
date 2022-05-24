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
msg = "(sun) [記得寫週報{p_date}]({p_url}) (sun)".format(
    p_date=today.strftime("%m%d"), p_url=url)
# 要先安裝ChromeDriver才能使用
# https://chromedriver.chromium.org/downloads
browser = webdriver.Chrome('chromedriver_101.exe')
browser.set_window_size(200, 500)
browser.get('https://web.skype.com/')

# 確認帳號
loginElem = browser.find_element_by_name('loginfmt')
loginElem.send_keys(accout)
nextElem = browser.find_element_by_id('idSIButton9')
nextElem.click()
sleep(1)

# 確認密碼
pwdElem = browser.find_element_by_name('passwd')
pwdElem.send_keys(password)
nextElem = browser.find_element_by_id('idSIButton9')
nextElem.click()
sleep(1)

# 確認記憶帳號
nextElem = browser.find_element_by_id('idSIButton9')
nextElem.click()

# 尋找對話視窗
# Skype需要時間load有可能一開始元素不存在會跳錯
# 因為頁面可視範圍有限,把目標對話視窗放到"我的最愛"比較容易找到
groupElem = None
while groupElem == None:
    try:
        groupElem = browser.find_element_by_xpath(
            "//div[@data-text-as-pseudo-element='幹話討論']")  # //標籤@屬性='值'
    except:
        print("找不到元素...")
        sleep(1)
# https://blog.csdn.net/WanYu_Lss/article/details/84137519
# 有些想要點擊的元素藏在第二層, 改用網路找到的其他方法處理
browser.execute_script("arguments[0].click();", groupElem)
# groupElem.click()
sleep(1)

# 輸入訊息
inputElem = browser.find_element_by_xpath(
    "//div[@role='textbox']")  # //標籤@屬性='值'
inputElem.send_keys(msg)  # 發送訊息
sendElem = browser.find_element_by_xpath(
    "//button[@aria-label='Send message']")  # //標籤@屬性='值'
sendElem.click()
sleep(1)

# 關閉程式
browser.quit()
