# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class URLPipeline(object):
	def open_spider(self, spider):
		file_name = spider.start_urls[0].join('_urls.jl')
		self.file = open(file_name, 'w')
		self.urls = set()
		
	def close_spider(self, spider):
		self.file.close()
	
	def process_item(self, item, spider):
		if not isinstance(item, URLItem):
			return item 
			
		if item not in set:
			set.add(item)
			line = json.dumps(dict(item)) + "\n"
			self.file.write(line)
		
		return item

class FormPipeline(object):
	def open_spider(self, spider):
		file_name = spider.start_urls[0].join('_forms.jl')
		self.file = open(file_name, 'w')
		self.forms = set()
		
	def close_spider(self, spider):
		self.file.close()
	
	def process_item(self, item, spider):
		if not isinstance(item, FormItem):
			return item 
			
		if item not in self.urls:
			self.forms.add(item)
			line = json.dumps(dict(item)) + "\n"
			self.file.write(line)
		
		return item
	