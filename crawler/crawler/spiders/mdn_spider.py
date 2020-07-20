import scrapy
import os


class MdnSpider(scrapy.Spider):
    name = "mdn"
    start_urls = [
        'https://developer.mozilla.org/en-US/docs/Mozilla',
        'https://developer.mozilla.org/en-US/docs/Tools',
        'https://wiki.developer.mozilla.org/en-US/docs/tag/mozilla?page=1',
    ]
    done = {}

    def is_mdn(self, response):
        titlebar = response.css('div.titlebar-container')
        if titlebar:
            return True

        # from scrapy.selector import Selector
        # input_tag = Selector(text=html_content).xpath("//input[contains(concat(' ', @class, ' '), ' nextbutton ')]")
        # if input_tag:
        #     print "Yes, I found a 'next' button on the page."

    def save_to_html(self):
        pass

    def next_page(self):
        pass


    def parse(self, response):
        title = response.css('div.titlebar h1.title::text').get()
        filename = 'htmls/%s.html' % title
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        if self.is_mdn(response) and title not in self.done:
            url = response.url
            self.done[title] = url

            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filename)


        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)