from time import time, sleep
from ssl import DER_cert_to_PEM_cert
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib2to3.pgen2 import  driver
import csv
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
options = Options()
options.add_argument("--user-data-dir=C:\\Users\\moffi\\AppData\\Local\\Google\\Chrome\\User Data\\User_data_selenium") #Use that for cookies with facebook_scrape.py once logged in no need to call log in functions again
options.page_load_strategy = 'normal'
driver= webdriver.Chrome(options=options)
data = [
    ["name", "website", "address", "phone number", "rating", "amount of ratings","facebook","instagram","twitter","linkedin","emails"],
]


#city = input("city: ")
#niche = input("niche: ")
#driver.get("https://www.google.com/search?q="+city+"+"+niche) #I commented it out for now to not have to input each time
#print("https://www.google.com/search?q="+city+"+"+niche)
driver.get("https://www.google.com/search?q=spa+in+california") #Going to google searching for that
sleep(2)
# try:
#     driver.find_element("xpath","//button[@id='W0wltc']").click()
# except Exception as e:
#     print(e)
sleep(1)
driver.find_element("xpath","//span[@class='wUrVib OSrXXb']").click() #trying to click the "more businesses button"
page_num=1
#rlfl__tls rl_tls <====== is the whole google places element


#link = driver.find_element("xpath","//button[@data-cookiebanner='accept_button']").click()
def website_handler(url):

    ActionChains(driver).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()

    driver.get(url)
    sleep(5)
    test_link=driver.find_element("xpath","//a/@href[contains(., 'facebook') or contains(.,'contact') or contains(.,'instagram') or contains(.,'twitter')]")
    print(test_link)
    sleep(30)
def FindBusiness():
    sleep(3)
    google_places = driver.find_elements("xpath", "//div[@class='uMdZh tIxNaf mnr-c']")
    print("google places", len(google_places))
    sleep(1)
    name=""
    website=""
    address=""
    phone_number=""
    review=""
    review_amount=""
    for place in google_places:
        print("place",place)
        sleep(2)
        place.click() #1 for each place we click the element
        sleep(1)

        gmb_container = driver.find_element("xpath", "//div[@class='immersive-container']") #it has all the business info inside


        try:
            name = driver.find_element("xpath", "//div[@class='SPZz6b']").text
        except Exception as e:
            name = "NA"
        print(name)
        try:
            phone_number = driver.find_element("xpath", "//span[@class='LrzXr zdqRlf kno-fv']").text
        except Exception as e:
            phone_number = "NA"
        print(phone_number)


        list_of_elements = gmb_container.find_elements("xpath","//div[@class='zloOqf PZPZlf']") #list of 1. address 2. hours 3. phone number
        #print(len(list_of_elements))

        test_website = gmb_container.find_elements("xpath","//a[@class='dHS6jb']") #contains 1. website 2. directions 3. save 4. call
        try:
            test_review = gmb_container.find_elements("xpath","//span[@class='NdWbqe Y0A0hc']") #it has all reviews thats why we look for it in the gmb container
        except Exception as e:
            print(e)

        split_review= test_review[len(test_review)-1].text.split("\n") #test review contains both review and review amount so we split it
        review=split_review[0]
        review_amount=split_review[1]
        print('review: ',review, "review amount", review_amount)


        #with each of the below like "Adres" or "Strona" we need to make it normalized to browser language "Adres" means Address in my lang "Strona" means website
        for item in list_of_elements:
            try:
                if "Adres" in item.get_attribute('innerText'):
                    address= item.text
                    print(address)
            except Exception as e:
                print("no address ",e)

        for item in test_website:
            try:
                if "Strona" in item.get_attribute('innerText') :  # WORKS

                    website = item.get_attribute("href")
                    print("website",website)
                   # website_handler(website) #no need for it at the moment
                    if website==None:
                        no_website = gmb_container.find_element("xpath", "//span[@class='qe9kJc']").text
                        print("no website found",no_website)
            except Exception as e:
                print("no website: ",e)

        row = [name,website,address,phone_number,review,review_amount]
        data.append(row)
        sleep(2)
    try:
        sleep(5)
        driver.find_element("xpath", "//a[@id='pnnext']").click() #Takes us to next google page, once its ran out script ends
        FindBusiness()

    except Exception  as e:
        print("finito",e)

def SaveData():
    with open("scraper/scraper/spiders/data.csv", "w", encoding="utf-8", newline="") as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the data to the CSV file
        writer.writerows(data)
    sleep(10)
    driver.quit()


FindBusiness()
SaveData()



