# -*- coding: utf-8 -*-
import scrapy
import json
import time
import chardet
import re

class NewsPubSpider(scrapy.Spider):
    name = 'news_pub'
    #allowed_domains = ['www.xuexi.cn', 'https://boot-source.xuexi.cn']

    def start_requests(self):
        #爬取链接
        start_url = 'https://www.xuexi.cn/lgdata/tuaihmuun2.json?_st={}'.format(int(time.time()))
        yield scrapy.Request(url=start_url, dont_filter=True,callback=self.parse)

    def parse(self, response):
        url = 'https://boot-source.xuexi.cn/data/app/{}.js?callback=callback&_st={}'
        #print(response.text)
        data = json.loads(response.text)

        count = 0
        for item in data:
            pub_time = item['publishTime']
            #now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            #start_time = '2020-03-05 00:00:00'
            #start_timestamp = time.mktime(time.strptime(start_time,"%Y-%m-%d %H:%M:%S"))
            #now = time.time()
            time.sleep(2)
            item_id = item['itemId']
            detail_url = url.format(item_id, int(time.time()*1000))
            #https://boot-source.xuexi.cn/data/app/13089679410767194944.js?callback=callback&_st=

            meta = {}
            meta['type'] = item['type']
            meta['itemId'] = item_id
            meta['channelNames'] = item['channelNames']
            print('meta: ',meta)
            if count < 10:
                count = count + 1
                yield scrapy.Request(url=detail_url, dont_filter = True, meta= meta, callback=self.parse_detail)
            else:
                break

    def parse_detail(self, response):
        #charset = chardet.dect(response.content)
        #response.encoding = charset['encoding']
        data = re.search(r'{.*}', response.text, re.M|re.I).group()
        print(data)
        meta = response.meta
        print(meta)
        with open(meta['itemId'] + '.json', 'a') as f:
            f.write(data)

        


        
