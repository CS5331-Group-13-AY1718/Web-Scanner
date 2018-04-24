import requests

class OpenRedirect(object):
	def __init__(self, target):
		self.target = target
		self.url = target['url']
		self.path = target['path']
		self.partial_path = target['scheme'] + "://" + target['domain']
		self.query = target['query']
		self.results = {}
		self.exploit_param = {}
		self.vulnerable = False
		if 'method' in target:
			if target['method']:
				method = target['method'].upper()
			else:
				method = 'POST'
			self.method = method
		else:
			self.method = 'GET'
	
	# https://github.com/ak1t4/open-redirect-scanner/blob/master/payloads.list
	def scan(self):
		payloads = ['https://status.github.com/messages', '%27%68%74%74%70%73%3a%2f%2f%73%74%61%74%75%73%2e%67%69%74%68%75%62%2e%63%6f%6d%2f%6d%65%73%73%61%67%65%73%27', 'https%3A%2F%2Fstatus.github.com%2Fmessages']
		query_strings = ['?redirect=', '/', '//', '///', '////', '//%5c']
		for payload in payloads):
			for q in query_strings:
					payload_string = q + payload
					if self.query:
						response = requests.get(self.partial_path + self.path + "?" + self.query.split('=')[0] + '=' + payload_string, verify = True)
					else:
						response = requests.get(self.url + payload_string, verify = True)
					try:
						if response.history:
							self.vulnerable = True
							print '[+] Open Redirect Vulnerability: ' + self.path 
							self.exploit_param['url'] = payload_string
							add_scan_results()
					except:
						print "[!] Unable to connect: " + self.url + payload_string
						continue
						
		if self.vulnerable:
			return self.results 
		else:
			return None
			
	def add_scan_results():
		domain = self.partial_path
		if domain not in self.results:
			self.results[domain] = []

		result = {}
		result['endpoint'] = self.path
		result['params'] = self.exploit_param
		result['method'] = self.method
		self.results[domain].append(result)
			
		
		
		
	def generate_exploit(self, endpoint):
		pass