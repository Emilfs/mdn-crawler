import os
import logging
import pypandoc
import scrapy
from bs4 import BeautifulSoup

logger = logging.getLogger()

class CsvSpider(scrapy.Spider):
    name = "csv"

    start_urls = []
    my_file = open("crawler/csv/migration_list.csv", "r")
    for i in my_file:
        u = i.split('\n')
        start_urls.append(u[0])

    def save_to_html(self, response, filename):
        with open(filename, 'wb') as f:
            f.write(response.body)

    def convert_to_rst(self, response, filename):
        soup = BeautifulSoup(response.text, 'html5lib')
        clean_resp = soup.find("article", id="wikiArticle")
        if clean_resp:
            rst_out = pypandoc.convert_text(clean_resp, 'rst', format='html')

        with open(filename, 'w') as f:
            f.write(rst_out)

    def parse(self, response):
        title = response.xpath('//title/text()').extract_first()
        filename = 'rst/%s.rst' % title
        os.makedirs("rst/", exist_ok=True)

        # self.save_to_html(response, filename)
        self.convert_to_rst(response, filename)
        logger.info('Link saved to file %s' % response.url)
