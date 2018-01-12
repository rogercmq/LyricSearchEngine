# -*- coding: utf-8 -*-
import scrapy,time
from xiamiSinger.items import XiamisingerItem

class SingerpicSpider(scrapy.Spider):
    name = 'SingerpicSpider'
    allowed_domains = ['xiami.com']
    song_url_file = './urls.csv'

    def __init__(self, *args, **kwargs):
        #从song_url.csv 文件中读取得到所有歌曲url
        f = open(self.song_url_file,"r")
        lines = f.readlines()
        #这里line[:-1]的含义是每行末尾都是一个换行符，要去掉
        #这里in lines[1:]的含义是csv第一行是字段名称，要去掉
        song_url_list=[line[:-1] for line in lines[2:]]
        f.close()
        self.start_urls = song_url_list

    def parse(self, response):
        singer_url = response.xpath('.//table[@id="albums_info"]/tr[2]/td[2]//a/@href')[0].extract()
        singer = response.urljoin(singer_url)
        yield scrapy.Request(url=singer, callback=self.parseSingerInfo)

    def parseSingerInfo(self,response):
        XiamisingerItemA = XiamisingerItem()
        XiamisingerItemA['name'] = response.xpath('.//div[@id="artist_photo"]/a/@title')[0].extract()
        pic_urls = response.xpath('.//div[@id="artist_photo"]/a/@href')[0].extract()
        XiamisingerItemA['picUrl'] = response.urljoin(pic_urls)
        try:
            infoA = response.xpath('.//div[@id="artist_photo"]/p/a[1]/@href')[0].extract()
            XiamisingerItemA['urlA'] = response.urljoin(infoA)
        except:
            pass
        try:
            infoB = response.xpath('.//div[@id="artist_photo"]/p/a[2]/@href')[0].extract()
            XiamisingerItemA['urlB'] = response.urljoin(infoB)
        except:
            pass
        try:
            infoC = response.xpath('.//div[@id="artist_photo"]/p/a[3]/@href')[0].extract()
            XiamisingerItemA['urlC'] = response.urljoin(infoC)
        except:
            pass
        return XiamisingerItemA

