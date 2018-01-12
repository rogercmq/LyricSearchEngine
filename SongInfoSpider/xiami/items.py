# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SongUrlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    song_url=scrapy.Field() #歌曲链接

class LyricItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    lyric=scrapy.Field() #歌曲链接
    song_url=scrapy.Field() #歌曲链接
    
    
class SongInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    song_url=scrapy.Field() #歌曲链接
    song_title=scrapy.Field() #歌名
    album=scrapy.Field() #专辑
    singer=scrapy.Field() #歌手
    language=scrapy.Field() #语种、
    album_pic=scrapy.Field()#专辑图片
    lyrics=scrapy.Field()#歌词
    album_genre=scrapy.Field()#专辑风格
    listenNum = scrapy.Field()#专辑试听数
    collectNum = scrapy.Field()#专辑收藏数
    shareNum = scrapy.Field()#专辑分享数
    
    
