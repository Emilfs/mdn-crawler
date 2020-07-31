import os
import logging
import w3lib.html
import pypandoc
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup



logger = logging.getLogger()

class MdnSpider(CrawlSpider):
    name = "mdn"
    allowed_domains = ['developer.mozilla.org']
    start_urls = [
        'https://developer.mozilla.org/en-US/docs/Mozilla',
        'https://developer.mozilla.org/en-US/docs/Tools',
        # 'https://wiki.developer.mozilla.org/en-US/docs/tag/mozilla?page=1',
    ]
    rules = (
        Rule(LinkExtractor(allow=(r'/en-US', r'/en', '\.html',), deny=('.{1,}\$.{1,}', '.{1,}\?.{1,}')), callback='parse_item', follow=True),
    )

    def is_mdn(self, response):
        titlebar = response.css('div.titlebar-container')
        if titlebar:
            return True

    def save_to_html(self, response, filename):
        with open(filename, 'wb') as f:
            f.write(response.body)

    def convert_to_rst(self, response, filename):
        """
        edit the which_ones to know which is going to be deleted

        To do:
        - we should make an argument for the crawler so that it could take webpage link as args so that it can scrape individually
        - the argument can also target a csv file and scrape the links in the csv
        """
        soup = BeautifulSoup(response.text, 'html5lib')
        clean_resp = soup.find("article", id="wikiArticle")
        if clean_resp:
            rst_out = pypandoc.convert_text(clean_resp, 'rst', format='html')

        with open(filename, 'w') as f:
            f.write(rst_out)


    def parse_item(self, response):
        title = response.xpath('//title/text()').extract_first()
        filename = 'rst/%s.rst' % title #response.url.rsplit('/', 1)[-1]
        os.makedirs("rst/", exist_ok=True)

        if self.is_mdn(response):
            # self.save_to_html(response, filename)
            self.convert_to_rst(response, filename)
            logger.info('Link saved to file %s' % response.url)





