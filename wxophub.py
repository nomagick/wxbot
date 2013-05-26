import wxoperator
import wxopplugins

import ibeidou
import wxparrot

beidoutags= ibeidou.BeidouTags()
beidoulocation= ibeidou.BeidouLocation()
beidoubookclub= ibeidou.BeidouBookClub()
parrot= wxparrot.Parrot()

initdata=[
	{
		'id': 'main',
		'name': '北斗微信君',
		'route':{
			'数据同步': 'admin_dbsync',
			'1': 'search',
			'关键词': 'search',
			'关键字': 'search',
			'搜索': 'search',
			'2': 'bookclub',
			'北斗读书会': 'bookclub',
			'读书会': 'bookclub',
			'3': 'location',
			'身边的北斗人': 'location',
			'9': 'about',
			'关于北斗': 'about',
			'留言': 'about',
		},
		'help': '北斗微信主菜单:\n1 关键词 搜索\n2 北斗读书会\n3 身边的北斗人\n9 关于北斗\nhttp://ibeidou.net',
		'app': parrot,
	},
	{
		'id':'teach',
		'help':'Teach the parrot what to say.\nFormat: key => value .',
		'app': parrot.wx_teach_text,
	},
	{
		'id': 'dbsync',
		'help': '与主站数据库同步，请输入暗号。',
		'app': (lambda req: req.reply('text',(beidoutags.sync() or 'OK')) if (req['Content'] == 'λ') else req.reply('text','输错了老湿..'))
	},
	{
		'id': 'search',
		'name': '北斗网分类/tag搜索',
		'help': '北斗网分类/关键词搜索:\n请直接回复分类关键词进行文章搜索.\n例如: 最新发布',
		'app' : beidoutags.wx_query,
	},
	{
		'id': 'about',
		'name': '关于北斗网',
		'help': '关于北斗网:\n回复任意字符即可查看.',
		'app' : lambda req: req.reply('news',[('ibeidou.net','北斗网（ibeidou.net），是一个面向中国青年的人文类原创性思想平台和生活门户，服务于青年的自我启蒙和人文生活，由全国青年大学生自发管理运作，坚持纯公益、志愿性原则。北斗网以“网络、人文、新生活”为主题，着力探讨当代中国青年对人文思想的追求和对转型社会的责任。','http://d364qxkgeys5n0.cloudfront.net/wp-content/uploads/2009/02/guestbook.jpg','http://ibeidou.net/guestbook')]) ,
	},
	{
		'id': 'location',
		'name': '距离最近的北斗人/读者',
		'help': '距离最近的北斗人/读者:\n1 设置个人简介\n2 找读者\n3 找北斗人\n 第一次使用请先回复 1 或 个人简介 进行个人资料设置，之后才可以回复定位消息进行查找。',
		'app': beidoulocation.wx_query,
	},
	{
		'id': 'bookclub',
		'name':'北斗线上读书会',
		'help': '北斗线上读书会\n回复数字(第n期,n>=8)、题目或关键词收听读书会录音。\n读书会持续数小时,做好心理准备,走3G流量的同学们就别点开了。',
		'app': beidoubookclub.wx_query,
	},

]

default= wxoperator.RootOperator([wxoperator.Operator(x) for x in initdata])
default.plugin(wxopplugins.pre_convert_event,timetorun='pre',coremode=False)
default.plugin(wxopplugins.mid_route,timetorun='mid',coremode=True)
default.plugin(wxopplugins.mid_reserved_words,timetorun='mid',coremode=True)
default.plugin(wxopplugins.mid_pseudo_shell,timetorun='mid',coremode=True)
default.plugin(wxopplugins.post_add_reminder,timetorun='post',coremode=True)

appfunc=default

