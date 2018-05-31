# -*- coding: utf-8 -*-

import scrapy
import re
import json
from Tracker.items import CateShopItem


class CitiesSpider(scrapy.Spider):
    name = "cities"
    allowed_domains = ["meituan.com"]
    start_urls = ["http://www.meituan.com/changecity/"]
    link_to_city = {}

    def parse(self, response):
        # 拿到每个城市的美团链接，比如济南，将得到一个 http://www.jn.meituan.com
        city_links = response.xpath('//a[@class="link city "]/@href').extract()
        city_names = response.xpath('//a[@class="link city "]/text()').extract()
        for i in xrange(0, len(city_links)):
            link = city_links[i]
            map_key = re.match(r'//([a-z]+)\.meituan\.com', link).group(1)
            name = city_names[i]
            # 将城市简写与城市名称对应起来，比如 jn -> 济南
            self.link_to_city[map_key] = name
            # 将链接拼为美团美食的链接，并继续爬取
            cateLink = "http:" + link + "/meishi"
            url = response.urljoin(cateLink)
            yield scrapy.Request(url, self.parse_cate_in_city)


    def parse_cate_in_city(self, response):
        search = re.search(r'.*("poiLists":.*),"comHeader"', response.body)
        if search:
            cateList = "{" + search.group(1) + "}"
            cateListAsJson = json.loads(cateList)
            poilnfos = cateListAsJson["poiLists"]["poiInfos"]
            if(len(poilnfos) == 0):
                print "No more data in %s" % response.url
            else:
                # 从 url 中获取城市简写
                city_map_key = re.match(r'http://([a-z]+).*', response.url).group(1)
                # 收集爬取到的商家信息
                for item in poilnfos:
                    print item
                    cateShopItem = CateShopItem()
                    cateShopItem['avgPrice'] = item["avgPrice"]
                    cateShopItem['allCommentNum'] = item["allCommentNum"]
                    cateShopItem['shopAvgScore'] = item["avgScore"]
                    cateShopItem['shopName'] = item["title"]
                    cateShopItem['shopAddress'] = item["address"]
                    cateShopItem['shopCityName'] = self.link_to_city[city_map_key]
                    yield cateShopItem
                # 继续分页爬取
                # 先看看当前的 url 是第几页
                match_index = re.match(r'http://.*?meituan.com/meishi/pn(\d+).*?', response.url)
                if match_index:
                    current_index = match_index.group(1)
                    new_index = int(current_index) + 1
                    next_page = re.sub(r'\d+/$', "%d%s" % (new_index, "/"), response.url)
                    url = response.urljoin(next_page)
                    yield scrapy.Request(url, self.parse_cate_in_city)
                else:
                    # 当前抓取的是第一页
                    next_page = response.url + "pn2/"
                    url = response.urljoin(next_page)
                    yield scrapy.Request(url, self.parse_cate_in_city)
        else:
            print "No match in %s" % response.url


