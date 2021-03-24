import scrapy
class Dofollow(scrapy.Spider):
    name="dofollow"

    start_urls = [
        'https://www.chubiagro.com.ng/farmslisting'
    ]


    def parse(self, response):
        dir = 'Chubiagro/'
        for farm in response.css("div#farmlisting"):
            yield {
                'farm_name': farm.css("div.farm-name h5 a::text").get(),
                'farm_img': farm.css("div.farm-image a img::attr(src)").get(),
                'farm_status': farm.css("div.farm-status h3::text")[1].get(),
                'farm_link': farm.css("div.farm-name h5 a::attr(href)").get()

            }

        next_page_link = ''

        next_page_id = 2

        query_next_page = response.css("div.farmslinks ul.pagination li.page-item")

        active_page_id = response.css("div.farmslinks ul.pagination li.page-item.active span.page-link::text").get()

        if query_next_page is not None:
            next_page_link = query_next_page.css('a::attr(href)').get()
        else:
            next_page_link = None

        if next_page_link is not None and int(active_page_id) < int(next_page_id):

            full_next_page_url = response.urljoin(next_page_link)

            next_page_id = query_next_page.css("a::text").get()

            yield scrapy.Request(full_next_page_url, callback=self.parse)

        self.log(f'all links fetched from {self.start_urls[0]}')