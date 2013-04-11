import bottle

import wxclass
from apphub import hubfunc

@bottle.get('/wxbot.xml')
def wxauth():
#	argdict= bottle.request.forms.decode()
#	authobj= wxclass.WxAuth(argdict)
#	sendback= authobj.reply()
#	return sendback
	return wxclass.WxAuth(bottle.request.GET.decode(), token='jjjjjjj').reply()

@bottle.post('/wxbot.xml')
def wxreply():
	xmlstr= bottle.request.body.read().decode()
	request= wxclass.WxRequest(xmlstr)
	response= hubfunc(request)
	return bottle.template(response['MsgType'],data=response)

#@bottle.get('/debug')
#def debug():
#	response= hubfunc(request)
#	print(response)
#	debugstr= bottle.template(response[0],data=response[1])
#	print(debugstr)
#	return debugstr


if __name__ == '__main__':
	bottle.debug(True)
	bottle.run(host='0.0.0.0', port=8080)
else:
	application=bottle.app()