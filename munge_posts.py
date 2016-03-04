import json
import app
from datetime import datetime

dat = app.post_list
for post in dat:
    datetime_obj = post['date']
    post['month'] = datetime_obj.month
    post['day'] = datetime_obj.day
    post['year'] = datetime_obj.year
    del post['date']
    del post['template']
    post['route'] = '//residentmar.io/' + post['route']

with open('./static/json/post_list.json', 'w') as outfile:
    json.dump(dat, outfile, indent=4)

xml = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<atom:link href="http://residentmar.io/feed" rel="self" type="application/rss+xml" />
<title>Data Hacks</title>
<link>http://www.residentmar.io/</link>
<description>Data hacks and other musings by Aleksey Bilogur</description>
"""

for post in dat:
    xml += """
    <item>
            <title>{0}</title>
            <link>{1}</link>
            <guid>{1}</guid>
            <pubDate>{2}</pubDate>
    """.format(post['title'], 'http:' + post['route'], datetime(post['year'], post['month'],
                                                                post['day']).strftime('%a, %d %b %Y %H:00:00 EST'))
    xml += """</item>"""

xml += """
</channel>
</rss>
"""

with open('./static/json/post_list.json', 'w') as outfile:
    json.dump(dat, outfile, indent=4)

with open('./templates/rss.xml', 'w') as outfile:
    outfile.write(xml)