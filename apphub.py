#from your.module import your.app
import ibeidou

beidouapp= ibeidou.Wpapp()

def hubfunc(wxreq):
	try:
		tmplist= beidouapp.wx_query(wxreq['Content'])
	except :
		return {'TooUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'text', 'Content': '真不好意思，服务器给您跪了，可能您的调戏方式不对，请重新调戏或直接访问北斗网  http://ibeidou.net' ,'FuncFlag': 1,}
	if not tmplist: 
		return {'TooUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'text', 'Content': '真不好意思，这个关键词没有对应内容，请换个关键词或直接访问北斗网    http://ibeidou.net' ,'FuncFlag': 0,}
	else: , 
		return {'TooUserName': wxreq['FromUserName'],'FromUserName': wxreq['ToUserName'], 'MsgType': 'news', 'Articles': tmplist ,'FuncFlag': 0,}
