# -*- coding: utf-8 -*-
import scrapy
import json
import time
import chardet
import re

from xuexi.items import XuexiItem

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

        start_time = '2020-03-04 09:00:00'
        start_st = time.mktime(time.strptime(start_time,"%Y-%m-%d %H:%M:%S"))
        now_st = time.time()
        # count = 0
        for item in data:
            pub_time = item['publishTime']
            pub_st = time.mktime(time.strptime(pub_time,"%Y-%m-%d %H:%M:%S"))

            item_id = item['itemId']
            detail_url = url.format(item_id, int(time.time()*1000))
            #https://boot-source.xuexi.cn/data/app/13089679410767194944.js?callback=callback&_st=

            meta = {}
            meta['type'] = item['type']
            meta['itemId'] = item_id
            meta['channelNames'] = item['channelNames']
            print('meta: ',meta)

            if pub_st < start_st or pub_st > now_st - 24*60*60:
                # if count < 3:
                #     count = count + 1
                time.sleep(2)
                yield scrapy.Request(url=detail_url, dont_filter = True, meta= meta, callback=self.parse_detail)
                # else:
                #     break
            else:
                break

    def parse_detail(self, response):
        #charset = chardet.dect(response.content)
        #response.encoding = charset['encoding']
        result = re.search(r'{.*}', response.text, re.M|re.I).group()
        meta = response.meta

        #file_path = '/home/xzw/scrapy/xuexi/'
        file_path = ''
        with open(file_path + meta['itemId'] + '.json', 'w') as f:
            f.write(result)

        data = json.loads(result)

        item = XuexiItem()
        item['item_id'] = meta['itemId']
        #item['item_type'] = meta['type']
        #item['channels'] = meta['channelNames']

        #item['images'] = data['image']
        #item['title'] = data['title']

        #item['audios'] = data['audios']

        item['source'] = data['show_source']
        #item['videos'] = data['videos']
        #item['voices'] = data['voices']
        #item['content'] = data['content']
        #item['categories'] = data['category']
        #item['tags'] = data['show_tag']
        item['pub_time'] = data['publish_time']
        item['title'] = data['normalized_title']
        item['content'] = data['normalized_content']

        yield item
        
        
        
        

        


        
