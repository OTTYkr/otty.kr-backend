
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://finance.yahoo.com/")
driver.get("https://query2.finance.yahoo.com/v1/test/getcrumb")