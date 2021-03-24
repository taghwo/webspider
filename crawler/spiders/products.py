import scrapy
from collections import deque 
class Products(scrapy.Spider):
    name="products"
    def start_requests(self):
        urls = [
            "http://jumia.com.ng"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'jumia_products.html'
        product_names = response.css("div.name").getall()
        product_prices = response.css("div.prc").getall()
        product_tag_dscts = response.css("div.tag._dsct").getall()
        product_links = response.css("div.itm.col a.prd._box::attr(href)").getall()

        def modify_links(link):
            split_link = link.split("/",0)
            split_link.insert(0,"https://jumia.com.ng")
            full_link = "".join(split_link)
            return full_link

        mod_links = list(map(modify_links, product_links))

        for product, price, dsct, link in zip(product_names,product_prices, product_tag_dscts, mod_links):
              with open(filename, 'a+', encoding="latin-1", errors='ignore') as f:
                  print(dict(name=product,price=price,discount=dsct, link=link))
                  f.write(str(dict(name=product,price=price,discount=dsct, link=link)))
        self.log(f'Saved file {filename}')