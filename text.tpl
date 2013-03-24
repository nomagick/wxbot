<xml>
<ToUserName><![CDATA[{{data['to']}}]]></ToUserName>
<FromUserName><![CDATA[{{data['from']}}]]></FromUserName>
<CreateTime>{{int(time())}}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{{data['content']}}]]></Content>
<FuncFlag>{{data['flag']}}</FuncFlag>
</xml>