from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
from datetime import date, timedelta
import os
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#XPATH範例1:f"//div[@data-text-as-pseudo-element='新增人員']"
#div元素且屬性data-text-as-pseudo-element值為'新增人員'
#XPATH範例2://div[@aria-label and @role="button" and @tabindex=-1]
#div元素有aria-label屬性且屬性role為"button"且屬性tableindex為-1
def findElementsForever(myBy, myValue):
    elem = None
    while elem == None:
        try:
            elem = browser.find_elements(
                by=myBy, value=myValue)  # //標籤@屬性='值'
        except:
            print("找不到元素...XPATH={myValue}")
            sleep(1)
    return elem
def findElementForever(myBy, myValue):
    elem = None
    while elem == None:
        try:
            elem = browser.find_element(
                by=myBy, value=myValue)  # //標籤@屬性='值'
        except:
            print(f"找不到元素...XPATH={myValue}")
            sleep(1)
    return elem


# 先切換到當前目錄，才能正常讀取檔案
cwd_dir = os.path.dirname(sys.argv[0])
os.chdir(cwd_dir)
# 帳密2
account = input("輸入原帳號:")
password = input("輸入原密碼:")
new_account_nickname = input("新帳號暱稱:")
new_account_id = input("貼上新帳號liveID:")

# 要先安裝ChromeDriver才能使用
# https://chromedriver.chromium.org/downloads
s = Service('chromedriver.exe')
browser = webdriver.Chrome(service=s)
browser.set_window_size(200, 1000)
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

# 定位群组列表元素
group_list = browser.find_elements(By.CSS_SELECTOR, '[data-control-id="SidebarMenuLink"]')

xpath_msg = '//div[@aria-label and @role="button" and @tabindex=-1]'

# 尋找對話視窗
# Skype需要時間load有可能一開始元素不存在會跳錯
while True:
    # 等待元素加载完成并可见
    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath_msg)))

    msg_elements = findElementsForever(By.XPATH, xpath_msg)
    for one_msg in msg_elements:
        print(one_msg.accessible_name)
        #找出群組
        if '群組聊天' in one_msg.accessible_name:
            one_msg.click()
            sleep(1)
            #點擊添加人員
            add_btn = findElementForever(By.XPATH, f"//div[@data-text-as-pseudo-element='新增人員' or @data-text-as-pseudo-element='邀請其他人']")
            can_add = True
            try:
                add_btn.click()
            except:
                can_add = False
                print('無法交互')
            if can_add == True:
                #找出新增的帳號
                input = findElementForever(By.XPATH, f"//input[@aria-label='搜尋']")
                input.send_keys(new_account_nickname)
                sleep(1)
                #選擇第一個
                new_account_elem = findElementForever(By.XPATH, f"//div[@role='listitem']")
                new_account_elem.click()
                sleep(1)
                #選擇完成
                finish_btn = findElementForever(By.XPATH, f"//button[@aria-label='完成']")
                finish_btn.click()
                sleep(1)
                #輸入設定權限命令
                inputElem = findElementForever(By.XPATH, "//div[@role='textbox']")
                inputElem.clear()
                inputElem.send_keys(f'/setrole {new_account_nickname} Admin')
                sleep(1)
                #送出
                sendElem = findElementForever(By.XPATH, "//button[@aria-label='傳送訊息']")
                sendElem.click()
                sleep(1)
            #點擊管理群組
            edit = findElementForever(By.XPATH, "//button[@aria-label='管理群組設定']")
            edit.click()
            sleep(1)
            #點擊離開
            leave = findElementForever(By.XPATH, "//div[@aria-label='離開']")
            leave.click()
            sleep(1)
            #點擊確認
            leave = findElementForever(By.XPATH, "//button[@aria-label='確認']")
            leave.click()
            sleep(1)
            break
        elif new_account_nickname in one_msg.accessible_name or new_account_id in one_msg.accessible_name:
            print('新帳號不能刪除,略過')
            continue
        #找出個人
        elif '有其他可用的選項' in one_msg.accessible_name:
            print('點擊 訊息')
            one_msg.click()
            sleep(1)
            #點擊管理群組
            wait = WebDriverWait(browser, 10)
            edit = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='管理群組設定']")))
            print('點擊 管理群組設定')
            edit.click()
            sleep(1)
            #點擊封鎖聯絡人
            block = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='封鎖聯絡人']")))
            print('點擊 封鎖聯絡人')
            block.click()
            sleep(1)
            #點擊封鎖
            block2 = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='封鎖']")))
            print('點擊 封鎖')
            block2.click()
            sleep(3)
            break

sleep(10)

browser.quit()
