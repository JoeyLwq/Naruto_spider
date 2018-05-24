# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from huoying.items import HuoyingItem
import re
import os
import urllib.request

class Spider1Spider(scrapy.Spider):
    name = 'spider_1'
    jpg_addr = 'http://n5.1whour.com/'
    book_addr = 'http://comic.kukudm.com'
    allowed_domains = ['http://comic.kukudm.com','n5.1whour.com']
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    def start_requests(self):  # 模拟成浏览器访问
        yield Request('http://comic.kukudm.com/comiclist/3/', headers=self.header)


    def parse(self, response):
        item = HuoyingItem()
        item['chapter_url'] = response.xpath('//dd/a[1]/@href').extract()
        item['chapter_title'] = response.xpath('//dd/a[1]/text()').extract()
        for i in range(len(item['chapter_url'])):
            item['chapter_url'][i] = self.book_addr + item['chapter_url'][i]
        yield item

        # 选择要爬取的册数
        for i in range(54,55):
            yield Request(url=item['chapter_url'][i],callback=self.parse2,headers=self.header,dont_filter=True)

    pattern = re.compile(r'\+"(.*?)\'><span', re.S)
    # pattern_next = re.compile(r'\+"(.*?)\'></span', re.S)
    def parse2(self,response):
        text = response.xpath('//script/text()').extract()[0]
        title = response.xpath('//title/text()').extract()[0]
        dir = 'C:/Users/56496/Pictures/临时复制/temp/' + title

        if not os.path.exists(dir):
            os.makedirs(dir)
        jpg_addr2 = re.findall(self.pattern,text)[0]
        jpg_url = self.jpg_addr + jpg_addr2

        if not os.path.exists(dir+'/'+jpg_addr2+'.jpg'):
            try:
                pic = urllib.request.urlopen(jpg_url).read()
                with open(dir+'/'+jpg_addr2[-6:-4]+'.jpg','wb') as f:
                    f.write(pic)
            except Exception as e:
                print(e)

        if response.xpath('//a[2]/@href').extract():
            next_page = 'http://comic.kukudm.com' + response.xpath('//a[2]/@href').extract()[0]
        else:
            next_page = 'http://comic.kukudm.com' + response.xpath('//a[1]/@href').extract()[0]

        yield Request(url= next_page,callback=self.parse2,headers=self.header,dont_filter=True)




