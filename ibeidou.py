import mysql.connector as sdb
from pymongo import MongoClient as ndb
#import datetime

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
	'picurl': lambda x: 'http://cdn.ibeidou.net/wp-content/uploads/'+x if x else 'http://cdn.ibeidou.net/wp-content/uploads/2012/12/logo.jpg' ,
	'posturl': lambda x: 'http://cdn.ibeidou.net/archives/'+str(x) if x else 'http://ibeidou.net/',
	'description': lambda x,y: x if x else y if y else ' 生而不易  愿同摘星 ',
	'max_sync_buff': 10000,
	'max_cached_posts': 10,
	'default_return_posts': 3,
}

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

	def init_ndb(self):
		self.resource['n_conn']= ndb(self.conf['n']['hostname'], self.conf['n']['port'])
		self.resource['n_db']= self.resource['n_conn']['ibeidou']
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
			(wp_posts.post_status = 'publish' AND wp_posts.post_type =  'post' )
			{}\
			ORDER BY wp_posts.post_date_gmt DESC;'''
		modes={
			'full': '{}',
			'custom': 'AND {}',
			'keyword': 'AND wp_Terms.name = \'{}\'',
			'post': 'AND wp_posts.id = \'{}\'',
			'later': 'AND wp_posts.post_date_gmt >= {}',
			'greater': 'AND wp_posts.id > {}',
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
			for pid in sorted(tmpkw['posts'], reverse=True)[:self.conf['v']['max_cached_posts']]:
				tmppost= self.resource['n_posts'].find_one({'_id': pid})
				if not tmppost:
					raise KeyError('WTF! Post doesn\'t exist!')
				try:
					self.nlive[keyword].append(tmppost)
				except:
					self.nlive[keyword]= [tmppost,]
		for kw,plist in self.nlive.items():
			self.resource['n_live'].update({'_id':kw}, {'$set':{'Articles':plist}}, True)

	def sync(self, mode='full', arg=''):
		self.fetch_from_sql(mode,arg)
		self.merge_to_nosql()
		self.mk_live_cache()

	def query(self, kw):
		cached= self.resource['n_live'].find_one({'_id':kw})
		if not cached:
			return None
		else:
			return cached['Articles'][:self.conf['v']['default_return_posts']]
		
	def wx_query(self, wxreq):
		try:
			tmplist= self.query(wxreq['Content'])
		except :
			return {'TooUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'text', 'Content': '真不好意思，服务器给您跪了，可能您的调戏方式不对，请重新调戏或直接访问北斗网  http://ibeidou.net' ,'FuncFlag': 1,}
		if not tmplist: 
			return {'TooUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'text', 'Content': '真不好意思，这个关键词没有对应内容，请换个关键词或直接访问北斗网    http://ibeidou.net' ,'FuncFlag': 0,}
		else: 
			return {'TooUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'news', 'Articles': tmplist ,'FuncFlag': 0,}
	
