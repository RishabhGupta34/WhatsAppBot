import json
import requests
from bs4 import BeautifulSoup
from gnews_utils import editionMap, langMap

class NotFound(Exception):
    """Raised when the list articles in the function scapefeed() is empty"""
    pass


class gnewsclient:

    def __init__(self, edition='United States (English)',
                 location=None,language='english',url=None):
        self.editions = list(editionMap)
        self.languages = list(langMap)
        self.edition = edition
        self.location = location
        self.language = language
        self.url=url
        self.params = {
        				'output': 'atom',
                       'ned': self.edition,
                       'geo': self.location,
                       'hl': self.language}

    def get_config(self):
        config = {
            'edition': self.edition,
            'language': self.language,
            'location': self.location
        }
        return config

    def reset(self):
        self.edition = 'United States (English)'
        self.language = 'english'
        self.location = None

    def get_news(self):
        status = self.set_params()
        if status is False:
            return

        soup = self.load_feed()
        articles = self.scrape_feed(soup)
        return articles

    def set_params(self):
        try:
            self.params['ned'] = editionMap[self.edition]
        except KeyError:
            print(f"{self.edition} edition not found.\n"
                  f"Use editions attribute to get list of editions.")
            return False
        try:
            self.params['hl'] = langMap[self.language]
        except KeyError:
            print(f"{self.language} language not found.\n"
                  f"Use langugaes attribute to get list of languages.")
            return False

        if self.location is not None:
            self.params['geo'] = self.location
        return True

    def load_feed(self):
        url = "https://news.google.com/news"
        resp = requests.get(url, params=self.params)
        soup = BeautifulSoup(resp.content, 'html5lib')
        return soup

    def scrape_feed(self, soup):
        entries = soup.findAll('entry')
        articles = []

        for i in range(0,min(4,len(entries))):
            article = {}
            article['title'] = entries[i].title.text
            article['link'] = entries[i].link['href']
            timer=entries[i].updated.text
            article['releasedAt'] = " ".join([timer.split('T')[0],timer.split('T')[1].split('.')[0]])
            articles.append(article)
        try:
            if len(articles) == 0:
                raise NotFound
        except NotFound:
                print("The articles for the given response are not found.")
                return
        return articles