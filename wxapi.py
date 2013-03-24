from hashlib import sha1

auth = {
	'incoming' : [
		'signature',
		'timestamp',
		'nonce',
		'echostr', 
	],

	'localconfig': [
		'token',
	],
	
	'check' : (lambda tpl: tpl[0]==sha1(''.join(sorted([tpl[1],tpl[2],tpl[3]])).encode()).hexdigest(), ('signature','timestamp','nonce','token') ),
	'sendback' : (lambda tpl: tpl[0], ('echostr',)),

}

#request = {
#	'text': [
#		('ToUserName', True, False),
#		('FromUserName', True, False),
#		('CreateTime', None, False),
#		('MsgType', True, False),
#		('Content', True, False),
#		('MsgId', None, False),
#	],
#
#	'image': [
#		('ToUserName', True, False),
#		('FromUserName', True, False),
#		('CreateTime', None)
#		('MsgType', True, False),
#		('PicUrl', True, False),
#		('MsgId', None, False),
#	],
#
#	'location': [
#		('ToUserName', None, False),
#		('FromUserName', None, False),
#		('CreateTime', None, False),
#		('MsgType', None, False),
#		('Location_X', None, False),
#		('Location_Y', None, False),
#		('Scale', None, False),
#		('Lable', None, False),
#		('MsgId', None, False),
#	],
#
#	'link': [
#		('ToUserName', None, False),
#		('FromUserName', None, False),
#		('CreateTime', None, False),
#		('MsgType', None, False),
#		('Title', None, False),
#		('Description', None, False),
#		('Url', None, False),
#		('MsgId', None, False),
#	],
#
#	'event': [
#		('ToUserName', None, False),
#		('FromUserName', None, False),
#		('CreateTime', None, False),
#		('MsgType', None, False),
#		('Event', None, False),
#		('Latitude', None, False),
#		('Longitude', None, False),
#		('Precision', None, False),
#	],
#
#}
#
#responses = {
#	'text': [
#		('ToUserName', None, False),
#		('FromUserName', None, False),
#		('CreateTime', None, False),
#		('MsgType', None, False),
#		('Content', None, False),
#		('FuncFlag', None, False),
#	],
#
#	'music': [
#		('ToUserName', None, False),
#		('FromUserName', None, False),
#		('CreateTime', None, False),
#		('MsgType', None, False),
#		('Music', [
#			('Title', None, False),
#			('Description', None, False),
#			('MusicUrl', None, False),
#			('HQMusicUrl', None, False),
#		],False),
#		('FuncFlag', None, False),
#	],
#
#	'news': [
#		('ToUserName', None, False),
#		('FromUserName', None, False),
#		('CreateTime', None, False),
#		('MsgType', None, False),
#		('ArticleCount', None, False),
#		('Articles', [
#			('item', [
#				('Title', None, False),
#				('Description', None, False),
#				('PicUrl', None, False),
#				('Url', None, False),
#			], True),
#		], False),
#		('FuncFlag', None, False),
#	],
#}
#
#autosetter= {
#	'text': (
#
#		)
#}
#
#hubfunc= lambda x: print('Oh shit')