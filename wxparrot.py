from pymongo import MongoClient
from wxoperator import MongoBasedApp
from random import choice

dbcfg={
#	'host': 'localhost',
#	'port': 27017,
#	'database': 'ibeidou',
#	'username': '',
#	'password': '',
	'collection': 'parrot',
}


class Parrot(MongoBasedApp):
	"""docstring for Parrot"""
	def __init__(self, dbcfg=dbcfg):
		super(Parrot, self).__init__(dbcfg)
		self._init_db()

	def query(self,qstr):
		try: 
			return choice(self.resources['coll'].find_one({'_id':qstr})['answers'])
		except (TypeError, KeyError):
			return None

	def insert(self,key,msgd):
		self.resources['coll'].update({'_id':key},{'$addToSet':{'answers':msgd}},True)

	def wx_query(self,wxreq):
		try:
			return wxreq.reply('raw',self.query(wxreq['Content']))
		except TypeError:
			tmpres= wxreq.reply('text','您的回复没有自动应答。\n系统已经将您的回复标记，稍后将会由人类处理。', stared= True)
			return tmpres

	def wx_teach_text(self,wxreq):
		pair= wxreq['Content'].partition('=>')
		if not (pair[0] and pair[2]):
			return wxreq.reply('text','Invalid.')
		self.insert(pair[0].strip(),{'MsgType':'text','Content':pair[2].strip()})
		return wxreq.reply('text',pair[0] + ' => ' + pair[2] + '\nOK.')

	def __call__(self,wxreq):
		return self.wx_query(wxreq)