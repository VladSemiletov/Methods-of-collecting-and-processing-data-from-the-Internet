import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/english/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath(
            '//a[@class="product-title-link"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        title = response.xpath('//div[@id="product-title"]/h1/text()').get()
        link = response.url
        author = response.xpath('//div[@class="authors"]/a/text()').get()
        price = response.xpath(
            '//span[@class="buying-priceold-val-number"]/text()').get()
        price_sale = response.xpath(
            '//span[@class="buying-pricenew-val-number"]/text()').get()
        rating = response.xpath('//div[@id="rate"]/text()').get()
        item = BookparserItem(title=title, link=link, author=author,
                              price=price, price_sale=price_sale, rating=rating)
        yield item
