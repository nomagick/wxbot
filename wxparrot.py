from pymongo import MongoClient
from random import choice

dbcfg={
	'host': 'localhost',
	'port': 27017,
	'database': 'ibeidou',
	'collection': 'parrot',
}


class Parrot(object):
	"""docstring for Parrot"""
	def __init__(self, dbcfg=dbcfg):
		super(Parrot, self).__init__()
		self.resources={}
		self.init_db(dbcfg)

	def init_db(self,dbcfg):
		self.resources['conn']= MongoClient(dbcfg['host'],dbcfg['port']) #connect to your mongodb
		self.resources['db']= self.resources['conn'][dbcfg['database']] #find your database
		self.resources['coll']= self.resources['db'][dbcfg['collection']] #find your collection

	def query(self,qstr):
		try: 
			return choice(self.resources['coll'].find_one({'_id':qstr})['answers'])
		except:
			return None

	def insert(self,key,msgd):
		self.resources['coll'].update({'_id':key},{'$addToSet':{'answers':msgd}},True)

	def wx_query(self,wxreq):
		try:
			return wxreq.reply('raw',self.query(wxreq['Content']))
		except :
			tmpres= wxreq.reply('text','您的回复没有自动应答。\n系统已经将您的回复标记，稍后将会由人类处理。')
			tmpres.star()
			return tmpres

	def wx_teach_text(self,wxreq):
		pair= wxreq['Content'].partition('=>')
		if not (pair[0] and pair[2]):
			return wxreq.reply('text','Invalid.')
		self.insert(pair[0].strip(),{'MsgType':'text','Content':pair[2].strip()})
		return wxreq.reply('text',pair[0] + ' => ' + pair[2] + '\nOK.')

	def __call__(self,wxreq):
		return self.wx_query(wxreq)