%from time import time
<xml>
<ToUserName><![CDATA[{{data['to']}}]]></ToUserName>
<FromUserName><![CDATA[{{data['from']}}]]></FromUserName>
<CreateTime>{{int(time())}}</CreateTime>
%include
<FuncFlag>{{data['flag']}}</FuncFlag>
</xml> 