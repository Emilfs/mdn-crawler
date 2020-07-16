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

    def parse(self, response):
        title = response.css('div.titlebar::text').get()
        filename = 'htmls/%s.html' % title
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        if title not in self.done:
            url = response.url
            self.done[title] = url

            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filename)


        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)