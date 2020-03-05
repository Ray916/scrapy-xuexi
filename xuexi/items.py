# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XuexiItem(scrapy.Item):
    # define the fields for your item here like:
    item_id = scrapy.Field()
    # item_type = scrapy.Field()
    # channels = scrapy.Field()
    # images = scrapy.Field()
    title = scrapy.Field()
    # audios = scrapy.Field()
    source = scrapy.Field()
    # videos = scrapy.Field()
    # voices = scrapy.Field()
    content = scrapy.Field()
    # categories = scrapy.Field()
    # tags = scrapy.Field()
    pub_time = scrapy.Field()
    # normalized_title = scrapy.Field()
    # normalized_content = scrapy.Field()

