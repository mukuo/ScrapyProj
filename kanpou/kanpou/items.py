# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KanpouTodayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    paper = scrapy.Field() #官報の日付と号数
    title = scrapy.Field() #公告のタイトル
    links = scrapy.Field() #URL（相対パス）

