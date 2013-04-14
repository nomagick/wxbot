def pre_convert_event(wxreq):
	if wxreq['MsgType'] == 'event':
		wxreq['MsgType']= 'text'
		wxreq['Content']= 'help'
	return wxreq

def post_add_reminder(wxres):
	if wxres['MsgType']== 'text':
		wxres['Content']= wxres['Content']+'\n--------\nhelp 查看帮助信息\nmenu 回到主菜单'
	return wxres
