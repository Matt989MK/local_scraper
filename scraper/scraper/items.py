# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SocialMediaLinks(scrapy.Item):
    index = scrapy.Field()
    facebook= scrapy.Field()
    instagram= scrapy.Field()
    linkedin= scrapy.Field()
    twitter= scrapy.Field()
    emails = scrapy.Field()

class ContactInfo(scrapy.Item):
    email = scrapy.Field()