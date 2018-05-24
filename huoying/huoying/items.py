# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuoyingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    chapter_url = scrapy.Field()
    chapter_title = scrapy.Field()
    pass
