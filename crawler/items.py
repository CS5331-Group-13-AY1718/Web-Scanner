# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class URLItem(scrapy.Item):
	scheme = scrapy.Field()
	domain = scrapy.Field()
	path = scrapy.Field()
	params = scrapy.Field()
	query = scrapy.Field()
	fragment = scrapy.Field()
	port = scrapy.Field()
	url = scrapy.Field()
    
class FormItem(scrapy.Item):
	form_id = scrapy.Field()
	url = scrapy.Field()
	inputs = scrapy.Field()
	method = scrapy.Field()
	action = scrapy.Field()
	