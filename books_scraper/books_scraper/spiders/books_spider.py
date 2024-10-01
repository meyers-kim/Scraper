import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for book in response.css('article.product_pod'):
            yield {
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('div.product_price p.price_color::text').get(),
                'availability': book.css('div.product_price p.instock.availability::text').re_first('\S+')
            }

        # Go to the next page
        next_page = response.css('ul.pager li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
