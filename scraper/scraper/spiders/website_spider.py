
import traceback

from selenium import webdriver
from logzero import logfile, logger
import scrapy
import re
import sys
sys.path.append('C:\\Users\\moffi\\PycharmProjects\\scraping_web\\scraper')
from scraper.items import SocialMediaLinks
import logging

logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)
class WebsiteSpider(scrapy.Spider):

    # Initializing log file
    logfile("../../../openaq_spider.log", maxBytes=1e6, backupCount=3)
    name = "website_spider"


    # Using a dummy website to start scrapy request
    def start_requests(self):
        url = "http://smithgill.com/"
        yield scrapy.Request(url=url, callback=self.parse_website)

    def parse_website(self, response):
        # driver = webdriver.Chrome()  # To open a new browser window and navigate it

        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

        # Getting website link
        driver.get("http://smithgill.com/")

        # Implicit wait
        driver.implicitly_wait(10)

        # Explicit wait
        #wait = WebDriverWait(driver, 5)
       # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card__title")))
        link  = "http://smithgill.com/"
        # Extracting country names
        hrefs_xpath = "//a/@href[contains(., 'facebook') or contains(.,'contact') or contains(.,'instagram') or contains(.,'twitter') or contains(.,'linkedin')]"
        hrefs = response.xpath(hrefs_xpath).extract()
        # Using Scrapy's yield to store output instead of explicitly writing to a JSON file
        for href in hrefs:

            try:
                if "facebook" in href:
                    facebook_link = href
                    print("facebook: ",facebook_link)
                    # check ads + recent posts engagement ratio + posts on ads engagement ratio
                if "instagram" in href:
                    # check ads + recent posts engagement ratio + posts on ads engagement ratio

                    instagram_link = href
                    print("instagram: ",instagram_link)

                if "twitter" in href:
                    #idk what yet
                    twitter_link = href
                    print("twitter: ",twitter_link)
                if "linkedin" in href:
                    linkedin_link = href
                    print("linkedin: ",linkedin_link)
                try:
                    if "contact" in href:
                        contact_link = href
                        print("contact link", contact_link)
                        yield scrapy.Request(url=contact_link, callback=self.parse_contact,
                                             meta={'contact': contact_link})


                        emails = response.meta['emails']
                        print("emails",response.meta['emails'])
                except Exception as e:
                    print("error with yield is:", e)

            except Exception as e:
                print(traceback.format_exc())
        #meta_contact = {'facebook': facebook_link, 'instagram': instagram_link, 'twitter': twitter_link, 'linkedin': linkedin_link,'emails': emails}

        item = SocialMediaLinks()
        item["facebook"] = facebook_link
        #item["instagram"] = instagram_link
        # item["twitter"] = twitter_link
        #item["linkedin"] = linkedin_link
        #item["emails"] = emails

        yield item

        driver.quit()
        logger.info(f"Total number of links in website: {len(hrefs)}")

    def parse_testing(self, response):
        print("parse testing")
        yield
    def parse_contact(self, response):
        #test_var_contact = "contact Doesnt work"
        #link = response.meta['link']
        print("meta test", response.meta['contact'])
        link = response.meta['contact']
        print('link is',link)
        emails="test var"
        try:
            test_var_contact = " contact works"
            print("contact key")
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', response.text)
            set_emails = set(emails)
            emails = list(set_emails)

            for item in list(emails):
                if ".com" not in item:
                    emails.remove((item))

            meta_data = {'emails': emails}
            print("meta data",meta_data)
            # yield scrapy(url="http://smithgill.com/", callback=self.parse_testing,
            #                      meta={'contact_key': "str(emails)"})
            yield scrapy.Request(url="http://smithgill.com/", callback=self.parse_testing,
                                 )
            #print("meta_contact", meta_contact)
        except Exception as e:
            print("Exception",e)






