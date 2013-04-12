from pymongo import MongoClient


class RootOperator(object):
	"""docstring for RootOperator"""
	def __init__(self, operators, debug=0):
		super(RootOperator, self).__init__()
		self.debuglevel= debug
		self.operators={}
		self.resources={}
		self.init_db()
		self.init_reserve()
		for x in operators:
			self.register(x)

	def debug(self, message, level=1):
		if level > self.debuglevel:
			print(message)
		
	def init_db(self):
		self.debug('About to init Mongodb.')
		self.resources['conn']= MongoClient('localhost',27017) #connect to your mongodb
		self.resources['db']= self.resources['conn']['ibeidou'] #find your database
		self.resources['coll']= self.resources['db']['operator'] #find your collection

	def register(self, operator):
		self.debug('About register operator '+ operator.id)
		self.operators[operator.id]= operator
		self.init_redirect(operator)

	def init_redirect(self, operator):
		if not operator.redirect:
			return None
		matchdict={}
		for pattern in operator.redirect:
			for word in pattern[0]:
				matchdict[word]= pattern[1]
		if (not matchdict):
			raise ValueError('illegal redirection information.')
		try:
			self.redirections[operator.id]= matchdict
		except AttributeError:
			self.redirections= {operator.id: matchdict,}
		finally:
			return True
 
	def init_request(self, request):
		try:
			request.curoperator= self.resources['coll'].find_one({'_id':request['FromUserName']}, {'operator':1})['operator']
		except:
			request.curoperator= None

	def customapp(self, request):
		return self.operators[request.curoperator].answer(request)

	def redirect(self, request):
		goto= None
		if not request.curoperator:
			goto= 'main'
		else:
			try:
				goto= self.redirections[request.curoperator][request['Content'].rstrip()]
			except:
				pass
		if goto:
			self.resources['coll'].update({'_id':request['FromUserName']},{'$set':{'operator':goto}}, True)
			return {'ToUserName': request['FromUserName'], 'FromUserName': request['ToUserName'], 'MsgType': 'text', 'Content': self.operators[goto].help, 'FuncFlag': 0}
		else:
			return None

	def init_reserve(self):
		self.reservations={
			';': lambda x: self.resources['coll'].update({'_id':x['FromUserName']},{'$set':{'operator':'main'}}, True) and self.operators['main'].help ,
			'help': lambda x: self.operators[self.resources['coll'].find_one({'_id':x['FromUserName']}, {'operator':1})['operator']].help ,
		}
		
	def reserve(self, request):
		try:
			return {'ToUserName': request['FromUserName'],'FromUserName': request['ToUserName'], 'MsgType':'text', 'Content': self.reservations[request['Content']](request) ,'FuncFlag': 0,}
		except:
			return None

	def answer(self, request):
		for func in [self.init_request, self.reserve, self.redirect, self.customapp]:
			result= func(request)
			if result:
				return result
			else:
				continue

