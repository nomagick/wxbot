<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>{{len(data['Articles'])}}</ArticleCount>
<Articles>
%for article in data['Articles']
<item>
<Title><![CDATA[{{article['Title']}}]]></Title> 
<Description><![CDATA[{{article['Description']}}]]></Description>
<PicUrl><![CDATA[{{article['PicUrl']}}]]></PicUrl>
<Url><![CDATA[{{article['Url']}}]]></Url>
</item>
%end
</Articles>
%rebase common data=data