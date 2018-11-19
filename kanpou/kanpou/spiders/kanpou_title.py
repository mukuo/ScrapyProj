import scrapy
from bs4 import BeautifulSoup

from kanpou.items import KanpouTodayItem
#from items import KanpouTodayItem

class KanpouTitleSpider(scrapy.Spider):
    name = 'kanpou_title'
    allowed_domains = ['kanpou.npb.go.jp']
    start_urls = ['http://kanpou.npb.go.jp/']

    def parse(self, response):
        soup = BeautifulSoup(response.body,'lxml')

        baseurl = 'http://kanpou.npb.go.jp/'

        #本日の官報から取得
        content = soup.find('div', {'class': 'todayBox'})
        links = content.find_all('a')
#       if len(links) < 1:
#            # ハイパーリンクがない場合終了
#            return
        for path in links:
            url = '{baseurl}{path}'.format(baseurl=baseurl, path=path.attrs['href'])
            yield scrapy.Request(url, self.parse_title)

        #過去30日の官報から取得
        content = soup.find('div', {'class': 'archiveBox'})
        links = content.find_all('a')
        for path in links:
            url = '{baseurl}{path}'.format(baseurl=baseurl, path=path.attrs['href'])
            yield scrapy.Request(url, self.parse_title)

    def parse_title(self, response):
        soup = BeautifulSoup(response.body,'lxml')

        #官報の日付と号数（改行コード削除）
        paper = soup.find('p', {'class': 'date'}).text.replace('\r','').replace('\n','')
        #タイトル含むパーサ
        content = soup.find('div', {'class': 'contentsBox'})
        groups = content.find_all('a')

        #span class="text"の記事タイトルとリンク先を取得
        for group in groups:
            item = KanpouTodayItem()
            item['paper'] = paper
            item['title'] = group.find('span', {'class' : 'text'}).text
            item['links'] = group.attrs['href']
            yield item
