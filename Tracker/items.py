# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CateShopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 人均价格
    avgPrice = scrapy.Field()
    # 商店名称
    shopName = scrapy.Field()
    # 商店平均评分
    shopAvgScore = scrapy.Field()
    # 总评论数
    allCommentNum = scrapy.Field()
    # 商店地址
    shopAddress = scrapy.Field()
    # 该商店所在城市
    shopCityName = scrapy.Field()

