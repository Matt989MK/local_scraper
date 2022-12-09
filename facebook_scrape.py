from time import time, sleep
from ssl import DER_cert_to_PEM_cert
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib2to3.pgen2 import  driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
options = Options()
options.add_argument("--user-data-dir=C:\\Users\\moffi\\AppData\\Local\\Google\\Chrome\\User Data\\User_data_selenium")
options.page_load_strategy = 'normal'
driver= webdriver.Chrome(options=options)
driver.get("https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&view_all_page_id=498384316938159&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=all")
ads_count = driver.find_element("xpath","//div[@class='x8t9es0.x1uxerd5.xrohxju.x108nfp6.xq9mrsl.x1h4wwuj.x117nqv4.xeuugli']").get_property("text")
print(ads_count)
# sleep(10)
# driver.find_element("xpath","//input[@class = 'inputtext _55r1 _6luy']").send_keys("")
# sleep(2)
# driver.find_element("xpath","//input[@class = 'inputtext _55r1 _6luy _9npi']").send_keys("")
# sleep(2)


# link = driver.find_element("xpath","//button[@data-cookiebanner='accept_button']").click()
# sleep(2)
# link = driver.find_element("xpath","//button[text()='Log In']").click()

sleep(10)
driver.quit()


#fbIndex UIPage_LoggedOut hasBanner _-kb _605a b_c3pyn-ahh chrome webkit win x1 Locale_en_US cores-gte4 _19_u hasCookieBanner

#//*[@id="facebook"]/body