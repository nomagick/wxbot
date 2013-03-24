<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>{{len(data['articles'])}}</ArticleCount>
<Articles>
%for article in data['articles']
<item>
<Title><![CDATA[{{article['title']}}]]></Title> 
<Description><![CDATA[{{article['description']}}]]></Description>
<PicUrl><![CDATA[{{article['picurl']}}]]></PicUrl>
<Url><![CDATA[{{article['url']}}]]></Url>
</item>
%end
</Articles>
%rebase common, data=data