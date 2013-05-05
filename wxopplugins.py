#	A Pre answer plugin takes a wxclass.WxRequest object and should also return a wxclass.WxRequest object.
def pre_convert_event(wxreq):
	if wxreq['MsgType'] == 'event':
		wxreq['MsgType']= 'text'
		wxreq['Content']= 'help'
	return wxreq

#	A Post answer plugin takes a wxclass.WxResponse object and should also return a wxclass.WxResponse object.
def post_add_reminder(wxres):
	if wxres['MsgType']== 'text':
		wxres['Content']= wxres['Content']+'\n--------\nhelp 查看帮助信息\nmenu 回到主菜单'
	return wxres

#	A Mid answer plugin takes a wxclass.WxRequest object and should return either a wxclass.WxResponse object or None.
#	A COREMOOD plugin takes the root operator instance as the first pram and the WxRequest/WxResponse object as the second pram.
def mid_route(rootop,wxreq):	#Default plugin, DO NOT REMOVE !!
	goto= None
	if not wxreq.curoperator:
		goto= 'main'
	else:
		try:
			goto= rootop.operators[wxreq.curoperator].route[wxreq['Content'].rstrip()]
		except:
			pass
	if goto:
		return wxreq.reply('text', rootop.transfer(wxreq['FromUserName'],goto))
	else:
		return None

evil_reservations={
	'menu': lambda op,req: req.reply('text',op.transfer(req['FromUserName'],'main')) ,
	'help': lambda op,req: req.reply('text',op.operators[req.curoperator].help),
}
def mid_reserved(rootop,wxreq):
	try:
		return evil_reservations[wxreq['Content'].rstrip()](rootop,wxreq)
	except:
		return None

