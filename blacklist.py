import requests
import re
from bs4 import BeautifulSoup as bs
from input import DOMAINS

class BlackList():
    domains = DOMAINS
    
    def __init__(self, url):
        self.url = url
        self.emails = set()
    
    def trace(func):
        def wrap(self):
            print('Checking', self.url)
            print('-'*20)
            func(self)
            print('-'*20, '\n')
        return wrap
        
    @trace
    def collect_emails(self):
        parser = bs(requests.get(self.url).text, 'html.parser')
        titles = (tag.get('title') for tag in parser.find_all('a'))
        for title in titles:
            try:
                if any(domain in title for domain in BlackList.domains):
                    self.emails.add(title)
            except TypeError:
                pass
        if not self.emails:
            print('Have got no emails with domains:')
            print(*BlackList.domains, sep=', ')
        return
        
    def get_date(self):
        parser = bs(requests.get(self.url).text, 'html.parser')
        try:
            self.date = re.search('\d{4}-\d{2}-\d{2}', str(parser.h1)).group()
        except AttributeError:
            self.date = ''
        return self.date
