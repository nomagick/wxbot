from pymongo import MongoClient
from functools import partial




class RootOperator(object):
	"""docstring for RootOperator"""
	def __init__(self, operators=[], debug=0):
		super(RootOperator, self).__init__()
		self.debuglevel= debug
		self.operators={}
		self.resources={}
		self.plugins_post=[]
		self.plugins_pre=[]
		self.plugins_mid=[self.runopfunc]
		self.init_db()
		for x in operators:
			self.register(x)

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

	def init_db(self):
		self.debug('About to init Mongodb.')
		self.resources['conn']= MongoClient('localhost',27017) #connect to your mongodb
		self.resources['db']= self.resources['conn']['ibeidou'] #find your database
		self.resources['coll']= self.resources['db']['operator'] #find your collection

	def register(self, operator):
		self.debug('About register operator '+ operator.id)
		self.operators[operator.id]= operator
 
	def init_request(self, request):
		try:
			request.curoperator= self.resources['coll'].find_one({'_id':request['FromUserName']}, {'operator':1})['operator']
		except:
			request.curoperator= None
		finally:
			return request

	def runopfunc(self, request):
		return self.operators[request.curoperator](request)

	def transfer(self, user, target):
		self.resources['coll'].update({'_id':user},{'$set':{'operator':target}}, True)
		return self.operators[target].help

	def answer(self, request):
		for func in self.plugins_mid:
			result= func(request)
			if result:
				return result
			else:
				continue
		return request.reply('text','虽然不知道为什么，但是您的回复击穿了整个处理系统，我真的不知道该回复您什么。。\n说点别的吧。。')

	def post_answer(self, response):
		reply= response
		for func in self.plugins_post:
			reply= func(reply)
		return reply

	def pre_answer(self,request):
		reply= request
		for func in self.plugins_pre:
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
		super(Operator, self).__init__()
		self.cfgd= dict(Operator.cfgd,**argd)
	def __getattr__(self, key):
		try :
			return self.cfgd[key]
		except :
			return None

	def __call__(self, req):
		return self.cfgd['app'](req)

