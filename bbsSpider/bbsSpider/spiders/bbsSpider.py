import scrapy
import hashlib
import time
import re
from bbsSpider.items import BbsspiderItem
from scrapy.selector import HtmlXPathSelector

class bbsSpider(scrapy.spiders.Spider):
    name = "bbsSpider"
    allowed_domains = ["ty.netease.com"]
    start_urls = [
        "http://ty.netease.com",
    ]


    def parse(self, response):
        md5_obj = hashlib.md5()
        print("respons: ",response)
        url = response.url #爬取时请求的url
        if(response.status!=200):
            return
        if(re.match('http://ty.netease.com/forum-\d+-\d+.html$',url) is not None or url=='http://ty.netease.com'):
            hxs = HtmlXPathSelector(response)
            urls = hxs.xpath('//a/@href').extract()
            for url in urls:
                url_new = ''
                print("----",url)
                if(re.match('//ty.netease.com/forum-\d+-\d+.html$',url) is not None):
                    url_new = "http:"+url
                if(re.match('/forum-\d+-\d+.html$',url) is not None):
                    url_new = "http://ty.netease.com"+url
                if(re.match('//ty.netease.com/thread-\d+-\d+-\d+.html$',url) is not None):
                    url_new = "http:"+url
                if(re.match('/thread-\d+-\d+-\d+.html$',url) is not None):
                    url_new = "http://ty.netease.com"+url
                if(url_new!=''):
                    print("++++",url_new)
                    yield scrapy.Request(url_new, self.parse)

        if(re.match('http://ty.netease.com/thread-\d+-\d+-\d+.html$',url) is not None):
            print("return")
            return
            item = BbsspiderItem()
            hxs = HtmlXPathSelector(response)
            titles1 = hxs.xpath('//div[@class="bm cl"]//div[@class="z"]/a/text()').extract()
            if(len(titles1)<1):
                 return
            label1 = '_'.join(titles1[0:len(titles1)-1])
            title = titles1[-1]
            item['label1'] = label1
            item['title'] = title
            titles2 = hxs.xpath('//h1[@class="ts"]/a/text()').extract()
            label2 = titles2[0].replace('[','').replace(']','')
            item['label2'] = label2
            contents = hxs.xpath('//div[@class="t_fsz"]//td[@class="t_f"]/text()').extract()
            item['content'] = ''.join(contents).replace('\r\n','')
            item['replyNum'] = len(contents)

            item['url'] = url
            md5_obj.update(url.encode('utf8'))
            umd5 = md5_obj.hexdigest()
            item['umd5'] = umd5

            date = time.strftime("%Y-%m-%d", time.localtime())
            item['create_time'] = date
            item['update_time'] = date
            yield item
