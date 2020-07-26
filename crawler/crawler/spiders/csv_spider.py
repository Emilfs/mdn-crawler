import os
import logging
import w3lib.html
import pypandoc
import scrapy

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
        clean_resp = w3lib.html.remove_tags_with_content(response.text, which_ones=('script', 'head', 'header', 'footer', 'span', 'section', 'button', 'div',))
        rst_out = pypandoc.convert_text(clean_resp, 'rst', format='html')

        data = rst_out.splitlines(True)
        with open(filename, 'w') as f:
            f.writelines(data[4:])

    def parse(self, response):
        title = response.xpath('//title/text()').extract_first()
        filename = 'rst/%s.rst' % title
        os.makedirs("rst/", exist_ok=True)

        # self.save_to_html(response, filename)
        self.convert_to_rst(response, filename)
        logger.info('Link saved to file %s' % response.url)
