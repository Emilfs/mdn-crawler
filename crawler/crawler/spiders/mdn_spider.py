import os
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import w3lib.html

import pypandoc

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
        clean_resp = w3lib.html.remove_tags_with_content(response.text, which_ones=('script', 'head', 'header', 'footer', 'span', 'section', 'button', 'div',))
        rst_out = pypandoc.convert_text(clean_resp, 'rst', format='html')

        # with open(filename, 'w') as f:
        #     f.write(rst_out)
        data = rst_out.splitlines(True)
        with open(filename, 'w') as f:
            f.writelines(data[4:])


    def parse_item(self, response):
        # title = response.css('div.titlebar h1.title::text').get()
        title = response.xpath('//title/text()').extract_first()
        filename = 'htmls/%s.rst' % title #response.url.rsplit('/', 1)[-1]
        os.makedirs("htmls/", exist_ok=True)

        if self.is_mdn(response):
            # self.save_to_html(response, filename)
            self.convert_to_rst(response, filename)
            logger.info('Link saved to file %s' % response.url)





