
import traceback
import csv
import pandas as pd
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
    record_number = 0

    # Using a dummy website to start scrapy request
    def start_requests(self):
        # Open the CSV file for reading
        with open("data.csv") as csvfile:
            # Create a CSV reader
            reader = csv.reader(csvfile)
            next(reader)

            # Iterate over the rows in the CSV file
            for row in reader:
                WebsiteSpider.record_number+=1
                # Get the URL from the first column of the row
                url = row[1]
                print("URL IS ",url)
                # Generate a request for the URL
                yield scrapy.Request(url=url, callback=self.parse_website)


    def parse_website(self, response):

        # Extracting country names
        hrefs_xpath = "//a/@href[contains(., 'facebook') or contains(.,'contact') or contains(.,'instagram') or contains(.,'twitter') or contains(.,'linkedin')]"
        hrefs = response.xpath(hrefs_xpath).extract()

        hrefs_xpath2 = "//a/@href[contains(.,'contact') or contains(.,'about me')]"
        hrefs2 = response.xpath(hrefs_xpath2).extract()
        # Using Scrapy's yield to store output instead of explicitly writing to a JSON file

        facebook_link=""
        instagram_link=""
        twitter_link=""
        linkedin_link=""
        for href in hrefs:

            try:
                if "facebook" in href:
                    facebook_link = href
                if "instagram" in href:
                    instagram_link = href
                if "twitter" in href:
                    twitter_link = href
                if "linkedin" in href:
                    linkedin_link = href

            except Exception as e:
                print(traceback.format_exc())

        for href in hrefs2:

            try:
                if "contact"  or "about" in href:
                    contact_link = href
                    print("contact link", contact_link)
                    yield scrapy.Request(url=contact_link, callback=self.parse_contact,
                                         meta={'facebook': facebook_link, 'instagram': instagram_link, 'twitter': twitter_link, 'linkedin': linkedin_link})


            except Exception as e:
                print("error with yield is:", e)

        logger.info(f"Total number of links in website: {len(hrefs)}")


    def parse_contact(self, response):



        try:

            emails = re.findall(r'[\w\.-]+@[\w\.-]+', response.text)
            set_emails = set(emails)
            emails = list(set_emails)

            for item in list(emails):
                if ".com" not in item:
                    emails.remove((item))
            print(emails)
            item = SocialMediaLinks()
            item["facebook"] = response.meta['facebook']
            item["instagram"] = response.meta['instagram']
            item["twitter"] = response.meta['twitter']
            item["linkedin"] = response.meta['linkedin']
            item["emails"] = emails

            # reading the csv file
            df = pd.read_csv("data.csv")
            print("RECORD NUMBER",WebsiteSpider.record_number)
            df.loc[WebsiteSpider.record_number, 'facebook'] = response.meta['facebook']
            df.loc[WebsiteSpider.record_number, 'instagram'] = response.meta['instagram']
            df.loc[WebsiteSpider.record_number, 'twitter'] = response.meta['twitter']
            df.loc[WebsiteSpider.record_number, 'linkedin'] = response.meta['linkedin']
            df.loc[WebsiteSpider.record_number, 'emails'] = emails
            # writing into the file
            df.to_csv("data.csv", index=False)
            print(item)
            yield item

        except Exception as e:
            print("Exception",e)






