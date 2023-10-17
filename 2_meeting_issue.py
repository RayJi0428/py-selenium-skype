from selenium.webdriver.common.by import By
from time import sleep
from datetime import date, timedelta
import os
import sys
import _ray_selenium


# 先切換到當前目錄，才能正常讀取檔案
cwd_dir = os.path.dirname(sys.argv[0])
os.chdir(cwd_dir)

url = 'https://docs.google.com/spreadsheets/d/1zvqC3UeDDrfO-g52PGG-MxbTwK9KwDQ6xDhkI6XkB0o/edit#gid=828109937'
meet_date = date.today() + timedelta(days=1)
msg = f'[{meet_date.strftime("%m/%d")}週會議題請填]({url})'
target = "幹話討論"

browser = _ray_selenium.createBrowser()
_ray_selenium.login()

# 尋找對話視窗
# Skype需要時間load有可能一開始元素不存在會跳錯
# 因為頁面可視範圍有限,把目標對話視窗放到"我的最愛"比較容易找到
groupElem = _ray_selenium.findElementForever(
    By.XPATH, "//div[@data-text-as-pseudo-element='{target}']".format(target=target))  # //標籤@屬性='值'

# https://blog.csdn.net/WanYu_Lss/article/details/84137519
# 有些想要點擊的元素藏在第二層, 改用網路找到的其他方法處理
browser.execute_script("arguments[0].click();", groupElem)
# groupElem.click()
sleep(1)

# 輸入訊息
inputElem = _ray_selenium.findElementForever(
    By.XPATH, "//div[@role='textbox']")  # //標籤@屬性='值'
inputElem.send_keys(msg)  # 發送訊息
sendElem = _ray_selenium.findElementForever(
    By.XPATH, "//button[@aria-label='傳送訊息']")  # //標籤@屬性='值'
sendElem.click()
sleep(3)

# 關閉程式
browser.quit()
