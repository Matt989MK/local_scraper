import traceback
import csv
from urllib.parse import urljoin
import pandas as pd
from logzero import logfile, logger
import scrapy
import re
import sys
sys.path.append('C:\\Users\\moffi\\PycharmProjects\\scraping_web\\scraper') #change path to your pc
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
    #record_number = 0
    info_list =[]
    # Using a dummy website to start scrapy request
    def start_requests(self):
        # Open the CSV file for reading

        with open("data.csv") as csvfile: #read out data from .csv file and go through each link positioned in 2nd row
            # Create a CSV reader
            reader = csv.reader(csvfile)
            next(reader)
            test_number=0
            # Iterate over the rows in the CSV file
            for row in reader:
                test_number+=1
                # Get the URL from the first column of the row
                url = row[1]
                #print("URL IS ",url)
                # Generate a request for the URL
                #print("this is the list of items:", len(WebsiteSpider.info_list))

                yield scrapy.Request(url=url, callback=self.parse_website,meta={'test_number':test_number})

            # with open("items.csv", "w") as csvfile:
            #     # Create a CSV writer
            #     writer = csv.DictWriter(csvfile,
            #                             fieldnames=["index", "facebook", "instagram", "twitter", "linkedin", "emails"])
            #
            #     # Write the header row
            #     writer.writeheader()
            #     print("this is the list of items:", len(WebsiteSpider.info_list))
            #     # Write the data rows
            #     for item in WebsiteSpider.info_list:
            #         writer.writerow(item)

    def parse_website(self, response):
        print("PARSING WEBSITE URL:", response.url)
        # Extracting country names
        hrefs_xpath = "//a/@href[contains(., 'facebook') or contains(.,'contact') or contains(.,'instagram') or contains(.,'twitter') or contains(.,'linkedin')]" #looking for social media links
        hrefs = response.xpath(hrefs_xpath).extract()
        test_number = response.meta['test_number'] #We need that number to go through each row to the next one
        hrefs_xpath2 = "//a/@href[contains(.,'contact') or contains(.,'about me')]" #Thats looking for contact links like about us or contact us
        hrefs2 = response.xpath(hrefs_xpath2).extract()
        # Using Scrapy's yield to store output instead of explicitly writing to a JSON file

        facebook_link="N/A"
        instagram_link="N/A"
        twitter_link="N/A"
        linkedin_link="N/A"
        emails ="N/A"
        contact_link = "N/A"
        try:

            emails = re.findall(r'[\w\.-]+@[\w\.-]+', response.text)
            set_emails = set(emails)
            emails = list(set_emails)

            # for item in list(emails):
            #     if ".com" not in item:
            #         emails.remove((item))
            clear_bad_emails(emails)
            #print(emails)
        except Exception as e:
            print(e)

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

                    contact_link = urljoin(response.url, contact_link)
                    #print("contact link", contact_link)
            except Exception as e:
                print("error with yield is:", e)

        try:
            yield scrapy.Request(url=contact_link, callback=self.parse_contact,
                                 meta={'facebook': facebook_link, 'instagram': instagram_link, 'twitter': twitter_link,
                                       'linkedin': linkedin_link, 'emails': emails,'test_number':test_number})
        except Exception as e:
            print("ERROR IS",e)

        logger.info(f"Total number of links in website: {len(hrefs)}")


    def parse_contact(self, response):

        test_number = response.meta['test_number']

        try:
            if response.meta['emails']!="N/A":
                emails = re.findall(r'[\w\.-]+@[\w\.-]+', response.text)
                set_emails = set(emails)
                emails = list(set_emails)
                clear_bad_emails(emails) #need more options to filter out bad emails
                # for item in list(emails):
                #     if ".com" not in item:
                #         emails.remove((item))
            #print(emails)
            item = SocialMediaLinks()
            item["index"] = test_number
            item["facebook"] = response.meta['facebook']
            item["instagram"] = response.meta['instagram']
            item["twitter"] = response.meta['twitter']
            item["linkedin"] = response.meta['linkedin']
            item["emails"] = emails

            # reading the csv file
            df = pd.read_csv("data4.csv")
            print("WEBSITE ",response.url," RECORD NUMBER",test_number ,"FACEBOOK: ",response.meta['facebook']," INSTAGRAM: ",response.meta['instagram'])
            df.loc[test_number,'index']=test_number
            df.loc[test_number, 'facebook'] = response.meta['facebook']
            df.loc[test_number, 'instagram'] = response.meta['instagram']
            df.loc[test_number, 'twitter'] = response.meta['twitter']
            df.loc[test_number, 'linkedin'] = response.meta['linkedin']
            df.loc[test_number, 'emails'] = str(emails)
            # writing into the file
            df.to_csv("data4.csv", index=False)
            #WebsiteSpider.record_number += 1
            #WebsiteSpider.info_list.append(item)
            #print(WebsiteSpider.info_list)

            yield item #Data seems to be correct but its saving it in the wrong row

        except Exception as e:
            #WebsiteSpider.record_number += 1

            print("Exception",e)



def clear_bad_emails(emails):
    #print("called clear bad emails")
    for item in list(emails):
       # print("ITEM",item)
        try:
            if "careers" in item or "reservations" in item or "donations" in item or "events" in item or "activities" in item:
                #print('removeing email', item)
                emails.remove((item))
            if ".com" not in item:
                emails.remove((item))
        except Exception as e:
            print("cant remove email",e)

