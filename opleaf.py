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
		'help': '北斗微信主菜单:\n1. 关键词 搜索\n2. 活动\n3. 调戏\n9. 关于北斗\nhttp://ibeidou.net',
		'app': lambda req: {'ToUserName': req['FromUserName'],'FromUserName': req['ToUserName'], 'MsgType':'text', 'Content': '您刚才输入的内容未能被识别，请输入帮助信息中出现的内容.' ,'FuncFlag': 0,} ,
	},
	{
		'id': 'search',
		'help': '北斗网分类/关键词搜索:\n请直接回复关键词进行文章搜索.',
		'app' : beidoutags.wx_query,
	},
	{
		'id': 'about',
		'help': '关于北斗网:\n回复任意字符即可查看.',
		'app' : lambda req: {'ToUserName': req['FromUserName'],'FromUserName': req['ToUserName'], 'MsgType': 'news', 'Articles': [{'Title':'ibeidou.net', 'Url':'http://ibeidou.net/guestbook', 'PicUrl': 'http://d364qxkgeys5n0.cloudfront.net/wp-content/uploads/2009/02/guestbook.jpg', 'Description': '北斗网（ibeidou.net），是一个面向中国青年的人文类原创性思想平台和生活门户，服务于青年的自我启蒙和人文生活，由全国青年大学生自发管理运作，坚持纯公益、志愿性原则。北斗网以“网络、人文、新生活”为主题，着力探讨当代中国青年对人文思想的追求和对转型社会的责任。'}] ,'FuncFlag': 0,} ,
	},
	{
		'id': 'location',
		'help': '离我最近的北斗人:\n请回复您的地理位置.',
		'app': lambda req: {'ToUserName': req['FromUserName'],'FromUserName': req['ToUserName'], 'MsgType':'text', 'Content': '喵！' ,'FuncFlag': 0,} ,
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
			self.cfgd.update({'app': lambda wxreq: {'ToUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'text', 'Content': 'App not provided.' ,'FuncFlag': 1,}})
		
	def __getattr__(self, key):
		try :
			return self.cfgd[key]
		except :
			return None

	def answer(self, req):
		return self.cfgd['app'](req)

operators= [Operator(x) for x in operators]