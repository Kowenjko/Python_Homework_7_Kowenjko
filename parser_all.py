"""

------Parse-------
'pravda.com.ua',
'eurointegration.com.ua',
'live.pravda.com.ua',
'epravda.com.ua'
------------------
"""

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json


def write_json(address, dictionary):
    with open(address, 'w', encoding="utf-8") as outfile:
        json.dump(dictionary, outfile, indent=4,
                  sort_keys=False, ensure_ascii=False)
        outfile.close()


def parse(url, where, post, class_text, class_img):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    article = soup.find(where, class_=post)
    
    data = {}
   

    data["content"] = []
    #Якщо текст рохміщується разом з картикою в одному блоці
    if post == class_text:
        # Якщо назма блока співпадає з классом
        if where == post:
            div_image = article.find('table')
            data['preview'] = 'https://life.pravda.com.ua/' + \
                div_image.find('img').get('src')
            element = article.find('p')
        else:
            div_image = article.find('div')
            #Перевіряємо чи є картинка
            if div_image.find('img'):
                data['preview'] = div_image.find('img').get('src')
        element = article.find('p')
    else:
        #Перевіряємо чи є картинка
        if article.find('img', class_=class_img):
            data['preview'] = article.find('img', class_=class_img).get('src')
        post_text = article.find('div', class_=class_text)
        element = post_text.find('p')
        data["content"].append({'p': element.text})
        # data["content"].append(element.text)
    while element != None:
        element = element.find_next_sibling()
        if element == None:
            break
        if element.name == 'p':
            data["content"].append({'p': element.text})
            # data["content"].append(element.text)
        elif element.name == 'div':
            #якщо реклама пропускаємо
            if element.find('a'):
                continue
            img = element.find('img')
            if img == None:
                continue
            # Різні сайти мають не одинакові src
            if post == class_text:
                data["content"].append({'img': img.get('src')})
            else:
                data["content"].append({'img': 'https:' + img.get('src')})
    
    return data


if __name__ == '__main__':
    # parse("https://www.epravda.com.ua/rus/news/2021/06/24/675329/", 'div', 'post__text',
    #       'post__text', 'image-box')
    parse("https://www.pravda.com.ua/rus/news/2021/06/24/7298338/", 'article', 'post',
          'post_text', 'post_photo_news_img')
    # parse("https://life.pravda.com.ua/health/2021/06/25/245264/", 'article', 'article',
    #       'article', None)
