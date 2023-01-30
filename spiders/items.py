# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZipfilesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #file_urls = scrapy.Field()
    file_urls = scrapy.Field()
    file_names = scrapy.Field()
    files = scrapy.Field()
