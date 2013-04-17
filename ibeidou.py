import mysql.connector as sdb
from pymongo import MongoClient as ndb
from time import time

SQLcfg= {
	'user': 'wxbot',
	'password': 'beidou7stars',
	'host': 'ibeidou.net',
	'database': 'ibeidoun_beidou',
}

NOSQLcfg= {
	'hostname': 'localhost',
	'database': 'ibeidou',
	'port': 27017,
	'user': '',
	'password': '',
}

SRVcfg= {
	'picurl': lambda x: 'http://cdn.ibeidou.net/wp-content/uploads/'+x if x else 'http://cdn.ibeidou.net/wp-content/uploads/2009/02/guestbook.jpg' ,
	'posturl': lambda x: 'http://ibeidou.net/archives/'+str(x) if x else 'http://ibeidou.net/',
	'description': lambda x,y: x if x else y if y else ' 生而不易  愿同摘星 ',
	'max_sync_buff': 10000,
	'max_cached_post': 10,
	'default_returned_post': 3,
}

_shared_ndb_connection= None

class BeidouTags(object):
	"""docstring for Wpdb"""
	def __init__(self, SQLconf= SQLcfg, NOSQLconf= NOSQLcfg, SRVconf=SRVcfg):
		super(BeidouTags, self).__init__()
		self.conf={}
		self.resource={}
		self.conf['s']= SQLconf
		self.conf['n']= NOSQLconf
		self.conf['v']= SRVconf
		self.init_ndb()
	
	def init_sdb(self):
		self.resource['s_conn']= sdb.connect(**self.conf['s'])
		self.resource['s_cursor']= self.resource['s_conn'].cursor(buffered=True)

	def destruct_sdb(self):
		try:
			self.resource['s_conn'].close()
			del self.resource['s_cursor']
			del self.resource['s_conn']
		except:
			pass


	def init_ndb(self):
		self.resource['n_conn']= ndb(self.conf['n']['hostname'], self.conf['n']['port'])
		self.resource['n_db']= self.resource['n_conn']['ibeidou']
		global _shared_ndb_connection
		if not _shared_ndb_connection:
			_shared_ndb_connection= self.resource['n_conn']
		self.resource['n_live']= self.resource['n_db']['live']
		self.resource['n_posts']= self.resource['n_db']['posts']
		self.resource['n_keywords']= self.resource['n_db']['keywords']

	def fetch_from_sql(self, mode, arg=''):
		try: 
			self.resource['s_conn']
		except:
			self.init_sdb()
		sqlstr= '''\
			SELECT wp_terms.name as Keyword, wp_posts.id as Id, wp_posts.post_title as Title, pic.meta_value as Pic, txt.meta_value as Description, wp_posts.post_excerpt as OldDescription
			FROM 
			wp_posts
			INNER JOIN wp_term_relationships ON wp_posts.id = wp_term_relationships.object_id
			INNER JOIN wp_term_taxonomy ON wp_term_relationships.term_taxonomy_id = wp_term_taxonomy.term_taxonomy_id
			INNER JOIN wp_terms ON wp_term_taxonomy.term_id = wp_terms.term_id
			LEFT JOIN wp_postmeta as pic ON pic.post_id = wp_posts.id AND pic.meta_key = 'newheadarticleimage' 
			LEFT JOIN wp_postmeta as txt ON txt.post_id = wp_posts.id AND txt.meta_key = 'featuredtext'
			WHERE
			(wp_posts.post_status = 'publish' AND (wp_posts.post_type = 'post' OR wp_posts.post_type= 'page'))
			{}\
			ORDER BY wp_posts.post_date_gmt DESC;'''
		modes={
			'full': '{}',
			'custom': 'AND {}',
			'keyword': 'AND wp_Terms.name = \'{}\'',
			'post': 'AND wp_posts.id = \'{}\'',
			'later': 'AND wp_posts.post_date_gmt >= {}',
			'greater': 'AND wp_posts.id > {}',
			'last_week': 'AND wp_posts.post_date_gmt >= FROM_UNIXTIME('+str(int(time())-3600*24*7)+')'
		}
		self.nposts= {}
		self.nkeywords= {}

		scursor= self.resource['s_cursor']

		finalsql= sqlstr.format(modes[mode].format(arg))

		scursor.execute(finalsql)
		for (kw, postid, title, picuri, description, olddescription) in scursor:
			for keyword in kw.split('·')[0].split('，'):
				keyword = keyword.strip('《》【】')
				keyword = keyword.rstrip('123')
				if not keyword:
					continue
				if keyword in self.nkeywords:
					self.nkeywords[keyword].add(postid)
				else:
					self.nkeywords[keyword]={postid,}

				if postid in self.nposts:
					pass
				else:
					self.nposts[postid]= {
						'_id':postid ,
						'Title':title,
						'PicUrl':self.conf['v']['picurl'](picuri),
						'Url':self.conf['v']['posturl'](postid),
						'Description': self.conf['v']['description'](description, olddescription),
					}
		for item in self.nkeywords:
			self.nkeywords[item]= sorted(list(self.nkeywords[item]), reverse=True)
		self.destruct_sdb()
#		self.merge_to_nosql()

	def merge_to_nosql(self):
		for name,content in self.nposts.items():
			self.resource['n_posts'].update({'_id':name}, content, True)
		for name,content in self.nkeywords.items():
			self.resource['n_keywords'].update({'_id':name}, {'$addToSet':{'posts':{'$each':content}}}, True)
		del(self.nposts)
		self.nposts={}

	def mk_live_cache(self):
		self.nlive= {}
		tmpkw= None
		tmppost= None
		for keyword in self.nkeywords:
			tmpkw= self.resource['n_keywords'].find_one({'_id':keyword})
			for pid in sorted(tmpkw['posts'], reverse=True)[:self.conf['v']['max_cached_post']]:
				tmppost= self.resource['n_posts'].find_one({'_id': pid})
				if not tmppost:
					raise KeyError('WTF! Post doesn\'t exist!')
				try:
					self.nlive[keyword].append(tmppost)
				except:
					self.nlive[keyword]= [tmppost,]
		for kw,plist in self.nlive.items():
			self.resource['n_live'].update({'_id':kw}, {'$set':{'Articles':plist}}, True)

	def sync(self, mode='last_week', arg=''):
		self.fetch_from_sql(mode,arg)
		self.merge_to_nosql()
		self.mk_live_cache()

	def query(self, kw):
		cached= self.resource['n_live'].find_one({'_id':kw})
		if not cached:
			return None
		else:
			return cached['Articles'][:self.conf['v']['default_returned_post']]
		
	def wx_query(self, wxreq):
		try:
			tmplist= self.query(wxreq['Content'])
		except :
			return {'ToUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'text', 'Content': '真不好意思，服务器给您跪了，可能您的调戏方式不对，请重新调戏或直接访问北斗网  http://ibeidou.net' ,'FuncFlag': 1,}
		if not tmplist: 
			return {'ToUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'text', 'Content': '真不好意思，这个关键词没有对应内容，但是您可以<a href=\"http://ibeidou.net/?s='+wxreq['Content']+'\">直接在北斗网上搜索「'+wxreq['Content']+'」</a>或访问北斗网主页\nhttp://ibeidou.net' ,'FuncFlag': 0,}
		else: 
			return {'ToUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'news', 'Articles': tmplist ,'FuncFlag': 0,}
	
class BeidouLocation(object):
	"""docstring for BeidouLocation"""
	def __init__(self, dbconf=NOSQLcfg, ):
		super(BeidouLocation, self).__init__()
		self.conf={}
		self.resource={}
		global _shared_ndb_connection
		if _shared_ndb_connection:
			self.resource['conn']= _shared_ndb_connection
		else:
			self.resource['conn']= ndb(dbconf['hostname'], dbconf['n']['port'])
			_shared_ndb_connection= self.resource['conn']
		self.resource['db']= self.resource['conn']['ibeidou']
		self.resource['coll']= self.resource['db']['location']

		self.resource['coll'].ensure_index([('location', '2dsphere'), ('identity', 1)])

		self.menu= [
			({'1','设置简介', '个人简介','设置介绍','自我介绍','设置资料'},'set_profile','请回复一条文本消息作为您的自我介绍\n至少要包含您的名字.\n如果您想让其他用户加您好友那么请包含相应联系方式，比如微信号什么的.\n这条消息中的所有内容都将在您被搜索到的时候展示给其他用户。'),
			({'愿同坠地'},'set_volunteer','哎呦..[好像有什么东西碎了一地]\n现在随便回复点什么，系统会记下你是北斗人。'),
			({'2','读者'},'query_reader','已经切换为寻找最近的读者。请回复您的位置信息。'),
			({'3','北斗人','志愿者'},'query_volunteer','已经切换为寻找最近的北斗志愿者。请回复您的位置信息。'),
		]

		self.behavior_table= {}
		for x in self.menu:
			for y in x[0]:
				self.behavior_table[y]= self.menu.index(x)


	def set_profile(self, wxreq):
		try:
			self.resource['coll'].update({'_id': wxreq['FromUserName']}, {'$set':{'profile': wxreq['Content'], 'behavior':'query_volunteer', 'identity':'reader'}}, True)
			return '个人简介设置完成，您现在可以回复位置信息。'
		except:
			return None
	def set_location(self, wxreq):
		try:
			return self.resource['coll'].update({'_id': wxreq['FromUserName']}, {'$set':{'location': {'type': 'Point', 'coordinates': [float(wxreq['Location_Y']), float(wxreq['Location_X'])]}, 'label': wxreq['Label'], 'time': int(time())}}, True)
		except KeyError:
			return None

	def change_behavior(self, wxreq):
		try:
			menuindex= self.behavior_table[wxreq['Content']]
			behavior= self.menu[menuindex][1]
			succmsg= self.menu[menuindex][2]
		except KeyError:
			return None
		try:
			self.resource['coll'].update({'_id': wxreq['FromUserName']}, {'$set':{'behavior': behavior}}, True)
			return succmsg
		except:
			raise RuntimeError('Behavior changeing failed')

	def set_volunteer(self, wxreq):
		self.resource['coll'].update({'_id': wxreq['FromUserName']}, {'$set':{'identity': 'volunteer', 'behavior':'query_volunteer'}}, True)
		return 'OK'

	def query_reader(self, wxreq):
		self.set_location(wxreq)
		try:
			result=[x for x in self.resource['coll'].find({'location':{'$near': {'$geometry': {'type': 'Point', 'coordinates': [float(wxreq['Location_Y']), float(wxreq['Location_X'])]}}}, 'identity':'reader'}).limit(2)] 
			theone= result[0] if result[0]['_id'] != wxreq['FromUserName'] else result[1]
			return '离您最近的北斗读者\n'+theone['profile']+'\n'+str(round((time()-theone['time'])/3600, 1))+'小时前的位置在<a href=\"http://ditu.google.cn/maps?ll='+str(theone['location']['coordinates'][1])+','+str(theone['location']['coordinates'][0])+'&spn=0.1,0.1&t=k&hl=cn\">这里</a>\n'+theone['label']
		except KeyError:
			return None
		except IndexError:
			return None

	def query_volunteer(self, wxreq):
		self.set_location(wxreq)
		try:
			result=[x for x in self.resource['coll'].find({'location':{'$near': {'$geometry': {'type': 'Point', 'coordinates': [float(wxreq['Location_Y']), float(wxreq['Location_X'])]}}}, 'identity':'volunteer'}).limit(2)] 
			theone= result[0] if result[0]['_id'] != wxreq['FromUserName'] else result[1]
			return '离您最近的北斗志愿者\n'+theone['profile']+'\n'+str(round((time()-theone['time'])/3600, 1))+'小时前的位置在<a href=\"http://ditu.google.cn/maps?ll='+str(theone['location']['coordinates'][1])+','+str(theone['location']['coordinates'][0])+'&spn=0.1,0.1&t=k&hl=cn\"">这里</a>\n'+theone['label']
		except KeyError:
			return None
		except IndexError:
			return None
	
	def answer(self, wxreq):
		result= self.change_behavior(wxreq)
		if result:
			return {'FromUserName':wxreq['ToUserName'], 'ToUserName':wxreq['FromUserName'], 'MsgType':'text', 'Content': result, 'FuncFlag':0}
		try:
			behavior= self.resource['coll'].find_one({'_id': wxreq['FromUserName']}, {'behavior':1})['behavior']
		except:
			return {'FromUserName':wxreq['ToUserName'], 'ToUserName':wxreq['FromUserName'], 'MsgType':'text', 'Content': '请您先回复 设置资料 完善您的个人资料后再进行其他操作', 'FuncFlag':0}

		result= getattr(self, behavior)(wxreq)
		if not result:
			result= '出问题了..=_=||\n请确保您已经完善了您的个人信息，之后严格按照帮助信息的内容进行操作。\n所谓位置信息是指微信提供的定位信息，请先选择回复框左侧加号状物体，再在弹出的众多方框中选择 位置 二字上方的方框。'
		return {'FromUserName':wxreq['ToUserName'], 'ToUserName':wxreq['FromUserName'], 'MsgType':'text', 'Content': result, 'FuncFlag':0}
