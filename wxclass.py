import lxml.etree as ET
from hashlib import sha1
#from copy import deepcopy
from time import time

class WxError(Exception):
	"""docstring for WxError"""
	def __init__(self, errstr):
		super(WxError, self).__init__()
		self.errstr = errstr
		

class WxRequest(object):
	"""docstring for WxRequest"""
	def __init__(self, xmlinf, fromstr=True, debug=False):
#		super(WxRequest, self).__init__()
		if debug:
			self.argdict= xmlinf
			return None
		if fromstr:
			xmlobj= ET.fromstring(xmlinf)
		else:
			xmlobj= ET.parse(xmlinf)
		self.argdict= WxRequest._parse(xmlobj)

	@staticmethod
	def _parse(xmlobj):
		tmpdict={}
		for elem in xmlobj:
			if len(elem):
				tmpdict[elem.tag]= WxRequest._parse(elem)
			else:
				tmpdict[elem.tag]= elem.text
		return tmpdict

	def __getitem__(self, keystr):
		i=self.argdict
		for key in keystr.rsplit('.'):
			i=i[key]
		return i

	def __setitem__(self, key, value):
		self.argdict[key]= value

	def __getattr__(self, key):
		return self.argdict[key]

	def reply(self, msgtype, msgarg, stared= False):
		if msgtype== 'raw':
#			print('Using raw mode.')
			return WxResponse(dict(msgarg,**WxResponse.api['common'](self)), stared= stared)
		else:
			return WxResponse(dict(WxResponse.api['common'](self),**WxResponse.api[msgtype](msgarg)), stared= stared)

class WxResponse(object):
#	"""docstring for WxResponse"""
	api={
		'text': lambda x: {'Content':x,'MsgType':'text'},
		'news': lambda x: {'Articles': [dict(zip(('Title','Description','PicUrl','Url'),t)) for t in x ],'ArticleCount': len(x),'MsgType':'news'},
		'music': lambda x: dict(zip(('Title','Description','MusicUrl','HQMusicUrl'),x),MsgType='music') ,
		'common': lambda x: {'ToUserName': x['FromUserName'],'FromUserName':x['ToUserName'],'CreateTime':int(time()),'FuncFlag':0},

	}

	def __init__(self, argd, caller=None, stared= False):
#		super(WxResponse, self).__init__()
		self.argd= argd
		self.type= argd['MsgType']
		self.caller= None
		if stared:
			self.star()
#		self.pass_to= None

	def __getitem__(self, key):
		return self.argd[key]
	def __setitem__(self, key, value):
		self.argd[key]= value
		
	def star(self):
		self.argd['FuncFlag']=1
		return self

	def setCaller(self,caller):
		self.caller=caller
		return self
#
#
#	def _autofill(self):
#		self.argdict[]
		

class WxAuth(object):
	"""docstring for WxAuth"""
	_check = lambda argd: argd['signature']==sha1(''.join(sorted([argd['token'],argd['timestamp'],argd['nonce']])).encode()).hexdigest()
	_sendback = lambda argd: argd['echostr']

	def __init__(self, arg, **additional):  #You should always give a token='xxxx' pram !
#		super(WxAuth, self).__init__()
		self.arg = arg
		self.arg.update(additional)
		self.ok= bool(WxAuth._check(self.arg))

	def __bool__(self):
		return self.ok

	def reply(self):
		if self.ok:
			return WxAuth._sendback(self.arg)
		else:
			return 'FUCK YOU'
		