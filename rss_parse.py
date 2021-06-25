
import parser_all
from feedparser import *
from pprint import pprint
from datetime import datetime
from time import mktime
import json



RSS_URL = "https://www.pravda.com.ua/rss/view_news/"

feed = parse(RSS_URL)

urls = {
    # --сайт------------назва блока--кл.блока---кл.текста------кл.картинки--         
    'www.epravda.com.ua': ['div', 'post__text', 'post__text', 'image-box'],
    'www.pravda.com.ua': ['article', 'post', 'post_text', 'post_photo_news_img'],
    'live.pravda.com.ua': ['article', 'article', 'article', None],
    'www.eurointegration.com.ua': ['div', 'post__text', 'post__text', 'image-box'],
}


def write_json(address, dictionary):
    with open(address, 'w', encoding="utf-8") as outfile:
        json.dump(dictionary, outfile, indent=4,
                  sort_keys=False, ensure_ascii=False)
        outfile.close()


news = []

for item in feed.entries:
    data = {}
    data["title"] = item.title
    data["decription"] = item.summary
    data["url"] = item.link

    data["date"] = str(datetime.fromtimestamp(mktime(item.published_parsed)))

    for key in urls:
        if data["url"].split('/')[2] == key:
            data.update(parser_all.parse(
                data["url"], urls[key][0], urls[key][1], urls[key][2], urls[key][3]))
   
    news.append(data)
# pprint(news)

write_json('files/data.json', news)
