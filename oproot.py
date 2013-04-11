from pymongo import MongoClient



class RootOperator(object):
	"""docstring for RootOperator"""
	def __init__(self, **arg):
		super(RootOperator, self).__init__()
		self.operators={}
		self.resources=arg
		self.init_db()
		self.init_reserve()
		
	def init_db(self):
		self.resources['conn']= MongoClient('localhost',27017) #connect to your mongodb
		self.resources['db']= self.resources['conn']['ibeidou'] #find your database
		self.resources['coll']= self.resources['db']['operator'] #find your collection

	def register(self, operator):
		self.operators[operator.id]= operator
		self.init_redirect(operator)

	def init_redirect(self, operator):
		if not hasattr(operator,'redirect'):
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
 
	def redirect(self, request):
		goto= None
		try:
			current= self.resources['coll'].find_one({'_id':request['FromUserName']}, {'operator':1})['operator']
		except:
			goto= 'main'
		if current:
			try:
				goto= self.redirections[current][request['Content'].rstrip()]
			except:
				pass
		else:
			goto= 'main'
		if goto:
			self.resources['coll'].update({'_id':request['FromUserName']},{'$set':{'operator':goto}}, True)
			return {'ToUserName': request['FromUserName'], 'FromUserName': request['ToUserName'], 'MsgType': 'text', 'Content': self.operators[goto].help, 'FuncFlag': 0}
		else:
			return None

	def init_reserve(self):
		self.reservations={
			';': lambda x: self.operators['main'].help and self.resources['coll'].update({'_id':x['FromUserName']},{'$set':{'operator':'main'}}, True) ,
			'help': lambda x: self.operators[self.resources['coll'].find_one({'_id':request['FromUserName']}, {'operator':1})['operator']].help ,
		}
		
	def reserve(self, request):
		try:
			return self.reservations[request['Content']](request)
		except:
			return None