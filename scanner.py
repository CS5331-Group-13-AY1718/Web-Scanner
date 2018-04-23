from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders import linkcrawlerspider
from twisted.internet import reactor
from urlparse import urlparse
import argparse
import scrapy
import os.path
		
def crawl(urls):
	if os.path.isfile(urls):
		start_urls = [line.strip() for line in open(urls)]
	else:
		start_urls = urls.split(',')
	settings = get_project_settings()
	for url in start_urls:
		domain_name = urlparse(url).netloc
		settings.set('filename', domain_name)
		process = CrawlerProcess(settings)
		process.crawl(linkcrawlerspider.LinkCrawlerSpider,
start_urls=[url], allowed_domains = [domain_name])
	process.start()

	

if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('-c', '--crawl', action='store', help='Target URL(s) for crawling', dest='url')
	argparser.add_argument('-s', '--scan', action='store', help='JSON file containing URLs for scanning', dest='targets')
	args = argparser.parse_args()
	if not any (vars(args).values()):
		argparser.error('No arguments provided, please choose an operation.')
	if args.url:
		crawl(args.url)
