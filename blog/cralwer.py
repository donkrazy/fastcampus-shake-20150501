# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from time import sleep
try:
    from urllib.parse import urljoin  # python 3
except ImportError:
    from urlparse import urljoin  # python 2
from bs4 import BeautifulSoup
import requests


class ClienNews(object):
    def __init__(self, name, url):
        self.id = None
        self.name = name
        self.url = url 
        self.content = ''

        matched = re.search(r'wr_id=(\d+)', self.url)
        if matched:
            self.id = int(matched.group(1))
        else:
            # 포스팅 아이디 (wr_id) 는 각 포스팅을 구별하는 중요한 요소이다.
            raise ValueError('not found wr_id from {}'.format(self.url))

    def update_content(self):
        soup = self.get_page_soup(self.url)
        self.content = soup.select('#writeContents')[0].text

    @classmethod
    def get_page_soup(cls, url):
        response = requests.get(url)
        response.encoding = 'utf8'  # 클리앙 사이트에서 인코딩 탐지에 실패하여, 인코딩을 utf8 로 강제시킴.
        html = response.text
        return BeautifulSoup(html)

    @classmethod
    def get_news(cls, page=1):
        clien_news_url = "http://www.clien.net/cs2/bbs/board.php?bo_table=news&page={}".format(page)
        soup = cls.get_page_soup(clien_news_url)

        clien_news_list = []

        # for tr_tag in soup.select('.board_main tbody .mytr'):  # 이와 같이 하고 싶었으나, 마크업이 꼬여있어서 못함 ㅠ_ㅠ
        for tr_tag in soup.select('.mytr'):
            try:
                link_tag = tr_tag.select('.post_subject a')[0]
            except IndexError:
                continue

            name = link_tag.text.strip()
            url = urljoin(clien_news_url, link_tag['href'])

            clien_news = ClienNews(name, url)
            clien_news.update_content()
            clien_news_list.append(clien_news)

            # break
            sleep(0.1)  # 서버에 부하를 적게 주기 위해서, 임의시간으로 딜레이를 줍니다.

        return clien_news_list


if __name__ == '__main__':
    print('crawling ...')
    for clien_news in ClienNews.get_news():
        print('[{}] {}'.format(clien_news.id, clien_news.name))

