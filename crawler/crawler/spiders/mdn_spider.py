import os
import logging
import w3lib.html
import pypandoc
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



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

        To test:
        - put div on the 3rd position
        - determine what to use from the combination of span, section, button (the lesser the better)
        """
        clean_resp = w3lib.html.remove_tags_with_content(response.text, which_ones=('script', 'head', 'header', 'footer', 'span', 'section', 'button', 'div',))
        rst_out = pypandoc.convert_text(clean_resp, 'rst', format='html')

        # with open(filename, 'w') as f:
        #     f.write(rst_out)
        """
        delete the comment above and use it instead of the bottom one
        pros = the first 3 line is gone
        cons = need more resource, could cause unwanted side effects since we are using writelines instead of write
        """
        data = rst_out.splitlines(True)
        with open(filename, 'w') as f:
            f.writelines(data[4:])


    def parse_item(self, response):
        title = response.xpath('//title/text()').extract_first()
        filename = 'rst/%s.rst' % title #response.url.rsplit('/', 1)[-1]
        os.makedirs("rst/", exist_ok=True)

        if self.is_mdn(response):
            # self.save_to_html(response, filename)
            self.convert_to_rst(response, filename)
            logger.info('Link saved to file %s' % response.url)





