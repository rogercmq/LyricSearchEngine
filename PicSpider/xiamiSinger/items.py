# -*- coding: utf-8 -*-

import scrapy

class XiamisingerItem(scrapy.Item):
    name = scrapy.Field()
    picUrl = scrapy.Field()
    urlA = scrapy.Field()
    urlB = scrapy.Field()
    urlC = scrapy.Field()
