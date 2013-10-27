from pymongo import MongoClient
from functools import partial
import wxopplugins

class MongoBasedApp(object):
	"""docstring for MongoBasedApp"""
	_dbcfg={
		'host': 'localhost',
		'port': 27017,
		'database': 'ibeidou',
		'username': '',
		'password': '',
		'collection': 'operator',
	}
	resources= {}
	def __init__(self, dbcfg= {}):
		super(MongoBasedApp, self).__init__()
		if dbcfg:
			self._dbcfg= dict(MongoBasedApp._dbcfg, **dbcfg)
		else:
			self._dbcfg= MongoBasedApp._dbcfg

	def _auth_db(self, uname= '', passwd= ''):
		if (uname and passwd):
			self._dbcfg['username']= uname
			self._dbcfg['password']= passwd
		else:
			pass

	def _init_db(self):
		self.resources['conn']= MongoClient(self._dbcfg['host'],self._dbcfg['port']) #connect to your mongodb
		self.resources['db']= self.resources['conn'][self._dbcfg['database']] #find your database
		if (self._dbcfg['username'] and self._dbcfg['password']):
			self.resources['db'].authenticate(self._dbcfg['username'], self._dbcfg['password']) #auth your database
		else:
			pass
		self.resources['coll']= self.resources['db'][self._dbcfg['collection']] #find your collection

dbcfg={
	'host': 'localhost',
	'port': 27017,
	'database': 'ibeidou',
	'username': '',
	'password': '',
	'collection': 'operator',
}
class RootOperator(MongoBasedApp):
	"""docstring for RootOperator"""
	def __init__(self, operators=[], debug=0, dbcfg= dbcfg):
		super(RootOperator, self).__init__(dbcfg)
		self.debuglevel= debug
		self.operators={}
		self.plugins_post=[]
		self.plugins_pre=[]
		self.plugins_mid=[self.runopfunc]
		self.init_db(dbcfg)
		for x in operators:
			self.register(x)
		self.plugin(wxopplugins.pre_convert_event,timetorun='pre',coremode=False)
		self.plugin(wxopplugins.mid_route,timetorun='mid',coremode=True)
		self.plugin(wxopplugins.mid_reserved_words,timetorun='mid',coremode=True)
		self.plugin(wxopplugins.mid_pseudo_shell,timetorun='mid',coremode=True)
		self.plugin(wxopplugins.post_add_reminder,timetorun='post',coremode=True)

	def __getitem__(self,key):
		return self.operators[key]

	def debug(self, message, level=1):
		if level > self.debuglevel:
			print(message)
		
	def plugin(self, pluginfunc, timetorun='post', coremode=False):
		if coremode:
			pluginfunc= partial(pluginfunc,self)
		else:
			pass
		if timetorun == 'post':
			self.plugins_post.append(pluginfunc)
		elif timetorun == 'pre':
			self.plugins_pre.append(pluginfunc)
		else :
			self.plugins_mid.insert(-1,pluginfunc)

	def init_db(self,dbcfg):
		self.debug('About to init Mongodb.')
		self._init_db()

	def register(self, operator):
		self.debug('About to register operator '+ operator.id)
		self.operators[operator.id]= operator
 
	def init_request(self, request):
		try:
			request.curoperator= self.resources['coll'].find_one({'_id':request['FromUserName']}, {'operator':1})['operator']
		except (TypeError, KeyError):
			request.curoperator= None
		finally:
			return request

	def runopfunc(self, request):
		return self.operators[request.curoperator](request)

	def transfer(self, user, target):
		self.resources['coll'].update({'_id':user},{'$set':{'operator':target}}, True)
		return self.operators[target].help

	def pre_answer(self,request):
		reply= request
		for func in self.plugins_pre:
			reply= func(reply)
		return reply

	def answer(self, request):
		for func in self.plugins_mid:
			result= func(request)
			if result:
				return result
			else:
				continue
		return request.reply('text','虽然不知道为什么，但是您的回复击穿了整个处理系统，我真的不知道该回复您什么。。\n说点别的吧。。', stared= True)

	def post_answer(self, response):
		reply= response
		for func in self.plugins_post:
			reply= func(reply)
		return reply


	def __call__(self,request):
		return self.post_answer(self.answer(self.pre_answer(self.init_request(request))))


class Operator(object):
	"""docstring for Operator"""
	cfgd= {
		'help': 'DEBUG: Help information not provided.',
		'app': lambda wxreq: wxreq.reply('text','DEBUG: Custom app not provided.'),
	}
	
	def __init__(self, argd):
		if 'id' not in argd:
			raise KeyError('id')
		super(Operator, self).__init__()
		self.cfgd= dict(Operator.cfgd,**argd)
	
	def __getattr__(self, key):
		try :
			return self.cfgd[key]
		except KeyError:
			return None

	def __call__(self, req):
		tmp=self.cfgd['app'](req)
		if tmp:
			tmp.caller= self.id
		return tmp

