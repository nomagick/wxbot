#from your.module import your.app


def hubfunc(wxreq):
	rstype= 'text'
	rsdata= {
		'to': wxreq['FromUserName'],
		'from': wxreq['ToUserName'],
		'content': 'miao//喵',
		'flag': 0,
	}


	return (rstype,rsdata)