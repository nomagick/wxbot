import bottle

import wxclass

from wxophub import appfunc
#from apphub import hubfunc
#
#@bottle.get('/wxbot.xml')
#def wxauth():
#	return wxclass.WxAuth(bottle.request.GET.decode(), token='jjjjjjj').reply()
#
#@bottle.post('/wxbot.xml')
#def wxreply():
#	request= wxclass.WxRequest(bottle.request.body.read().decode())
#	response= hubfunc(request)
#	return bottle.template(response['MsgType'],data=response)

@bottle.get('/ibeidou.xml')
def wxauth():
	return wxclass.WxAuth(bottle.request.GET.decode(), token='wxbotbyavastms').reply()

@bottle.post('/ibeidou.xml')
def wxreply():
	request= wxclass.WxRequest(bottle.request.body.read().decode())
	response= appfunc(request)
	return bottle.template(response['MsgType'],data=response)

#@bottle.post('/debug')
#def wxdebug():
##	xmlstr= bottle.request.body.read().decode()
#	request= wxclass.WxRequest(bottle.request.forms.decode(), debug=True)
#	response= hubfunc(request)
#	print (response)
#	return bottle.template(response['MsgType'],data=response)
#
#@bottle.get('/debug')
#def debug():
#	res= """
#	<form action="/debug" method="POST">
#	<input type="text" name="FromUserName" value="123456"/>
#	<input type="text" name="ToUserName" value="654321"/>
#	<input type="text" name="MsgType" value="text"/>
#	<input type="text" name="Content" />
#	<input type="submit">
#	</form>
#	"""
#	return res

if __name__ == '__main__':
	bottle.debug(True)
	bottle.run(host='0.0.0.0', port=80)
else:
	application=bottle.app()