from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders import linkcrawlerspider
from urlparse import urlparse
from plugins import dirt, ci
import argparse
import scrapy
import os.path
import json
		
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

	
def generate_json_report(results)	

def scan(targets):
	sqli_vuln = []
	csrf_vuln = []
	or_vuln = []
	sqli_vuln = []
	ssci_vuln = []
	dt_vuln = {}
	
	with open(targets) as f:
		for line in f:
			url = json.loads(line)
			dt_results = dirt.DirectoryTraversal(url).scan()
			ci_results = ci.CommandInjection(url).scan()
	
	results = (dt_results, ci_results)

if __name__ == "__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('-c', '--crawl', action='store', help='Target URL(s) for crawling', dest='url')
	argparser.add_argument('-s', '--scan', action='store', help='JSON file containing URLs for scanning', dest='targets')
	args = argparser.parse_args()
	if not any (vars(args).values()):
		argparser.error('No arguments provided, please choose an operation.')
	if args.url:
		crawl(args.url)
	if args.targets:
		scan(args.targets)
