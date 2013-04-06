#from your.module import your.app
import ibeidou

beidouapp= ibeidou.Wpapp()

def hubfunc(wxreq):
	try:
		tmplist= beidouapp.wx_query(wxreq['content'])
	except Exception as e:
		return ('text',{'TooUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'],'Content': str(e) ,'FuncFlag': 1,})
	if not tmplist:
		return ('text',{'TooUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'],'Content': 'No such keyword. =_=||' ,'FuncFlag': 0,})
	else:
		return ('news',{'TooUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'],'Articles': tmplist ,'FuncFlag': 0,})