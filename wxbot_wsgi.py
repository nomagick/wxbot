import bottle

import wxclass
from apphub import hubfunc

@bottle.get('/wxbot.xml')
def wxauth():
#	argdict= bottle.request.forms.decode()
#	authobj= wxclass.WxAuth(argdict)
#	sendback= authobj.reply()
#	return sendback
	return wxclass.WxAuth(bottle.request.GET.decode()).reply()

@bottle.post('/wxbot.xml')
def wxreply():
	xmlstr= bottle.request.body.read().decode()
	request= wxclass.WxRequest(xmlstr)
	print (request)
	response= hubfunc(request)
	print(response)
	debugstr= bottle.template(response[0],data=response[1])
	print(debugstr)
	return debugstr

#bottle.debug(True)
if __name__ == '__main__':
	bottle.run(host='0.0.0.0', port=80)
else:
	application=bottle.app()
