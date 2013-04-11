import ibeidou

beidoutags= ibeidou.BeidouTags()

operators=[
	{
		'id': 'main',
		'redirect':[
			({'skykingcovergroundtiger'}, 'admin'),
			({'1', '关键词', '关键字', '搜索',}, 'search'),
			({'2', '活动',}, 'event'),
			({'3', '调戏',}, 'simsim'),
			({'9', '关于北斗','留言',}, 'about'),
		],
		'help': '',
		'app': lambda req: {'TooUserName': req['FromUserName'],'FromUserName': req['ToUserName'],'Content': '北斗微信主菜单:\n1. 关键词 搜索\n2. 活动\n 3. 调戏\n9. 关于北斗\nhttp://ibeidou.net' ,'FuncFlag': 0,} ,
	},
	{
		'id': 'search',
		'help': '北斗网分类/关键词搜索:\n请直接回复关键词进行文章搜索.',
		'app' : beidoutags.wx_query,
	},
	{
		'id': 'about',
		'help': '关于北斗网:\n回复任意字符即可查看.',
		'app' : lambda x: beidoutags.query('about') ,
	},
	{
		'id': 'location',
		'help': '离我最近的北斗人:\n请回复您的地理位置.',
		'app': lambda req: {'TooUserName': req['FromUserName'],'FromUserName': req['ToUserName'],'Content': '喵！' ,'FuncFlag': 0,} ,
	},

]

class Operator(object):
	"""docstring for Operator"""
	def __init__(self, cfgd):
		super(Operator, self).__init__()
		self.cfgd= cfgd
		if 'help' not in self.cfgd:
			self.cfgd.update({'help':'Help information not provided'})
		if 'app' not in self.cfgd:
			self.cfgd.update({'app': lambda wxreq: {'TooUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'text', 'Content': 'App not provided.' ,'FuncFlag': 1,}})
		
	def __getattr__(key):
		try :
			return self.cfgd[key]
		except :
			return None

	def answer(self, req):
		return self.cnfd['app'](req)

