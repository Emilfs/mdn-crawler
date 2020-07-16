import scrapy


class MdnSpider(scrapy.Spider):
    name = "mdn"
    start_urls = [
        'https://developer.mozilla.org/en-US/docs/Mozilla',
        'https://developer.mozilla.org/en-US/docs/Tools',
        'https://wiki.developer.mozilla.org/en-US/docs/tag/mozilla?page=1',
    ]

    def parse(self, response):
        title = response.css('div.titlebar::text').get()
        filename = '%s.html' % title
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)