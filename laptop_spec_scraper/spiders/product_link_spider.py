import scrapy
from ..items import LaptopSpecScraperItem

class ProductLinkSpider(scrapy.Spider):
    name = 'ProductLinks'
    page_count = 2

    custom_settings = {
        'ITEM_PIPELINES': {
            "laptop_spec_scraper.pipelines.ProductLinkScraperPipeline": 300,
        }
    }

    def start_requests(self):
        # Starting URL for the first page of laptop search results
        url = 'https://www.flipkart.com/search?q=laptops&page=1'
        yield scrapy.Request(url=url, callback=self.parse)

        
    def parse(self, response):
        # Initialize the item
        item = LaptopSpecScraperItem()

        # Extract product titles and links from the current page
        product_titles = response.css("._4rR01T::text").extract()
        product_links = response.css("._1fQZEK::attr(href)").extract()


        # Iterate through product titles and links
        for product_title, product_link in zip(product_titles,product_links):

            item["title"] = product_title
            item["link"] = product_link

            yield item

        # Prepare URL for the next page
        next_page = 'https://www.flipkart.com/search?q=laptops&page='+ str(self.page_count)

        # Check if there are more pages to scrape
        if   response.css("._4rR01T::text").extract(): # not empty --> true
            self.page_count+=1
            yield response.follow(next_page, callback=self.parse)






