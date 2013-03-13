import xml.etree.ElementTree as ET
from hashlib import sha1

from config import cfgdict
import wxapi

class WxError(Exception):
	"""docstring for WxError"""
	def __init__(self, errstr):
		super(WxError, self).__init__()
		self.errstr = errstr
		

class WxRequest(object):
	"""docstring for WxRequest"""

	def __init__(self, rqtype, xmlstr):
		super(WxRequest, self).__init__()
		self.rqtype= rqtype
		self.api= wxapi.request[rqtype]
		self.keys= [x[0] for x in self.api]
		self.argdict= {x:y for x,y in zip((key for key in self.keys),(xmlobj.text for xmlobj in ET.fromstring(xmlstr))) if y not in ['\n',None,'\r\n']}
		self.argdict={}

	def _digest(self, xmlobj, target=self.api):
		result={}
		for item in target:
			if type(item[1]) == list:
				result[item[0]]= [self._digest(x,item[1])]


class WxAuth(object):
	"""docstring for WxAuth"""
	check = wxapi.auth['check'][0]
	sendback = wxapi.auth['sendback'][0]

	def __init__(self, arg, config=cfgdict):
		super(WxAuth, self).__init__()
		self.arg = arg
		self.arg.update(cfgdict)
		self.checkarg = tuple(self.arg[x] for x in wxapi.auth['check'][1])
		self.sendbackarg = tuple(self.arg[x] for x in wxapi.auth['sendback'][1])

	def act(self):
		try:
			if self.check(self.checkarg)
				return self.sendback(self.sendbackarg)
			else:
				return False
		except Exception e:
			print('Exception while calculating signature !')
			raise e

