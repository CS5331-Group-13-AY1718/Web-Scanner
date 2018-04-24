from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders import linkcrawlerspider
from urlparse import urlparse
from plugins import dirt, ci, sqli, or
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

	
def generate_json_report(results):
	(dt_results, ci_results, sqli_results, or_results) = results
	sqli_json = {'class':'SQL Injection', 'results': {}}
	ssci_json = {'class': 'Server Side Code Injection', 'results': {}}
	dt_json = {'class': 'Directory Traversal', 'results': {}}
	or_json = {'class': 'Open Redirect', 'results': {}}
	csrf_json = {'class' : 'CSRF', 'results': {}}
	ci_json = {'class' : 'Command Injection', 'results': {}}
	
	if dt_results is not None:
		for result in dt_results:
			for domain in result:
				if domain not in dt_json['results']:
					dt_json['results'][domain] = []
				dt_json['results'][domain].append(result[domain]) 
	
	if ci_results is not None:
		for result in ci_results:
			for domain in result:
				if domain not in ci_json['results']:
					ci_json['results'][domain] = []
				ci_json['results'][domain].append(result[domain])
	
	if sqli_results is not None:
		for result in sqli_results:
			for domain in result:
				if domain not in sqli_json['results']:
					sqli_json['results'][domain] = []
				sqli_json['results'][domain].append(result[domain])
	
	if or_results is not None:
		for result in or_results:
			for domain in result:
				if domain not in or_json['results']:
					or_json['results'][domain] = []
				or_json['results'][domain].append(result[domain])
	
	out_ci = "ci.json"
	with open(out_ci, 'w') as ci_f:
		ci_f.write(json.dumps(ci_json))
	
	out_dt = "dt.json"
	with open(out_dt, 'w') as dt_f:
		dt_f.write(json.dumps(dt_json))

	out_sqli = "sqli.json"
	with open(out_sqli, 'w') as sqli_f:
		sqli_f.write(json.dumps(sqli_json))
	
	out_or = "or.json"
	with open(out_or, 'w') as or_f:
		or_f.write(json.dumps(or_json))
		
def scan(targets):
	sqli_vuln = []
	csrf_vuln = []
	or_vuln = []
	ci_vuln = []
	ssci_vuln = []
	dt_vuln = []
	
	with open(targets) as f:
		for line in f:
			url = json.loads(line)
			dt_results = dirt.DirectoryTraversal(url).scan()
			if dt_results is not None:
				dt_vuln.append(dt_results)
			
			ci_results = ci.CommandInjection(url).scan()
			if ci_results is not None:
				ci_vuln.append(ci_results)
			
			sqli_results = sqli.SQLInjection(url).scan()
			if sqli_results is not None:
				sqli_vuln.append(sqli_results)
			
			or_results = or.OpenRedirect(url).scan()
			if or_results is not None:
				or_vuln.append(or_results)
	
	results = (dt_vuln, ci_vuln, sqli_vuln, or_vuln)
	generate_json_report(results)

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
