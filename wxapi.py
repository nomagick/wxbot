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
	
	'check' : (lambda tpl : tpl[0]==sha1(''.join(sorted([tpl[1],tpl[2],tpl[4]])).encode()).hexdigest(), ('signature','timestamp','nonce','token') ),
	'sendback' : (lambda tpl : tpl[0] , ('echostr')),

}

request = {
	'text': [
		('ToUserName', True),
		('FromUserName', True),
		('CreateTime', None),
		('MsgType', True),
		('Content', True),
		('MsgId', None),
	],

	'image': [
		('ToUserName', True),
		('FromUserName', True),
		('CreateTime', None)
		('MsgType', True),
		('PicUrl', True),
		('MsgId', None),
	],

	'location': [
		('ToUserName', None),
		('FromUserName', None),
		('CreateTime', None),
		('MsgType', None),
		('Location_X', None),
		('Location_Y', None),
		('Scale', None),
		('Lable', None),
		('MsgId', None),
	],

	'link': [
		('ToUserName', None),
		('FromUserName', None),
		('CreateTime', None),
		('MsgType', None),
		('Title', None),
		('Description', None),
		('Url', None),
		('MsgId', None),
	],

	'event': [
		('ToUserName', None),
		('FromUserName', None),
		('CreateTime', None),
		('MsgType', None),
		('Event', None),
		('Latitude', None),
		('Longitude', None),
		('Precision', None),
	],

}

response = {
	'text': [
		('ToUserName', None),
		('FromUserName', None),
		('CreateTime', None),
		('MsgType', None),
		('Content', None),
		('FuncFlag', None),
	],

	'music': [
		('ToUserName', None),
		('FromUserName', None),
		('CreateTime', None),
		('MsgType', None),
		('Music', [
			('Title', None),
			('Description', None),
			('MusicUrl', None),
			('HQMusicUrl', None),
		]),
		('FuncFlag', None),
	],

	'hybrid': [
		('ToUserName', None),
		('FromUserName', None),
		('CreateTime', None),
		('MsgType', None),
		('ArticleCount', None),
		('Articles', [
			('item', [
				('Title', None),
				('Description', None),
				('PicUrl', None),
				('Url', None),
			]),
		]),
		('FuncFlag', None),
	],
}