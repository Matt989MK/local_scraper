import sys
import traceback
from time import time, sleep
from ssl import DER_cert_to_PEM_cert
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib2to3.pgen2 import  driver
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException
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
search_bar=driver.get("https://www.google.com/search?q=tree+works+in+california") #Going to google searching for that


start = time.perf_counter()
element = '//span[@class="wUrVib OSrXXb"]'

# Use the WebDriverWait class to wait for the element to appear
try:
    element_present = EC.presence_of_element_located((By.XPATH, element))
    WebDriverWait(driver, 3).until(element_present)
except (HttpError, DNSLookupError, TimeoutError, TCPTimedOutError):
    # Handle any errors that occur while waiting for the element
    pass

# Once the element is present, press it using the click method
driver.find_element(By.XPATH, element).click()
#sleep(1)
#driver.find_element("xpath","//span[@class='wUrVib OSrXXb']").click() #trying to click the "more businesses button"

page_num=1

def FindBusiness(count_var):
    count_var+=1
    sleep(4)

    try:
        google_places = driver.find_elements("xpath", "//div[@class='rllt__details']")
    except StaleElementReferenceException:
        google_places = driver.find_elements("xpath", "//div[@class='rllt__details']")

    print("google places", len(google_places))
    #sleep(0.3)
    name=""
    website=""
    address=""
    phone_number=""
    review=""
    review_amount=""
    list_counter=0

    for place in google_places:
        print("place",place)
        #sleep(2)
        try:
            place.click() #1 for each place we click the element it does not work when there is an extra button like "schedule"
            sleep(0.6)
        except StaleElementReferenceException:
            sleep(4)
            place.click()
        print("gmb works")
        try:
            element_present = EC.presence_of_element_located((By.XPATH, "//div[@class='immersive-container']"))
            WebDriverWait(driver, 6).until(element_present)
            gmb_container = driver.find_element("xpath", "//div[@class='immersive-container']")  # it has all the business info inside

            try:
                list_of_elements = gmb_container.find_elements("xpath",
                                                           "//div[@class='zloOqf PZPZlf']")  # list of 1. address 2. hours 3. phone number
            except StaleElementReferenceException:
                sleep(1)
                list_of_elements = gmb_container.find_elements("xpath",
                                                               "//div[@class='zloOqf PZPZlf']")
                print("AVOIDED STALE")


            # print(len(list_of_elements))
            print("list of elements works")
            try:
                test_website = gmb_container.find_elements("xpath",
                                                           "//a[@class='dHS6jb']")  # contains 1. website 2. directions 3. save 4. call
                print("test website works")
            except StaleElementReferenceException:
                sleep(1)
                test_website = gmb_container.find_elements("xpath",
                                                           "//a[@class='dHS6jb']")  # contains 1. website 2. directions 3. save 4. call
                print("test website works BUT WAS STALE")

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
            try:
                test_review = gmb_container.find_elements("xpath",
                                                          "//span[@class='NdWbqe Y0A0hc']")  # it has all reviews thats why we look for it in the gmb container
                split_review = test_review[len(test_review) - 1].text.split(
                    "\n")  # test review contains both review and review amount so we split it
                review = split_review[0]
                review_amount_raw = split_review[1]
                if "(" in review_amount_raw and ")" in review_amount_raw:
                    # If it does, remove the text between them
                    review_amount = review_amount_raw.replace('(', "").replace(')', "")
                print('review: ', review, "review amount", review_amount)
            except Exception as e:
                print(e)



            for item in list_of_elements:
                try:
                    if "Adres" in item.get_attribute('innerText'):
                        address = item.text
                        if "Adres:" in address:
                            # If it does, remove it
                            address = address.replace("Adres:", "")
                        print(address)
                except Exception as e:
                    print("no address ", e)

            for item in test_website:
                try:
                    if "Strona" in item.get_attribute('innerText'):  # WORKS

                        website = item.get_attribute("href")
                        print("website", website)
                        # website_handler(website) #no need for it at the moment
                        if website == None:
                            no_website = gmb_container.find_element("xpath", "//span[@class='qe9kJc']").text
                            print("no website found", no_website)

                except Exception as e:
                    print("no website: ", e)

            row = [name, website, address, phone_number, review, review_amount]
            data.append(row)
            # sleep(1)
        except (HttpError, DNSLookupError, TimeoutError, TCPTimedOutError):
            # Handle any errors that occur while waiting for the element
            pass
        print("element: ", list_counter, " out of ", len(google_places))
        list_counter+=1






        #with each of the below like "Adres" or "Strona" we need to make it normalized to browser language "Adres" means Address in my lang "Strona" means website


    try:
        sleep(1)

        driver.find_element("xpath", "//a[@id='pnnext']").click() #Takes us to next google page, once its ran out script ends
        print("PAGE NUMBER:", count_var)
        FindBusiness(count_var)
    except BaseException as ex:
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()

        for trace in trace_back:
            stack_trace.append(
                "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" % ex_value)
        print("Stack trace : %s" % stack_trace)


def SaveData():
    with open("scraper/scraper/spiders/data.csv", "w", encoding="utf-8", newline="") as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the data to the CSV file
        writer.writerows(data)
    #sleep(10)
    end = time.perf_counter()

    # calculate the total time it took to execute the script
    elapsed = end - start

    # print the total time it took to execute the script
    print(f"Total time: {elapsed:.2f} seconds")
    driver.quit()


FindBusiness(0)
SaveData()



