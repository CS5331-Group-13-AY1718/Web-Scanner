# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from crawler.items import *

class URLPipeline(object):
	@classmethod
	def from_crawler(cls, crawler):
		settings = crawler.settings
		pipeline = cls(settings)
		return pipeline
	
	def __init__(self, settings):
		self.filename = settings.get('filename')

	def open_spider(self, spider):
		file_name = self.filename + '.json'
		self.file = open(file_name, 'a')
		self.urls = set()
		
	def close_spider(self, spider):
		self.file.close()
	
	def process_item(self, item, spider):
        	if not isinstance(item, URLItem):
				return item 
			
		if item not in self.urls:
			self.urls.add(item)
			line = json.dumps(dict(item)) + "\n"
			self.file.write(line)
		
		return item

class FormPipeline(object):
	@classmethod
	def from_crawler(cls, crawler):
		settings = crawler.settings
		pipeline = cls(settings)
		return pipeline
	
	def __init__(self, settings):
		self.filename = settings.get('filename')
		
	def open_spider(self, spider):
		file_name = self.filename + '.json'
		self.file = open(file_name, 'a')
		self.forms = set()
		
	def close_spider(self, spider):
		self.file.close()
	
	def process_item(self, item, spider):
        	if not isinstance(item, FormItem):
				return item 
			
		if item not in self.forms:
			self.forms.add(item)
			line = json.dumps(dict(item)) + "\n"
			self.file.write(line)
		
		return item
	
